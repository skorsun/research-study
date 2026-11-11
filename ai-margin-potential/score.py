"""
AI margin-potential score for the 16 panel companies, and its test against
the operating margin change after 2023.

Input:  ../panel/panel.csv
Output: score.csv, results.json (the values in section 4.3 of the paper)

Score (0-100) = mean of 4 components, each scaled 0-1 across the 16 companies (min-max),
all measured in the base year (fiscal year with midpoint in 2023):
    1. revenue model:       vendor paid for time = 0, fixed-price vendor = 0.5, product = 1
    2. gross margin:        1 - cost of revenue / revenue
    3. overhead share:      gross margin - operating margin (R&D, sales, G&A as % of revenue)
    4. revenue per person:  log of revenue per person in USD

Outcome: operating margin change per year from the base year to the latest fiscal year.

Usage:
    python score.py
"""

import csv
import json
import math
import sys
from pathlib import Path

import numpy as np

HERE: Path = Path(__file__).resolve().parent
PANEL: Path = HERE.parent / "panel" / "panel.csv"

# Fixed 2023 average exchange rates, to put revenue per person in USD.
FX_2023: dict[str, float] = {"USD": 1.0, "EUR": 1.08, "INR": 1 / 82.6, "GBP": 1.24}
MODEL_VALUE: dict[str, float] = {"vendor_time": 0.0, "vendor_fixed": 0.5, "product": 1.0}
NAMES: dict[str, str] = {
    "EPAM": "EPAM", "CTSH": "Cognizant", "INFY": "Infosys", "WIT": "Wipro", "GLOB": "Globant",
    "DAVA": "Endava", "ACN": "Accenture", "SAP": "SAP", "EXPE": "Expedia", "ADBE": "Adobe",
    "INTU": "Intuit", "BKNG": "Booking", "CRM": "Salesforce", "NOW": "ServiceNow",
    "WDAY": "Workday", "ABNB": "Airbnb",
}
# Gross margin not tagged in XBRL: derived from the 10-K expense lines (base year).
# Intuit FY2023: total costs 11,227 - R&D 2,539 - S&M 3,762 - G&A 1,300 = 3,626 (includes
#   amortization of acquired intangibles, so the gross margin is a lower bound).
# Workday FY2024 (ends Jan 2024): operating expenses 7,076 - R&D 2,464 - S&M 2,139 - G&A 702 = 1,771.
# Booking has no cost of revenue line: gross margin and overhead share are not defined.
DERIVED_COST: dict[str, float] = {"INTU": 3626.0, "WDAY": 1771.0}


def scale(values: dict[str, float | None]) -> dict[str, float | None]:
    """Min-max scale to 0-1, keep None."""
    known = [v for v in values.values() if v is not None]
    lo, hi = min(known), max(known)
    return {k: None if v is None else (v - lo) / (hi - lo) for k, v in values.items()}


