# Research study: AI, productivity and margins in software and IT services

Two working papers by Serhii Korsunenko (November 2026). The papers use public company reports only. They compare the AI story in the media with the real results of listed software and IT services companies.

| Folder | Content |
|---|---|
| [`ai-services-study/`](ai-services-study/) | **Where Did the AI Productivity Go?** Four IT services companies (EPAM, Infosys, Cognizant, Accenture), mid-2024 against mid-2026. Paper as Markdown and PDF. |
| [`ai-margin-potential/`](ai-margin-potential/) | **Who Keeps the AI Gain? A Margin-Potential Score for 16 Software and IT Services Companies.** Panel 2017–2026: revenue per person, operating margin and a score from 2023 data. Paper as Markdown and PDF, and the score script with its output. |
| [`panel/`](panel/) | Data and code for the 16-company panel: SEC XBRL financials, headcount, the panel file and the models. |

## Links

- Web version of both papers: https://serhii.korsunenko.com
- "Where Did the AI Productivity Go?" on SSRN: https://ssrn.com/abstract=7687580

## Main results

1. At four large IT services companies, revenue per person grew by 0.8% to 8.1% in two years (mid-2024 to mid-2026), and headcount grew at all four.
2. In a panel of 16 companies, revenue per person grew faster after 2024 in all groups. The difference between product companies and vendors paid for time is 0.0 points per year (standard error 2.6).
3. Operating margin: product companies +2.5 points per year in the AI period, vendors paid for time +0.2. After year effects, the difference is 1.2 points per year (standard error 1.3), not yet significant.
4. The business model (product or time billing) predicts the margin change after 2023 (r = 0.75). A score from four 2023 values gives the same result (r = 0.72).

## Data sources

- U.S. Securities and Exchange Commission, XBRL company facts API (annual 10-K and 20-F reports).
- Headcount from the annual reports, stockanalysis.com and macrotrends.net.
- Infosys and Wipro fiscal 2026 revenue from two press sources each.

The sources of each value are listed in the papers and in [`panel/README.md`](panel/README.md).

## License

The papers are licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Cite as:

- Korsunenko, S. (2026). Where Did the AI Productivity Go? Four IT Services Companies, Two Years, Public Numbers Only. SSRN working paper 7687580.
- Korsunenko, S. (2026). Who Keeps the AI Gain? A Margin-Potential Score for 16 Software and IT Services Companies. Working paper.

## Disclaimer

The papers are for education only. They are not investment advice and do not recommend or judge any company. The author worked at EPAM Systems in the past and has no current relationship with any company in the study.
