# Who Keeps the AI Gain? A Margin-Potential Score for 16 Software and IT Services Companies

Serhii Korsunenko, independent researcher, Aachen, Germany. Working paper, November 2026.

## Summary

Generative AI tools came into daily use in 2024, and many reports say that they make knowledge work much faster. This working paper asks who keeps that gain. It tests one hypothesis: when software becomes faster to make, a vendor that bills for time gives the gain to its clients as more work for the same money. A company that sells a product keeps the gain.

This paper tests the hypothesis on a panel of 16 listed companies from 2017 to 2026: 7 IT services vendors and 9 product companies (software and online marketplaces). All financial data come from SEC filings in XBRL format. Headcount comes from the filings and from public data sites that cite them.

The results:
- **Revenue per person grew faster after 2024 in all groups.** Product companies changed from 4.4% to 7.9% per year, and time-billing vendors from 2.9% to 4.4%. After year effects are removed, the AI-period change is the same for both groups: 0.0 points per year (standard error 2.6). Revenue per person alone does not support the hypothesis.
- **Operating margin separates the groups.** In the AI period, product companies increased their operating margin by 2.5 points per year, and time-billing vendors by 0.2 points. After year effects, the difference is 1.2 points per year (standard error 1.3), so it is not yet significant.
- **A simple score finds the companies that kept the gain.** The score uses four values from 2023: revenue model, gross margin, overhead share and revenue per person. It correlates with the operating margin change after 2023 (r = 0.72, n = 16). But the business-model label alone (product or vendor) gives the same result (r = 0.75). The score separates product companies from vendors, but it cannot rank the companies inside the product group.

The companies with the highest potential to increase margin with AI sell a product, have a high gross margin and a large cost base in research, sales and administration, and do not bill for hours. Vendors that bill for time have the lowest potential. They can increase their margin mainly through lower overhead, fewer people or a change to fixed-price contracts.

The paper is for education. It does not recommend or judge any company, and it is not investment advice.

## Reader's guide

### The task

When AI tools make knowledge work faster, someone receives the gain: the company, its clients or its employees. The task of this paper is to find out who receives it, with numbers from public annual reports only. The paper does three steps:

1. It measures two values for 16 companies from 2017 to 2026: revenue per person and operating margin.
2. It compares the change after 2024 for companies that bill for time and companies that sell a product.
3. It makes a simple score from 2023 values and tests if the score finds the companies whose margin increased after 2023.

### Why we solve this problem

- **Claims and numbers do not agree.** In 2024–2026 many articles and AI companies said that AI makes knowledge work much faster. But the annual reports of large IT services companies show only small changes in revenue per person after 2024 (Korsunenko, 2026, gives the details for four of them). If the gain is real, it must go to some place. This paper looks for that place.
- **The answer is important for people who work in IT.** The contract type decides if a faster team earns more money or less money for its employer. At a vendor paid for time, a team that does a task in fewer hours bills fewer hours, unless it gets more work. At a product company, the same saving lowers the cost and the company keeps it.
- **The answer is important for companies that buy IT services.** If the vendor bills for time, the client can receive the gain as fewer hours. The client must ask for it.
- **The method is useful for any reader.** The paper shows how to test a media claim with public data and arithmetic. A reader can repeat each calculation with a calculator and one annual report.

### What we use

| Item | What this paper uses |
|---|---|
| Companies | 16 listed companies that file annual reports with the SEC (list in 2.1) |
| Financial data | SEC XBRL company facts: revenue, cost of revenue, operating income. No paid data. |
| Headcount | Annual reports, and two public data sites that cite the annual reports |
| Values not in XBRL | Two independent press sources for each value (Infosys and Wipro, fiscal 2026) |
| Period | Fiscal years 2017–2026; the AI period starts in 2024 |
| Calculations | Python 3.12 scripts: `fetch_sec.py` (download), `build_panel.py` (panel and models), `score.py` (score and test) |
| Statistics | Averages, growth rates, linear regression with company and year effects (difference-in-differences), Pearson and Spearman correlation, leave-one-out test |
| Output | This paper (PDF on SSRN) and the same text as a web page |

### How to read this paper

- If financial reports are new to you, read the **Glossary** at the end first.
- Section 3 gives each formula and a full calculation for SAP. You can repeat it with a calculator.
- "pt" means percentage points. A margin that changes from 10% to 12% changes by +2 pt (and by +20% in relative terms).
- "SE" is the standard error. An estimate that is less than about two standard errors from zero is not statistically significant.

## 1. Question

