"""
Fetch annual revenue, cost of revenue and operating income from SEC XBRL company facts.

Output: financials.csv (one row per company and fiscal year end).
Raw JSON goes to a local folder, not to the repository.

Usage:
    python fetch_sec.py <raw_dir>
"""

import csv
import json
import sys
import time
import urllib.request
from datetime import date
from pathlib import Path

HERE: Path = Path(__file__).resolve().parent
OUT: Path = HERE / "financials.csv"
AGENT: str = "ai-productivity-research admin@example.org"

# ticker: (CIK, business model)
COMPANIES: dict[str, tuple[int, str]] = {
    "EPAM": (1352010, "vendor_time"),
    "CTSH": (1058290, "vendor_time"),
    "INFY": (1067491, "vendor_time"),
    "WIT": (1123799, "vendor_time"),
    "GLOB": (1557860, "vendor_time"),
    "DAVA": (1656081, "vendor_time"),
    "ACN": (1467373, "vendor_fixed"),
    "SAP": (1000184, "product"),
    "EXPE": (1324424, "product"),
    "ADBE": (796343, "product"),
    "INTU": (896878, "product"),
    "BKNG": (1075531, "product"),
    "CRM": (1108524, "product"),
    "NOW": (1373715, "product"),
    "WDAY": (1327811, "product"),
    "ABNB": (1559720, "product"),
}

CONCEPTS: dict[str, list[tuple[str, str]]] = {
    "revenue": [
        ("us-gaap", "RevenueFromContractWithCustomerExcludingAssessedTax"),
        ("us-gaap", "Revenues"),
        ("us-gaap", "SalesRevenueNet"),
        ("us-gaap", "RevenueFromContractWithCustomerIncludingAssessedTax"),
        ("ifrs-full", "Revenue"),
        ("ifrs-full", "RevenueFromContractsWithCustomers"),
    ],
    "cost_of_revenue": [
        ("us-gaap", "CostOfRevenue"),
        ("us-gaap", "CostOfGoodsAndServicesSold"),
        ("us-gaap", "CostOfServices"),
        ("us-gaap", "CostOfGoodsAndServiceExcludingDepreciationDepletionAndAmortization"),
        ("ifrs-full", "CostOfSales"),
    ],
    "operating_income": [
        ("us-gaap", "OperatingIncomeLoss"),
        ("ifrs-full", "ProfitLossFromOperatingActivities"),
    ],
}
ANNUAL_FORMS: set[str] = {"10-K", "20-F", "40-F", "10-K/A", "20-F/A"}


def fetch(cik: int, raw_dir: Path) -> dict:
    """Return company facts JSON (cached in raw_dir)."""
    path = raw_dir / f"CIK{cik:010d}.json"
    if not path.exists():
        req = urllib.request.Request(
            f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json",
            headers={"User-Agent": AGENT},
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            path.write_bytes(resp.read())
        time.sleep(0.3)
    return json.loads(path.read_text(encoding="utf-8"))


def annual_values(facts: dict, options: list[tuple[str, str]]) -> dict[str, tuple[float, str, str]]:
    """Return {period end: (value, unit, concept)} for full-year values, latest filing first.

    Concepts earlier in the list win. A value counts as annual if the period is 350-380 days.
    """
    out: dict[str, tuple[float, str, str]] = {}
    for taxonomy, name in options:
        concept = facts.get("facts", {}).get(taxonomy, {}).get(name)
        if not concept:
            continue
        for unit, rows in concept["units"].items():
            best: dict[str, tuple[str, float]] = {}
            for r in rows:
                if r.get("form") not in ANNUAL_FORMS or "start" not in r:
                    continue
                days = (date.fromisoformat(r["end"]) - date.fromisoformat(r["start"])).days
                if not 350 <= days <= 380:
                    continue
                if r["end"] not in best or r["filed"] > best[r["end"]][0]:
                    best[r["end"]] = (r["filed"], float(r["val"]))
            for end, (_, val) in best.items():
                out.setdefault(end, (val, unit, f"{taxonomy}:{name}"))
    return out


def main() -> int:
    raw_dir = Path(sys.argv[1])
    raw_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []
    for ticker, (cik, model) in COMPANIES.items():
        facts = fetch(cik, raw_dir)
        data = {k: annual_values(facts, v) for k, v in CONCEPTS.items()}
        for end in sorted(data["revenue"]):
            if end < "2017-06-01":
                continue
            rev, unit, concept = data["revenue"][end]
            cost = data["cost_of_revenue"].get(end, (None, "", ""))[0]
            opinc = data["operating_income"].get(end, (None, "", ""))[0]
            rows.append({
                "ticker": ticker, "model": model, "fy_end": end, "currency": unit,
                "revenue_m": round(rev / 1e6, 1),
                "cost_of_revenue_m": round(cost / 1e6, 1) if cost is not None else "",
                "operating_income_m": round(opinc / 1e6, 1) if opinc is not None else "",
                "revenue_concept": concept,
            })
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} rows -> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
