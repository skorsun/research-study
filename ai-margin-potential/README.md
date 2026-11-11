# Who Keeps the AI Gain?

**A Margin-Potential Score for 16 Software and IT Services Companies.** Serhii Korsunenko, working paper, November 2026.

| File | Content |
|---|---|
| [`ai-margin-potential-2026.md`](ai-margin-potential-2026.md) | Full text (Markdown) |
| [`ai-margin-potential-2026.pdf`](ai-margin-potential-2026.pdf) | Full text (PDF, A4, with charts) |
| [`score.py`](score.py) | Calculates the AI margin-potential score and its test against the operating margin change |
| [`score.csv`](score.csv) | Output: score, components and margin change for each company |
| [`results.json`](results.json) | Output: the same values and the test statistics (correlation, slope, leave-one-out) |

- SSRN: https://ssrn.com/abstract=7691398
- Web version: https://serhii.korsunenko.com/articles/ai-margin-potential/
- Data and panel code: [`../panel/`](../panel/)

## How to run

Python 3.10 or later with numpy. The script reads `../panel/panel.csv`.

```bash
python score.py
```

The output must be equal to the values in section 4.3 of the paper. The formula and a full worked example for SAP are in section 3.3.

License: CC BY 4.0. For education only. Not investment advice.