Generative AI tools for code, text and support came into daily use in 2024. If they make knowledge work faster, someone receives the gain: the company, its clients, or its employees. This paper asks two questions:

1. Did revenue per person and operating margin change after 2024 differently for companies that bill for time and companies that sell a product?
2. Which measurable properties of a company, known before the AI period, predict a higher margin in the AI period?

## 2. Data

### 2.1 Companies

| Group | Companies | How they earn revenue |
|---|---|---|
| Vendors, paid mostly for time | EPAM, Cognizant, Infosys, Wipro, Globant, Endava | Clients pay for people, days or hours |
| Vendor, mostly fixed price | Accenture (over 65% of bookings fixed price, company statement) | Clients pay for a result or a project |
| Product companies | SAP, Adobe, Intuit, Salesforce, ServiceNow, Workday (software); Booking, Expedia, Airbnb (online marketplaces) | Subscriptions, licenses, usage or transaction fees |

All 16 companies file annual reports with the US Securities and Exchange Commission (10-K or 20-F). Other large vendors (TCS, HCL, Capgemini, CGI) do not file XBRL data with the SEC, so this version does not include them.

### 2.2 Values and sources

| Value | Source |
|---|---|
| Revenue, cost of revenue, operating income | SEC XBRL company facts (annual 10-K and 20-F), fiscal years 2017–2026 |
| Infosys and Wipro revenue for fiscal year 2026 | Company results as reported by two press sources each (not yet in XBRL) |
| Headcount | SEC XBRL (SAP and Endava average employees); stockanalysis.com and macrotrends.net for the other 14 companies (these sites cite the annual reports) |
| Gross margin of Intuit and Workday | Calculated from the expense lines in the 10-K (no cost-of-revenue tag) |

The panel has 140 company-years. Each company uses its own fiscal year. A fiscal year belongs to the **AI period** if its midpoint is on or after 1 January 2024.

### 2.3 Exclusions

- Fiscal years with a midpoint in 2020 or 2021 (COVID).
- 2022 for Booking, Expedia and Airbnb (travel recovery after COVID).

After the exclusions, 77 company-years have a growth rate and a lagged headcount growth rate.

## 3. Method

### 3.1 Measures

All formulas are applied to each company and fiscal year.

| Measure | Formula |
|---|---|
| Average headcount | (headcount at the start of the year + headcount at the end of the year) ÷ 2, or the reported average |
| Revenue per person | revenue ÷ average headcount |
| Growth of revenue per person | ln(revenue per person this year ÷ revenue per person last year) |
| Headcount growth | ln(average headcount this year ÷ average headcount last year) |
| Gross margin | 1 − cost of revenue ÷ revenue |
| Operating margin | operating income ÷ revenue (GAAP or IFRS, as reported) |
| Overhead share | gross margin − operating margin (research, sales, general and administrative costs as a share of revenue) |

Revenue per person is in the company's reporting currency (USD; EUR for SAP; INR for Wipro; GBP for Endava). For the score, it is converted to USD with fixed 2023 average rates (EUR 1.08, GBP 1.24, INR 82.6 per USD).

### 3.2 Panel models

**Model A (each group against its own past).** Growth of revenue per person = company effect + b1 × headcount growth + b2 × headcount growth last year + d × (AI period × group). The headcount terms remove the hiring cycle: new people are not productive at once, and fewer people can produce the same revenue for some time.

**Model B (difference-in-differences).** Model A plus one effect for each calendar year. Year effects remove everything that is the same for all companies in a year: demand, inflation, interest rates, and an AI effect that is equal for all. The AI-period terms then measure the difference between product companies (or Accenture) and time-billing vendors.

**Model C.** Model B with the yearly change of operating margin (in points) as the result.

Standard errors are clustered by company (16 clusters).

### 3.3 The AI margin-potential score

The score uses only values from the base year (the fiscal year with a midpoint in 2023), before the AI period. Each component is scaled from 0 (lowest company) to 1 (highest company):

| Component | Value | Why it can predict an AI margin gain |
|---|---|---|
| 1. Revenue model | time-billing vendor = 0; fixed-price vendor = 0.5; product = 1 | If a client pays for hours, faster work reduces revenue. If a client pays for a product or a result, faster work reduces cost. |
| 2. Gross margin | 1 − cost of revenue ÷ revenue | A high gross margin means the main costs are not in billed delivery. |
| 3. Overhead share | gross margin − operating margin | Research, sales, support and administration are knowledge work that AI tools can make faster. The company keeps this saving. |
| 4. Revenue per person | ln(revenue per person in USD) | High revenue per person means revenue does not grow with headcount. |

Score = 100 × (average of the available components).