def main() -> int:
    rows = list(csv.DictReader(PANEL.open(encoding="utf-8")))
    base: dict[str, dict] = {}
    last: dict[str, dict] = {}
    for r in rows:
        if r["midpoint"][:4] == "2023":
            base[r["ticker"]] = r
        if r["operating_margin"] != "":
            last[r["ticker"]] = r

    raw: dict[str, dict[str, float | None]] = {"model": {}, "gross_margin": {}, "overhead": {}, "log_rpp": {}}
    info: dict[str, dict] = {}
    for t, b in base.items():
        rev = float(b["revenue_m"])
        om = float(b["operating_margin"])
        if b["gross_margin"] != "":
            gm: float | None = float(b["gross_margin"])
        elif t in DERIVED_COST:
            gm = 1 - DERIVED_COST[t] / rev
        else:
            gm = None
        rpp_usd = float(b["rpp_k"]) * FX_2023[b["currency"]]
        raw["model"][t] = MODEL_VALUE[b["model"]]
        raw["gross_margin"][t] = gm
        raw["overhead"][t] = None if gm is None else gm - om
        raw["log_rpp"][t] = math.log(rpp_usd)
        lr = last[t]
        years = max(int(lr["midpoint"][:4]) - 2023, 1)
        rpp_growth = (float(lr["rpp_k"]) / float(b["rpp_k"])) ** (1 / years) - 1
        info[t] = {
            "ticker": t, "name": NAMES[t], "model": b["model"], "base_fy_end": b["fy_end"],
            "last_fy_end": lr["fy_end"], "years": years,
            "gross_margin_base": None if gm is None else round(gm * 100, 1),
            "op_margin_base": round(om * 100, 1),
            "op_margin_last": round(float(lr["operating_margin"]) * 100, 1),
            "overhead_base": None if gm is None else round((gm - om) * 100, 1),
            "rpp_usd_k_base": round(rpp_usd, 1),
            "headcount_change_pct": round((float(lr["avg_headcount"]) / float(b["avg_headcount"]) - 1) * 100, 1),
            "rpp_growth_pct_yr": round(rpp_growth * 100, 1),
        }
        info[t]["margin_change_pt_yr"] = round((info[t]["op_margin_last"] - info[t]["op_margin_base"]) / years, 2)

    scaled = {k: scale(v) for k, v in raw.items()}
    for t in info:
        parts = {k: scaled[k][t] for k in scaled}
        known = [v for v in parts.values() if v is not None]
        info[t]["score"] = round(100 * sum(known) / len(known), 1)
        info[t]["components_used"] = len(known)
        for k, v in parts.items():
            info[t][f"c_{k}"] = None if v is None else round(v * 100, 1)

    ranked = sorted(info.values(), key=lambda d: -d["score"])
    with (HERE / "score.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(ranked[0]))
        w.writeheader()
        w.writerows(ranked)

    x = np.array([d["score"] for d in ranked])
    y = np.array([d["margin_change_pt_yr"] for d in ranked])
    slope, intercept = np.polyfit(x, y, 1)
    resid = y - (intercept + slope * x)
    se = math.sqrt((resid @ resid) / (len(x) - 2) / ((x - x.mean()) @ (x - x.mean())))
    pearson = float(np.corrcoef(x, y)[0, 1])
    rank = lambda a: np.argsort(np.argsort(a))  # noqa: E731
    spearman = float(np.corrcoef(rank(x), rank(y))[0, 1])
    # Leave-one-out check: correlation without each company in turn.
    loo = [float(np.corrcoef(np.delete(x, i), np.delete(y, i))[0, 1]) for i in range(len(x))]
    # Inside the product group only: does the score still sort the companies?
    prod = [d for d in ranked if d["model"] == "product"]
    prod_r = float(np.corrcoef([d["score"] for d in prod], [d["margin_change_pt_yr"] for d in prod])[0, 1])
    stats = {
        "n": len(x), "pearson": round(pearson, 2), "spearman": round(spearman, 2),
        "slope_pt_per_10_score": round(slope * 10, 2), "slope_se_per_10": round(se * 10, 2),
        "intercept": round(intercept, 2), "loo_min": round(min(loo), 2), "loo_max": round(max(loo), 2),
        "product_only_pearson": round(prod_r, 2), "product_n": len(prod),
    }
    (HERE / "results.json").write_text(json.dumps({"companies": ranked, "stats": stats}, indent=2), encoding="utf-8")

    print(f"{'company':11} {'model':12} {'score':>5} {'GM':>5} {'OH':>5} {'rpp$k':>6} {'OM23':>5} {'OMlast':>6} {'dOM/yr':>6} {'rpp/yr':>6}")
    for d in ranked:
        print(f"{d['name']:11} {d['model']:12} {d['score']:5.1f} {str(d['gross_margin_base']):>5} {str(d['overhead_base']):>5} "
              f"{d['rpp_usd_k_base']:6.0f} {d['op_margin_base']:5.1f} {d['op_margin_last']:6.1f} {d['margin_change_pt_yr']:+6.2f} {d['rpp_growth_pct_yr']:+6.1f}")
    print(stats)
    return 0


if __name__ == "__main__":
    sys.exit(main())
