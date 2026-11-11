# Panel: AI period and revenue per person, 16 companies, 2017–2026

Data and code for the study "Who Keeps the AI Gain?" (folder `../ai-margin-potential`). Date: November 2026.

## Question

Does the AI period (fiscal years with midpoint from 2024 on) change revenue per person and operating margin differently for:
- **vendor_time:** IT services vendors paid mostly for time (EPAM, Cognizant, Infosys, Wipro, Globant, Endava);
- **vendor_fixed:** a vendor with mostly fixed-price work (Accenture, the only one with SEC data);
- **product:** companies that sell a product (SAP, Expedia, Adobe, Intuit, Booking, Salesforce, ServiceNow, Workday, Airbnb)?

The hypothesis (from the study "Where Did the AI Productivity Go?", folder `../ai-services-study`) predicts: after 2024, revenue per person and margin grow faster at product companies than at time-billing vendors, because vendors pass the AI gain to clients.

## Data

| File | Content | Source |
|---|---|---|
| `financials.csv` | Annual revenue, cost of revenue, operating income, 2017–2026 | SEC XBRL company facts (10-K, 20-F), by `fetch_sec.py` |
| `financials_manual.csv` | Infosys and Wipro FY2026 revenue (not yet in XBRL) | press reports, 2 sources each |
| `headcount.csv` | Year-end or average headcount | SEC XBRL (SAP, Endava average employees); stockanalysis.com and macrotrends.net (cite filings) for the others |
| `panel.csv` | One row per company and fiscal year, with growth rates | `build_panel.py` |

Revenue per person = annual revenue ÷ average headcount (start and end of the fiscal year, or the reported average). Local currency (USD; EUR for SAP; INR for Wipro; GBP for Endava). Growth = log change per year.

Excluded: fiscal years with midpoint in 2020–2021 (COVID); 2022 for the 3 travel companies (travel recovery). Result: 77 company-years for the main model.

## Method

1. **Model A:** company fixed effects + hiring cycle (headcount growth this year and last year) + one AI-period term per business model.
2. **Model B (difference-in-differences):** company fixed effects + year fixed effects + hiring cycle + AI-period terms for vendor_fixed and product. The year effects remove everything that is common to all companies in a year: demand, inflation, interest rates, and also an AI effect that is the same for all. The terms measure the difference against time-billing vendors.
3. **Model C:** Model B for the yearly change of GAAP operating margin.

Standard errors are clustered by company (16 clusters).

## Results

### Revenue per person, change of yearly growth in the AI period

| Term | Model A (vs own past) | Model B (vs time-billing vendors) |
|---|---|---|
| Time-billing vendors | +3.0 pt/yr (SE 3.0) | reference |
| Accenture | +2.8 pt/yr (one company) | −2.2 pt/yr (one company) |
| Product companies | +3.7 pt/yr (SE 1.9) | **+0.0 pt/yr (SE 2.6)** |
| Headcount growth (hiring cycle) | −0.12 (SE 0.17) | −0.14 (SE 0.23) |

### Operating margin, change per year

| Group | Before 2024 | AI period | Model C (vs time-billing vendors) |
|---|---|---|---|
| Time-billing vendors | −1.5 pt/yr | +0.2 pt/yr | reference |
| Accenture | −0.3 pt/yr | +0.6 pt/yr | −0.7 pt/yr (SE 1.1) |
| Product companies | −0.1 pt/yr | **+2.5 pt/yr** | **+1.2 pt/yr (SE 1.3)** |

### Revenue growth ÷ headcount growth (the "decoupling" indicator)

Before 2024, most companies needed about 1% more people for 1–1.5% more revenue. In the AI period, revenue grew while headcount fell or stayed flat at Cognizant, Infosys, Wipro, Endava and Expedia (negative ratio), and the ratio rose strongly at SAP, Adobe, Intuit, Salesforce and Booking. It rose a little at Globant, Workday, ServiceNow and Accenture (1.0 → 1.6). It did not change at EPAM (1.5 → 1.5) and fell at Airbnb (2.9 → 1.7).