Booking has no cost-of-revenue line, so its score uses only components 1 and 4.

**Example: SAP.** Revenue model: product, so 1.00. Gross margin 72.2%; the range is 24.3% (Endava) to 87.9% (Adobe), so (72.2 − 24.3) ÷ (87.9 − 24.3) = 0.75. Overhead share 53.6%; the range is 9.4% (Infosys) to 79.7% (Expedia), so (53.6 − 9.4) ÷ (79.7 − 9.4) = 0.63. Revenue per person $318k; the range is $45k (Wipro) to $1,446k (Airbnb), so (ln 318 − ln 45) ÷ (ln 1,446 − ln 45) = 0.56. Score = 100 × (1.00 + 0.75 + 0.63 + 0.56) ÷ 4 = 73.6.

**Test.** The result is the operating margin change per year from the base year to the latest fiscal year: (operating margin latest − operating margin base) ÷ number of years. The test is the correlation between the score and this change, and a straight-line fit.

## 4. Results

### 4.1 Revenue per person

| Group | Companies | Before 2024, per year | AI period, per year | Change |
|---|---|---|---|---|
| Vendors paid for time | 6 | +2.9% | +4.4% | +1.5 pt |
| Accenture (fixed price) | 1 | +0.1% | +1.8% | +1.7 pt |
| Product companies | 9 | +4.4% | +7.9% | +3.5 pt |

Average of company averages. Before 2024 = fiscal years 2017–2019 and 2022–2023 (with the exclusions in 2.3).

| Model term | Model A: change against own past | Model B: difference against time-billing vendors |
|---|---|---|
| AI period × vendors paid for time | +3.0 pt/yr (SE 3.0) | reference |
| AI period × Accenture | +2.8 pt/yr (one company) | −2.2 pt/yr (one company) |
| AI period × product companies | +3.7 pt/yr (SE 1.9) | **+0.0 pt/yr (SE 2.6)** |
| Headcount growth | −0.12 (SE 0.17) | −0.14 (SE 0.23) |
| Headcount growth last year | +0.09 (SE 0.15) | +0.13 (SE 0.16) |

Model A without the headcount terms gives almost the same AI-period values (vendors +2.5 pt, product companies +3.9 pt). The hiring cycle explains little in annual data.

**Reading.** Revenue per person grew faster after 2024 in both groups. Model B shows that the difference between the groups is zero. On revenue per person, the panel does not support the hypothesis. A common change in all companies can come from AI that helps every company, or from the end of the hiring boom of 2021–2022.

### 4.2 Operating margin

| Group | Before 2024, change per year | AI period, change per year |
|---|---|---|
| Vendors paid for time | −1.5 pt | +0.2 pt |
| Accenture | −0.3 pt | +0.6 pt |
| Product companies | −0.1 pt | **+2.5 pt** |

Model C (difference against time-billing vendors, with company and year effects): product companies +1.2 points per year (SE 1.3); Accenture −0.7 points per year (SE 1.1, one company).

**Reading.** In simple averages, product companies increased their margin by 2.5 points per year and time-billing vendors by 0.2 points. After company and year effects, the difference is smaller: 1.2 points per year, with a standard error of 1.3. The direction agrees with the hypothesis: the product company keeps the saving, and the vendor passes it on. But with 1–3 years of AI-period data, the difference is not statistically significant, and it can still be zero.

### 4.3 The score and the margin change

