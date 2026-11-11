"""
Build the company-year panel and estimate the AI-period effect on revenue per person.

Input:  financials.csv, headcount.csv
Output: panel.csv (one row per company and fiscal year), printed tables and model results.

Model (OLS, company fixed effects, standard errors clustered by company):
    g_rpp = company effect + b1 * g_hc + b2 * g_hc_lag + sum_m d_m * (post * model_m)

    g_rpp     log change of revenue per person (local currency)
    g_hc      log change of average headcount (hiring cycle)
    g_hc_lag  same, one year earlier
    post      fiscal year midpoint on or after 2024-01-01 (AI coding tools in daily use)
    d_m       change of the yearly growth of revenue per person in the AI period,
              for each business model, after the hiring cycle is removed

Years with midpoint in 2020-2021 (COVID) are excluded. For travel companies
(EXPE, BKNG, ABNB) 2022 is also excluded (travel recovery).

Usage:
    python build_panel.py
"""

import csv
import math
import sys
from datetime import date, timedelta
from pathlib import Path

import numpy as np

HERE: Path = Path(__file__).resolve().parent
TRAVEL: set[str] = {"EXPE", "BKNG", "ABNB"}
POST_START: date = date(2024, 1, 1)
MODELS: list[str] = ["vendor_time", "vendor_fixed", "product"]