## What the panel shows

1. **Revenue per person grew faster after 2024 in all 3 groups, by about 3 points per year.** The change is the same for vendors and product companies (Model B: +0.0, SE 2.6). With annual data to 2025, the panel does not support the hypothesis on revenue per person.
2. **Margins point in the direction of the hypothesis, but not significantly.** Product companies increased their operating margin by 2.5 points per year in the AI period; time-billing vendors by 0.2. The difference after year effects is +1.2 points per year with SE 1.3.
3. **The hiring cycle explains little in annual data.** The headcount coefficients are small and not significant. The common jump after 2024 is a year effect: it is the same for all business models.
4. **Revenue and headcount separated after 2024 in both groups.** This is the clearest common signal. It agrees with an AI effect for all companies, and also with the end of the 2021–2022 hiring boom (fewer new people while old contracts continue).

## Why the panel and the quarterly study differ

The study "Where Did the AI Productivity Go?" compares Q3 2024 with Q3 2026. It shows almost no gain at EPAM, Infosys and Cognizant. The panel uses fiscal years and ends mostly in 2025, so it does not see the 2026 slowdown. Its "before" period also contains the weak years 2022–2023, when vendor revenue per person fell. Both views are correct for their periods. The difference shows how much the result depends on the period.

## Prediction for 2027–2028 (scenarios)

The panel cannot give one number. It gives a range:

| Scenario | Revenue per person, all companies | Operating margin |
|---|---|---|
| Slow (the 2024–2025 jump was the end of the hiring boom) | back to the pre-2024 trend (vendors 0–2%, products 3–4% per year) | vendors flat, products +0–1 pt/yr |
| Base (the jump continues) | about 3 points per year above the old trend | vendors flat to +0.5 pt/yr, products +1–2.5 pt/yr |
| Fast (AI share of work grows from 20% to 60%, speed-up 1.3) | the study formula 1/((1−s)+s/m) gives +5% (s = 20%) → +10% (40%) → +16% (60%): about 5 points per year | under the hypothesis: vendors pass it to clients (flat margin, lower price); products keep it |

The decisive data for the choice between the scenarios:
- **FY2026 annual reports** (Dec 2026 year ends, published Feb–Mar 2027). They show if the vendor slowdown in the 2026 quarters continues.
- **Margin difference** between product companies and vendors. If it stays above 1 point per year for 2 more years, it becomes significant and supports the hypothesis.
- **Utilization and price per hour** (Infosys, Wipro, TCS, HCL publish them every quarter). They separate the hiring cycle from lower prices.

## Limits

1. **Few years after 2024:** 1–3 per company. Standard errors are 2–3 points per year, so the panel can find only large effects.
2. **One fixed-price vendor.** Accenture alone cannot represent the group. CGI and Capgemini do not file XBRL data with the SEC.
3. **Headcount from secondary sources** for 14 of 16 companies (stockanalysis.com, macrotrends.net). Wipro, Salesforce (before 2021) and Workday numbers are rounded. The sources cite the filings; they were not checked one by one.
4. **GAAP operating margin** includes restructuring costs (SAP 2024, Endava, Accenture), which add noise.
5. **Local currency:** INR and EUR revenue moves with exchange rates differently than USD revenue.
6. **Business model is a label, not a measure.** Some vendors have fixed-price work, and some product companies have services.
7. **Two manual values** (Infosys and Wipro FY2026 revenue) come from press reports, not from the 20-F.
8. The panel shows correlation by business model, not cause.

## How to run

Python 3.10 or later with numpy.

```bash
python fetch_sec.py <folder for raw SEC JSON>
python build_panel.py
```

The SEC asks automated clients to send a User-Agent with a contact. Set your own contact in `AGENT` in `fetch_sec.py` before you run it.