| Rank | Company | Group | Gross margin 2023 | Overhead share 2023 | Revenue per person 2023 | Score | Operating margin 2023 → latest | Change per year |
|---|---|---|---|---|---|---|---|---|
| 1 | Expedia | Product | 87.8% | 79.7% | $764k | 95.4 | 8.1% → 12.7% | +2.30 pt |
| 2 | Booking | Product | n/a | n/a | $945k | 93.9 | 27.3% → 32.8% | +2.75 pt |
| 3 | Airbnb | Product | 82.8% | 67.5% | $1,446k | 93.7 | 15.3% → 20.8% | +2.75 pt |
| 4 | Adobe | Product | 87.9% | 53.6% | $656k | 85.0 | 34.3% → 36.6% | +1.15 pt |
| 5 | ServiceNow | Product | 78.6% | 70.1% | $416k | 84.0 | 8.5% → 13.7% | +2.60 pt |
| 6 | Workday | Product | 75.6% | 73.1% | $398k | 83.5 | 2.5% → 7.5% | +2.50 pt |
| 7 | Intuit | Product | 74.8% | 52.9% | $810k | 81.1 | 21.9% → 27.4% | +1.83 pt |
| 8 | Salesforce | Product | 75.5% | 61.1% | $458k | 80.2 | 14.4% → 20.1% | +2.85 pt |
| 9 | SAP | Product | 72.2% | 53.6% | $318k | 73.6 | 18.6% → 26.1% | +3.75 pt |
| 10 | Accenture | Vendor, fixed price | 32.3% | 18.6% | $88k | 23.8 | 13.7% → 15.4% | +0.57 pt |
| 11 | Globant | Vendor, time | 36.1% | 26.6% | $74k | 14.3 | 9.5% → 7.0% | −1.25 pt |
| 12 | EPAM | Vendor, time | 30.6% | 19.9% | $83k | 10.6 | 10.7% → 9.5% | −0.60 pt |
| 13 | Cognizant | Vendor, time | 34.6% | 20.7% | $55k | 9.5 | 13.9% → 16.1% | +1.10 pt |
| 14 | Endava | Vendor, time | 24.3% | 21.6% | $78k | 8.3 | 2.7% → 4.1% | +1.40 pt |
| 15 | Infosys | Vendor, time | 30.1% | 9.4% | $56k | 3.9 | 20.7% → 21.1% | +0.40 pt |
| 16 | Wipro | Vendor, time | 29.6% | 14.5% | $45k | 3.9 | 15.2% → 17.0% | +1.80 pt |

"Latest" is the last fiscal year with an operating margin in XBRL (fiscal 2025 for most companies; 2026 for Accenture, Intuit, Salesforce and Workday). GAAP or IFRS operating margin, so restructuring costs are included.

| Test | Value |
|---|---|
| Correlation (Pearson), score and margin change per year | **0.72** (n = 16) |
| Rank correlation (Spearman) | 0.56 |
| Slope | +0.25 points per year of margin change for each 10 points of score (SE 0.06) |
| Correlation without one company (lowest / highest of 16 runs) | 0.69 / 0.77 |
| Correlation inside the product group only | −0.26 (n = 9) |
| Correlation inside the vendor group only (7 vendors) | −0.36 (n = 7) |
| Business-model label alone (product = 1, fixed price = 0.5, time = 0) | 0.75 |
| Score without the label (components 2–4 only) | 0.69 |

**Reading.**
1. The score separates the groups well: every product company has a score above 73 and a margin gain of at least 1.15 points per year; every vendor has a score below 24 and a margin change of at most 1.8 points per year.
2. No single company makes the result: without any one company, the correlation stays between 0.69 and 0.77.
3. Inside the product group, the score does not predict the order. SAP has the lowest product score and the largest margin gain. Part of the SAP gain is a return to its earlier level: its operating margin was 20–24% in 2017–2022, 18.6% in 2023, 13.7% in 2024 (restructuring costs) and 26.1% in 2025. Adobe has a high score and the smallest product gain: it already had the highest margin, and AI image tools compete with its products.
4. **The score does not add information to the business-model label.** The label alone gives a correlation of 0.75, and the three financial values without the label give 0.69. In this sample, high gross margin, high overhead share and high revenue per person are simply the properties of product companies. The score is a way to measure "how much of a product company" a company is from its numbers, not a better predictor than the label.
5. Margin gains at product companies did not need fewer people. ServiceNow increased its headcount by about 29% and its operating margin by 2.6 points per year. At vendors, the margin increased mainly where headcount went down (Wipro, Cognizant, Infosys) and went down where headcount increased (EPAM, Globant).

## 5. Which companies can increase their margin with AI

The data agree with this profile of high potential:

1. **The company sells a product or a result, not hours.** A saving in time becomes a saving in cost, not a loss of revenue.
2. **Most costs are knowledge work in overhead,** not in billed delivery: research and development, sales, customer support, finance and administration. These are the tasks that AI tools make faster today.
3. **Revenue does not grow with headcount** (high revenue per person, subscription or transaction fees).
4. **The price is protected** by a platform, data, a network or switching costs. Where AI makes a product easier to copy, competition can move the gain to customers (Adobe is a possible example).

Low potential:
- **Vendors paid for time** (IT services, staffing, outsourcing of business processes). The gain goes to the client as fewer billed hours, lower prices or more work for the same budget.
- **Products that AI can replace or copy.**
- **Software priced per user,** if clients need fewer users because of AI. This risk is not yet visible in the data to 2026.

A vendor can move up the score: more fixed-price and outcome-based contracts, own platforms and intellectual property, and lower overhead. Accenture and Cognizant show the last path: their margin gains after 2024 come from lower selling, general and administrative costs, while their gross margins fell.