def read(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def nearest(rows: list[dict[str, str]], end: date, days: int = 45) -> dict[str, str] | None:
    """Return the headcount row closest to a fiscal year end (within `days`)."""
    best = min(rows, key=lambda r: abs((date.fromisoformat(r["date"]) - end).days), default=None)
    if best and abs((date.fromisoformat(best["date"]) - end).days) <= days:
        return best
    return None


def build() -> list[dict]:
    fin = read("financials.csv") + read("financials_manual.csv")
    hc = read("headcount.csv")
    out: list[dict] = []
    for ticker in dict.fromkeys(r["ticker"] for r in fin):
        f_rows = sorted((r for r in fin if r["ticker"] == ticker), key=lambda r: r["fy_end"])
        h_rows = [r for r in hc if r["ticker"] == ticker]
        prev: dict | None = None
        for r in f_rows:
            end = date.fromisoformat(r["fy_end"])
            this = nearest(h_rows, end)
            if this is None:
                prev = None
                continue
            if this["kind"] == "average":
                avg = float(this["employees"])
            else:
                before = nearest(h_rows, end - timedelta(days=365))
                if before is None:
                    prev = None
                    continue
                avg = (float(before["employees"]) + float(this["employees"])) / 2
            rev = float(r["revenue_m"])
            mid = end - timedelta(days=182)
            row = {
                "ticker": ticker, "model": r["model"], "fy_end": r["fy_end"], "midpoint": mid.isoformat(),
                "currency": r["currency"], "revenue_m": rev, "avg_headcount": round(avg),
                "rpp_k": round(rev / avg * 1000, 1),
                "gross_margin": round(1 - float(r["cost_of_revenue_m"]) / rev, 4) if r["cost_of_revenue_m"] else "",
                "operating_margin": round(float(r["operating_income_m"]) / rev, 4) if r["operating_income_m"] else "",
                "g_rpp": "", "g_hc": "", "g_rev": "", "g_hc_lag": "",
                "post": int(mid >= POST_START),
            }
            if prev is not None:
                row["g_rpp"] = round(math.log(row["rpp_k"] / prev["rpp_k"]), 4)
                row["g_hc"] = round(math.log(avg / prev["avg_headcount"]), 4)
                row["g_rev"] = round(math.log(rev / prev["revenue_m"]), 4)
                row["g_hc_lag"] = prev["g_hc"]
            excluded = mid.year in (2020, 2021) or (ticker in TRAVEL and mid.year == 2022)
            row["excluded"] = int(excluded)
            out.append(row)
            prev = row
    return out


def ols_cluster(y: np.ndarray, x: np.ndarray, groups: list[str]) -> tuple[np.ndarray, np.ndarray]:
    """OLS coefficients and cluster-robust standard errors (CR1)."""
    xtx_inv = np.linalg.pinv(x.T @ x)
    beta = xtx_inv @ x.T @ y
    resid = y - x @ beta
    meat = np.zeros((x.shape[1], x.shape[1]))
    uniq = sorted(set(groups))
    for g in uniq:
        idx = [i for i, gg in enumerate(groups) if gg == g]
        s = x[idx].T @ resid[idx]
        meat += np.outer(s, s)
    n, k, c = len(y), x.shape[1], len(uniq)
    scale = c / (c - 1) * (n - 1) / (n - k)
    cov = scale * xtx_inv @ meat @ xtx_inv
    return beta, np.sqrt(np.diag(cov))


def model(rows: list[dict]) -> None:
    data = [r for r in rows if r["g_rpp"] != "" and r["g_hc_lag"] != "" and not r["excluded"]]
    tickers = sorted({r["ticker"] for r in data})
    names = ["g_hc", "g_hc_lag"] + [f"post x {m}" for m in MODELS] + [f"fe {t}" for t in tickers]
    x = np.array([
        [r["g_hc"], r["g_hc_lag"]]
        + [r["post"] * (r["model"] == m) for m in MODELS]
        + [float(r["ticker"] == t) for t in tickers]
        for r in data
    ], dtype=float)
    y = np.array([r["g_rpp"] for r in data], dtype=float)
    beta, se = ols_cluster(y, x, [r["ticker"] for r in data])
    print(f"\nModel: n = {len(y)} company-years, {len(tickers)} companies, company fixed effects, clustered SE")
    print(f"{'term':22} {'coef':>8} {'SE':>8} {'t':>6}")
    for name, b, s in zip(names, beta, se):
        if name.startswith("fe "):
            continue
        print(f"{name:22} {b:8.4f} {s:8.4f} {b / s if s else float('nan'):6.2f}")
    # Same model without the hiring-cycle controls, for comparison.
    beta2, se2 = ols_cluster(y, x[:, 2:], [r["ticker"] for r in data])
    print("\nWithout hiring-cycle controls:")
    for name, b, s in zip(names[2:5], beta2, se2):
        print(f"{name:22} {b:8.4f} {s:8.4f} {b / s if s else float('nan'):6.2f}")

    # Difference-in-differences: company and year fixed effects. Year effects remove
    # everything common to all companies in a year (demand, inflation, AI hype).
    # The post terms then measure the AI-period change against time-billing vendors.
    years = sorted({r["midpoint"][:4] for r in data})[1:]
    did_names = ["g_hc", "g_hc_lag", "post x vendor_fixed", "post x product"]
    xd = np.array([
        [r["g_hc"], r["g_hc_lag"], r["post"] * (r["model"] == "vendor_fixed"), r["post"] * (r["model"] == "product")]
        + [float(r["ticker"] == t) for t in tickers]
        + [float(r["midpoint"][:4] == yv) for yv in years]
        for r in data
    ], dtype=float)
    beta3, se3 = ols_cluster(y, xd, [r["ticker"] for r in data])
    print("\nDiD (company + year fixed effects), against time-billing vendors:")
    for name, b, s in zip(did_names, beta3, se3):
        print(f"{name:22} {b:8.4f} {s:8.4f} {b / s if s else float('nan'):6.2f}")
    print("(post x vendor_fixed is one company, ACN: its SE is not reliable.)")

    # Same DiD for the yearly change of operating margin (who keeps the gain).
    prev_m: dict[str, float] = {}
    mrows: list[tuple[dict, float]] = []
    for r in rows:
        m = r["operating_margin"]
        key = r["ticker"]
        if m != "" and key in prev_m and not r["excluded"]:
            mrows.append((r, (m - prev_m[key]) * 100))
        prev_m[key] = m if m != "" else prev_m.get(key)
    mt = sorted({r["ticker"] for r, _ in mrows})
    my = sorted({r["midpoint"][:4] for r, _ in mrows})[1:]
    xm = np.array([
        [r["post"] * (r["model"] == "vendor_fixed"), r["post"] * (r["model"] == "product")]
        + [float(r["ticker"] == t) for t in mt]
        + [float(r["midpoint"][:4] == yv) for yv in my]
        for r, _ in mrows
    ], dtype=float)
    ym = np.array([d for _, d in mrows])
    b4, s4 = ols_cluster(ym, xm, [r["ticker"] for r, _ in mrows])
    print(f"\nDiD on operating margin change (points per year), n = {len(ym)}:")
    for name, b, s in zip(["post x vendor_fixed", "post x product"], b4, s4):
        print(f"{name:22} {b:8.2f} {s:8.2f} {b / s if s else float('nan'):6.2f}")
    for grp in MODELS:
        pre = [d for r, d in mrows if r["model"] == grp and not r["post"]]
        post = [d for r, d in mrows if r["model"] == grp and r["post"]]
        print(f"{grp:13} mean margin change pre {sum(pre) / len(pre):+.2f} pt/yr, post {sum(post) / len(post):+.2f} pt/yr")


def describe(rows: list[dict]) -> None:
    print(f"\n{'ticker':6} {'model':13} {'pre g_rpp':>10} {'post g_rpp':>11} {'pre g_hc':>9} {'post g_hc':>10} {'pre elast':>10} {'post elast':>11} {'post years'}")
    for t in dict.fromkeys(r["ticker"] for r in rows):
        rs = [r for r in rows if r["ticker"] == t and r["g_rpp"] != "" and not r["excluded"]]
        pre = [r for r in rs if not r["post"]]
        post = [r for r in rs if r["post"]]

        def mean(v: list[float]) -> float:
            return sum(v) / len(v) if v else float("nan")

        def elast(v: list[dict]) -> float:
            hc = sum(r["g_hc"] for r in v)
            return sum(r["g_rev"] for r in v) / hc if abs(hc) > 1e-9 else float("nan")

        print(f"{t:6} {rs[0]['model'] if rs else '':13} {mean([r['g_rpp'] for r in pre]):10.3f} {mean([r['g_rpp'] for r in post]):11.3f} "
              f"{mean([r['g_hc'] for r in pre]):9.3f} {mean([r['g_hc'] for r in post]):10.3f} {elast(pre):10.2f} {elast(post):11.2f} "
              f"{','.join(r['fy_end'][:7] for r in post)}")


def main() -> int:
    rows = build()
    with (HERE / "panel.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} rows -> panel.csv")
    describe(rows)
    model(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