## 6. Prediction for 2027–2028

The panel gives a range, not one value.

| Scenario | Revenue per person | Operating margin, product companies | Operating margin, vendors paid for time |
|---|---|---|---|
| Slow: the 2024–2025 change was the end of the hiring boom | back to the trend before 2024 (vendors about 3%, products about 4% per year) | +0.5 pt per year (range 0 to +1) | 0 pt per year |
| Base: the 2024–2025 change continues | about 3 points per year above the trend before 2024, in all groups | +1.75 pt per year (range +1 to +2.5) | +0.25 pt per year (range 0 to +0.5) |
| Fast: AI does a larger share of the work | with the formula 1 ÷ ((1 − s) + s ÷ m), speed-up m = 1.3 and AI share s = 20%, 40%, 60%: +5%, +10%, +16% total effect | +2.5 pt per year (the AI-period rate continues) | −0.5 pt per year (vendors pass the gain to clients, and clients ask for lower prices) |

**How the forecast chart is made.** The group value is the simple average of the operating margins of the companies in the group. The year is the calendar year of the fiscal-year midpoint. Each line starts at the last year with data for all companies in the group: 2025 for product companies (21.8%, 9 of 9 companies) and 2024 for vendors paid for time (12.9%, 6 of 6 companies). Each scenario adds its rate from the table for each year to 2028:

| Group | Last actual value | Slow, 2028 | Base, 2028 | Fast, 2028 |
|---|---|---|---|---|
| Product companies | 21.8% (2025) | 21.8 + 3 × 0.5 = 23.3% | 21.8 + 3 × 1.75 = 27.1% | 21.8 + 3 × 2.5 = 29.3% |
| Vendors paid for time | 12.9% (2024) | 12.9 + 4 × 0 = 12.9% | 12.9 + 4 × 0.25 = 13.9% | 12.9 − 4 × 0.5 = 10.9% |

These lines are arithmetic from the scenario rates. They are not a statistical forecast, and the real path will not be a straight line.

With the base scenario and the score slope (0.25 pt per year for 10 score points, so 0.025 pt per year for 1 score point), a company with a score of 90 can expect about 2 points (80 × 0.025) of operating margin per year more than a company with a score of 10. This is an in-sample estimate from 16 companies, not a forecast for one company.

## 7. Limits

1. **Short AI period.** Each company has 1–3 fiscal years after 2024. Standard errors are 1–3 points per year. The panel can only find large effects.
2. **The score was designed after the author saw the data.** The components are reasonable, but the selection was not fixed in advance. The fiscal 2026 and 2027 reports are the first true test (out of sample). The formula is now fixed in this paper (November 2026) and will not change for that test.
3. **The score is close to the business-model label** (section 4.3, point 4). It does not yet show that the financial values predict more than the label.
4. **One fixed-price vendor.** Accenture alone cannot represent a group.
5. **Headcount from secondary sources** for 14 of 16 companies. Some values are rounded (Wipro, Workday, Salesforce before 2021). The sources cite the annual reports, but the author did not check every value against the original report.
6. **GAAP and IFRS margins include one-time costs**, for example restructuring at SAP (2024), Endava and Accenture.
7. **Currency.** Revenue per person for SAP, Wipro and Endava is in EUR, INR and GBP. The growth rates include currency effects.
8. **Business model is a label.** Vendors have some fixed-price work, and product companies have some services.
9. **Other causes after 2023.** Many companies cut costs in 2023–2024 for reasons that are not AI: higher interest rates and pressure from investors after the hiring boom. The panel cannot separate these causes from AI.
10. **Correlation, not cause.** The paper shows which companies increased their margin in the AI period, not that AI caused the increase.

## 8. What to watch

1. **Fiscal 2026 annual reports** (published from February 2027): the first out-of-sample test of the score.
2. **The margin difference between product companies and vendors.** If it stays above 1 point per year for two more years, it becomes statistically significant.
3. **Utilization and price per hour** at vendors (Infosys, Wipro, TCS and HCL publish them each quarter). They separate the hiring cycle from lower prices.
4. **Seat counts at software companies priced per user.**
5. **Share of fixed-price and outcome-based revenue** at vendors.

## FAQ

This section answers questions that a reader new to financial reports and statistics can have about the method and the results.

**1. Product companies changed from 4.4% to 7.9% per year, and vendors from 2.9% to 4.4%. How can the difference be 0.0?**
Do the difference-in-differences with the two group averages first:

| Step | Product companies | Vendors paid for time | Difference |
|---|---|---|---|
| Before 2024, per year | 4.4% | 2.9% | |
| AI period, per year | 7.9% | 4.4% | |
| Change | +3.5 pt | +1.5 pt | **+2.0 pt** (simple DiD) |
| Model A: company effects and hiring cycle | +3.7 pt | +3.0 pt | +0.7 pt |
| Model B: also year effects | | | **+0.0 pt** (SE 2.6) |

The simple averages compare different calendar years: the fiscal years of the companies end in different months, and each company has a different number of years in each period. Model B compares companies only inside the same calendar year, and it removes the hiring cycle. The standard error is 2.6 points, so +2.0, +0.7 and 0.0 are all inside the uncertainty. The correct reading is: the data do not show a difference in revenue per person between the groups.

**2. How do you get from 140 company-years to 77?**
140 rows (16 companies, up to 10 years). A growth rate needs the year before, so the first year of each company has none: 124 rows. The lagged headcount growth (growth in the year before) needs one more year: 108 rows. The exclusions in 2.3 remove 31 rows: 77 rows.

**3. Why remove 2020–2021 but keep 2022, the hiring boom?**
In 2020–2021 revenue and headcount moved for reasons that are not normal business (lockdowns, then a sudden recovery). The hiring boom of 2021–2022 is in the headcount terms of the models: they remove the part of revenue per person growth that comes from fast or slow hiring. Travel companies are also removed in 2022, because travel revenue was still recovering in that year.

**4. Why trust headcount from stockanalysis.com and macrotrends.net?**
These sites copy the headcount from the annual reports, and the author compared some values with the reports. But it is a weakness (limit 5). It is important to know which results use headcount: revenue per person and the score component 4 use it. The operating margin results and score components 1–3 do not use headcount at all.

**5. What are "bookings"? Was Accenture fixed price already in 2023?**
Bookings are the value of new contracts that a company signs in a period. They are not revenue: revenue comes later, when the work is done. The 65% value comes from 2026. The author assumes that the share was similar in 2023. If Accenture gets the label 0 (time vendor) instead of 0.5, its score changes from 23.8 to 11.2, and the correlation stays at 0.72.

**6. What are b1, b2 and d in Model A?**
They are coefficients: numbers that the regression calculates. b1 shows how much revenue per person growth changes when headcount growth is 1 point higher; b2 does the same for the year before. d is the AI-period effect. "AI period × group" is a multiplication of two values that are 0 or 1, so it is 1 only for a company of that group in an AI-period year.

**7. Why do all four score components have the same weight?**
Equal weights are the simplest choice, and they do not adjust the score to the result. Weights chosen to fit this small sample would make the score look better than it is.

**8. Is the score more than the label "product or vendor"?**
No, not in this sample. The label alone gives a correlation of 0.75, and the score gives 0.72. Section 4.3 now shows this. The score tells you from the numbers how much a company looks like a product company. This can help for a company that has no clear label, but this paper cannot yet show that the score predicts better than the label.

**9. Why use ln for revenue per person? Why does SAP get 73.6 and not 73.5?**
Revenue per person goes from $45k to $1,446k, a factor of 32. On a linear scale, all vendors get almost 0, and SAP gets 0.19. The logarithm makes "two times more" the same step at every level. The worked example rounds each component to two decimals; the script uses all decimals (75.4, 62.9 and 56.3 on the 0–100 scale), so the result is 73.6.

**10. Booking has only two components. Is its score of 93.9 fair?**
Possibly not. If its missing components were equal to the lowest values in the product group, its score would be 81.2, and its rank would be lower. This does not change the separation of the groups.

**11. Why is a high overhead good?**
It is not good in itself. A high overhead share means a large cost base that AI tools can make cheaper: research, sales, support and administration. A company with a small overhead has little to save.

**12. What does "reference" mean in Model B, and why does Accenture change from +2.8 to −2.2?**
In Model B each value is a difference against one group, the reference group: vendors paid for time. Accenture's −2.2 is Accenture's change minus the vendors' change, after year effects. With one company, this value is not reliable. Read it as "no clear difference".

**13. "More than 10 times faster" (2.5 against 0.2), but Model C gives 1.2 with SE 1.3. Which number is correct?**
Both numbers are correct calculations, but Model C is the better test, and its result is not significant. The phrase "10 times faster" made the result look stronger than it is, so the text in 4.2 is changed.

**14. SAP's restructuring was in 2024, but the base year is 2023. How can it change the base?**
It cannot. The first draft had this mistake. The restructuring lowered the 2024 margin, not the 2023 margin. The corrected text in 4.3 explains the SAP gain as a return to its earlier margin level. One-time costs stay in the margin because each company defines its adjusted margin differently, and XBRL gives only the official margin (limit 6).

**15. Why m = 1.3, and why +1.75 and +0.25 in the base scenario? Where does 0.025 come from?**
The scenario values are assumptions, not results. m = 1.3 means that the part of the work that AI helps becomes 30% faster; this is a moderate value for illustration. The base rates are the middle of the ranges: products +1 to +2.5 (2.5 is the observed AI-period rate), vendors 0 to +0.5. The slope is 0.25 points per 10 score points, so 0.025 points per 1 score point.

**16. If the score was designed after the data were seen, is r = 0.72 not automatic?**
Partly, yes. The group difference was known, so a score that separates the groups must correlate with the result. The paper publishes the formula now, so that the next annual reports can test it without changes (section 8).

**17. I will work in IT soon. Does this paper mean that my company earns less if I work faster with AI?**
The paper measures companies, not jobs. It shows that at a vendor paid for time, faster work does not automatically give more money to the vendor: the client can pay for fewer hours. Vendors increased their margin mainly where headcount went down. At product companies, margins increased while headcount often increased too. The paper does not show what happens to the job of one person.

**18. What is a "seat count", and can I see it in an annual report?**
A seat is one paid user license. If a client needs fewer employees because of AI, it can buy fewer seats. Most companies in this study do not report seat counts. Signs in the reports are slower subscription revenue growth and a lower net revenue retention rate (how much existing customers pay this year compared with last year), when the company reports it.

**19. What are a listed company and SSRN?**
They are now in the Glossary.

## Glossary

| Term or abbreviation | Meaning in this paper |
|---|---|
| 10-K | The annual report that a US company files with the SEC. |
| 20-F | The annual report that a non-US company with shares listed in the USA files with the SEC (for example SAP, Infosys, Wipro, Globant, Endava). |
| AI | Artificial intelligence. In this paper: generative AI tools that write code, text and answers, for example code assistants and chat assistants. |
| AI period | Fiscal years with a midpoint on or after 1 January 2024. |
| Average headcount | (people at the start of the year + people at the end of the year) ÷ 2. |
| Bookings | The value of new contracts that a company signs in a period. Revenue from these contracts comes later. |
| Base year | The fiscal year with a midpoint in 2023: the last year before the AI period. The score uses only base-year values. |
| Clustered standard errors | Standard errors that accept that the years of one company are not independent. They are larger and more honest than normal standard errors. |
| Coefficient | A number that a regression calculates: how much the result changes when one input changes by one unit. |
| Company effect (fixed effect) | One constant for each company in a model. It removes the differences between companies that do not change with time, for example a permanently higher margin. |
| Company-year | One row of data: one company in one fiscal year. |
| Correlation (Pearson, r) | A number from −1 to +1. It shows how well a straight line describes the relation between two values. 0 = no straight-line relation; +1 = all points are on a rising line. |
| Cost of revenue | The cost to deliver the product or service. At a vendor, this is mainly the salaries of the people who do billed work. |
| DiD (difference-in-differences) | Compare the change in one group with the change in a second group in the same period. A change that is the same for both groups cancels. |
| EUR, GBP, INR, USD | Euro, British pound, Indian rupee, US dollar. |
| Fiscal year (FY) | The 12-month reporting year of a company. It can end in a month that is not December, for example March (Infosys, Wipro), June (Endava), July (Intuit), August (Accenture) or January (Workday). |
| Fixed price | The client pays an agreed amount for a result or a project, not for hours. |
| GAAP, IFRS | The two sets of accounting rules: US Generally Accepted Accounting Principles and International Financial Reporting Standards. |
| Gross margin | 1 − cost of revenue ÷ revenue. The share of revenue that is left after the cost of delivery. |
| Hiring cycle | Companies hire many people in good years and few people in bad years. New people are not productive at once, so revenue per person goes down during a hiring boom and goes up in the years after it, when hiring stops. |
| In sample, out of sample | A test is in sample if it uses the same data that was used to make the method. It is out of sample if it uses new data. Only an out-of-sample test can show that a method predicts. |
| Lagged | From the year before. "Lagged headcount growth" is the headcount growth of the previous year. |
| Leave-one-out test | Calculate the result 16 times, each time without one company. If the result changes little, no single company makes the result. |
| Listed company | A company whose shares are traded on a stock exchange. It must publish its financial reports. |
| ln | Natural logarithm. For small changes, ln(new ÷ old) is almost equal to the percent change: ln(1.05) = 0.049, so about 5%. |
| Midpoint | The middle day of a fiscal year. It puts fiscal years that end in different months on one calendar. |
| Min-max scaling | (value − lowest value) ÷ (highest value − lowest value). The lowest company gets 0, the highest company gets 1. |
| n | The number of companies or observations in a calculation. |
| Operating income | Revenue minus all operating costs (cost of revenue, research, sales, administration). |
| Operating margin | Operating income ÷ revenue. The share of revenue that the company keeps from its main business. |
| Overhead share | Gross margin − operating margin. The costs of research, sales, support and administration as a share of revenue. |
| Panel | Data for the same companies for many years. |
| Product company | A company that sells software, a platform or a service on a platform, and earns subscription, license, usage or transaction fees. |
| pt, percentage point | The difference between two percentages. A margin that changes from 10% to 12% changes by +2 pt. |
| pt/yr | Percentage points per year. |
| R&D | Research and development. |
| Reference group | In Models B and C: the group that the other groups are compared with (vendors paid for time). |
| Regression | A calculation that finds the line, or the set of effects, that fits the data best. |
| Restructuring | One-time costs to reduce staff, offices or business units. GAAP and IFRS operating income includes them. |
| Revenue | The money that a company earns from its customers in one year. |
| Revenue per person | Revenue ÷ average headcount. |
| Score (AI margin-potential score) | 100 × the average of four scaled 2023 values: revenue model, gross margin, overhead share and revenue per person (section 3.3). |
| SE (standard error) | The uncertainty of an estimate. If an estimate is more than about 2 SE from zero, it is statistically significant at the 95% level. |
| Seat | One paid user license of a software product that is priced per user. |
| SEC | US Securities and Exchange Commission: the US authority that receives the reports of listed companies. |
| SG&A | Selling, general and administrative costs. |
| Significant (statistically) | Not likely to come from random variation only. In this paper: more than about 2 standard errors from zero. |
| Slope | How much the result changes when the score changes by one unit (here, by 10 points). |
| Spearman rank correlation | The Pearson correlation of the ranks (1st, 2nd, 3rd …) instead of the values. It is less sensitive to a few extreme values. |
| Speed-up formula | 1 ÷ ((1 − s) + s ÷ m): the total speed-up of a job when a share s of the work becomes m times faster (Amdahl's law). |
| SSRN | Social Science Research Network: a public website where researchers publish working papers. |
| Utilization | The share of working hours that a vendor bills to clients. |
| Vendor | An IT services company that does work for clients. "Vendor paid for time" means the client pays for people, days or hours (time and materials). |
| XBRL | eXtensible Business Reporting Language: the machine-readable format of financial reports filed with the SEC. |
| Year effect | One constant for each calendar year in a model. It removes changes that are the same for all companies in that year, for example demand or interest rates. |

## Data and code

The data files and scripts are in the public repository <https://github.com/skorsun/research-study> (folders `panel` and `ai-margin-potential`): `fetch_sec.py` (SEC XBRL), `build_panel.py` (panel and models), `score.py` (score and test), with the data files and the outputs. All values marked as calculated are the author's arithmetic from the listed sources.

## Sources

- U.S. Securities and Exchange Commission, XBRL company facts API, https://data.sec.gov/api/xbrl/companyfacts/ (annual reports of the 16 companies, fiscal years 2017–2026).
- Headcount history: https://stockanalysis.com (company employee pages); https://www.macrotrends.net (Globant); Globant Q4 2020 results release.
- Infosys fiscal 2026 revenue: https://analyticsindiamag.com/it-services/muted-guidance-overshadows-infosys-20-billion-revenue-milestone ; https://www.investywise.com/?p=76330
- Wipro fiscal 2026 revenue: https://www.angelone.in/news/stocks/wipro-fy26-earnings-results-revenue-at-rs-926-2-billion-net-profit-at-rs-132-billion ; https://www.bajajbroking.in/share-market-news/wipro-q4fy26-results-revenue-steady-sequential-growth-guidance-of-2-to-0-percent-rs150-billion-buyback-approved
- Accenture fixed-price share: Accenture Q4 fiscal 2026 earnings call.
- Korsunenko, S. (2026). Where Did the AI Productivity Go? Four IT Services Companies, Two Years, Public Numbers Only. SSRN working paper 7687580, https://ssrn.com/abstract=7687580

---

**About the author.** Serhii Korsunenko is an applied AI and data engineer in Aachen, Germany. He worked at EPAM Systems in the past. He is the author of "The Case of the Missing $331 Million", a book on reading company financial statements: https://www.amazon.com/dp/B0HQVTX11K

This paper is for education only. It is not investment advice and does not recommend or judge any company.
