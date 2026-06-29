Streamlit Multi-Asset Financial Dashboard

## 1. Project Objective

This project creates a complete **Streamlit multi-asset financial dashboard** using Python.

T
This dashboard allows the user to:

- enter multiple stock tickers;
- select a start date;
- define portfolio weights;
- set a portfolio value;
- compare cumulative returns;
- analyse return distributions;
- view a correlation heatmap;
- compare risk and return;
- view portfolio allocation;
- analyse return contribution;
- inspect one selected asset in detail with candlesticks, MA20, MA50, volume, cumulative return and drawdown;
- export the analysis to Excel.

---

## 2. Main File

The main Streamlit file is:

```text
Multi_asset_dashboard.py
```

This is the final integrated dashboard file for this phase of the project.

---

## 3. VS Code Debug File

The VS Code Run and Debug configuration is stored in:

```text
.vscode/launch.json
```

This file allows the Streamlit dashboard to open directly through **Run and Debug** instead of only through the terminal.

---

## 4. Recommended Project Structure

The project folder should look like this:

```text
Plotly Asset Visualization Program
│
├── .vscode
│   └── launch.json
│
├── Multi_asset_dashboard.py

```

### Folder meaning

| Folder / File | Purpose |
|---|---|
| `.vscode/launch.json` | Runs Streamlit dashboards through VS Code Run and Debug. |
| `multi_asset_dashboard.py` | Final integrated multi-asset dashboard. |

---

## 5. Libraries Used

```python
from pathlib import Path
from io import BytesIO
from datetime import date

import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
```

### Purpose of each library

| Library | Purpose |
|---|---|
| `pandas` | DataFrames, returns, metrics, correlation, drawdown, portfolio contribution and Excel export. |
| `yfinance` | Downloads historical stock market data from Yahoo Finance. |
| `plotly.graph_objects` | Creates interactive financial charts. |
| `plotly.subplots.make_subplots` | Creates the multi-row single-asset technical chart. |
| `streamlit` | Builds the browser-based dashboard interface. |
| `pathlib.Path` | Handles file paths and creates the `Data` folder. |
| `BytesIO` | Creates Excel files in memory for download. |
| `datetime.date` | Sets default dates for Streamlit inputs. |

---

## 6. Installation

The project is configured to run with **Python 3.14**.

Install the required libraries with:

```bash
py -3.14 -m pip install streamlit pandas yfinance plotly openpyxl
```

If needed, upgrade pip first:

```bash
py -3.14 -m pip install --upgrade pip
```

Check Streamlit:

```bash
py -3.14 -m streamlit version
```

---

## 7. How to Run from Terminal

Inside the `Plotly Practice` folder, run:

```bash
py -3.14 -m streamlit run Multi_asset_dashboard.py
```

Do **not** run the Streamlit app with:

```bash
python Multi_asset_dashboard.py
```

Streamlit apps must be launched through:

```bash
streamlit run
```

or:

```bash
python -m streamlit run
```

For this project, the safest command is:

```bash
py -3.14 -m streamlit run Multi_asset_dashboard.py
```

---

## 8. VS Code Run and Debug Configuration

The dashboard can be run directly from **Run and Debug** in VS Code.

The file:

```text
.vscode/launch.json
```

should contain:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Run Multi-Asset Streamlit Dashboard - Python 3.14",
      "type": "debugpy",
      "request": "launch",
      "python": "C:/Users/Lenovo/AppData/Local/Python/pythoncore-3.14-64/python.exe",
      "module": "streamlit",
      "args": [
        "run",
        "${workspaceFolder}/multi_asset_dashboard.py"
      ],
      "console": "integratedTerminal",
      "justMyCode": true
    },
  ]
}
```

If the Python path is different, run:

```bash
py -3.14 -c "import sys; print(sys.executable)"
```

Then replace this part:

```json
"python": "C:/Users/Lenovo/AppData/Local/Python/pythoncore-3.14-64/python.exe"
```

with the path returned by the terminal.

---

## 9. How to Run with VS Code Run and Debug

In VS Code:

```text
Run and Debug
```

Then choose:

```text
Run Multi-Asset Streamlit Dashboard - Python 3.14
```

Then press the green play button.

Important:

```text
Do not use Run Python File for Streamlit apps.
```

That button runs the file as a normal Python script, but Streamlit must run through its own runtime.

---

## 10. Sidebar Inputs

The dashboard includes the following sidebar controls:

| Input | Meaning |
|---|---|
| `Tickers` | Comma-separated list of stock tickers. |
| `Start date` | Start date for the analysis. |
| `Portfolio weights (%)` | Optional portfolio weights. Leave blank for equal weights. |
| `Portfolio value` | Total portfolio value used for allocation and contribution analysis. |
| `Save Excel file to Data folder` | Saves the Excel export automatically inside the `Data` folder. |

Example tickers:

```text
AAPL, MSFT, AMZN, TSLA, NVDA
```

Example weights:

```text
30, 25, 20, 15, 10
```

If weights are left blank, the dashboard creates an equal-weight portfolio.

---

## 11. Dashboard Tabs

The final version contains eight tabs:

```text
Performance
Distribution
Correlation
Risk-Return
Allocation
Contribution
Single Asset Detail
Data & Export
```

Each tab corresponds to one part of the financial analysis.

---

## 12. Tab 1 — Performance

The **Performance** tab shows:

```text
Multi-Asset Cumulative Returns
```

This graph compares the cumulative returns of all selected assets.

### Main calculation

```python
daily_returns = prices.pct_change().dropna()
cumulative_returns = (1 + daily_returns).cumprod() - 1
```

### Financial interpretation

All assets start at `0%`, so performance comparison is fairer than comparing raw prices.

A higher line means the asset delivered higher cumulative return over the selected period.

This tab is useful for answering:

```text
Which asset performed best?
Which asset underperformed?
When did performance leadership change?
Which assets had more unstable performance paths?
```

---

## 13. Tab 2 — Distribution

The **Distribution** tab includes:

```text
Histogram of Daily Returns
Box Plot of Daily Returns
```

The user selects one ticker from a dropdown.

### Histogram

The histogram shows the frequency distribution of daily returns.

It helps identify:

- whether returns are concentrated around zero;
- whether there are extreme return days;
- whether there are outliers;
- whether the asset has a wide or narrow return distribution.

### Box plot

The box plot summarises:

- median return;
- interquartile range;
- dispersion;
- outliers.

This tab is useful for understanding the statistical behaviour of one selected asset.

---

## 14. Tab 3 — Correlation

The **Correlation** tab shows:

```text
Correlation Heatmap
```

### Main calculation

```python
correlation_matrix = daily_returns.corr()
```

### Financial interpretation

Correlation measures how assets move together.

| Correlation | Interpretation |
|---|---|
| Close to `+1` | Assets moved very similarly. |
| Around `0` | Weak linear relationship. |
| Negative | Assets tended to move in opposite directions. |

High correlation can reduce diversification benefits.

Lower correlation can improve diversification, but must still be analysed together with return, volatility and drawdown.

---

## 15. Tab 4 — Risk-Return

The **Risk-Return** tab shows:

```text
Risk-Return Scatter Plot
```

### Main calculations

```python
annualized_return = average_daily_return * 252
annualized_volatility = daily_volatility * (252 ** 0.5)
sharpe_ratio = annualized_return / annualized_volatility
```

### Chart meaning

| Element | Meaning |
|---|---|
| X-axis | Annualized volatility. |
| Y-axis | Annualized return. |
| Marker colour | Sharpe Ratio. |
| Marker size | Sharpe Ratio magnitude. |
| Each point | One asset. |

### Financial interpretation

The upper-left area is generally more attractive because it represents higher return with lower volatility.

The lower-right area is generally weaker because it represents lower return with higher volatility.

---

## 16. Tab 5 — Allocation

The **Allocation** tab shows:

```text
Portfolio Allocation Pie Chart
```

### Main calculations

```python
allocated_value = portfolio_value * (weight / 100)
estimated_shares = allocated_value / latest_close_price
```

### Financial interpretation

The pie chart shows the portfolio weights.

It helps identify:

- concentration risk;
- dominant assets;
- equal-weight vs concentrated allocation;
- exposure by ticker.

A large slice means a large portfolio weight.

---

## 17. Tab 6 — Contribution

The **Contribution** tab shows:

```text
Portfolio Return Contribution Waterfall
```

### Main formula

```text
Return Contribution = Portfolio Weight × Asset Return
```

### Financial interpretation

This tab shows which assets added or reduced portfolio performance.

A stock can have a high return but low contribution if its weight is small.

A stock can have a moderate return but high contribution if its weight is large.

This is a simple form of portfolio performance attribution.

---

## 18. Tab 7 — Single Asset Detail

The **Single Asset Detail** tab was added in the updated version.

It combines the previous single-stock dashboard logic with the multi-asset dashboard.

The user selects one valid ticker from a dropdown and the tab displays:

```text
Candlestick chart
MA20
MA50
Trading volume
Cumulative return
Drawdown
Single-asset metrics
Daily data table
```

### Main calculations

```python
df["MA20"] = df["Close"].rolling(window=20).mean()
df["MA50"] = df["Close"].rolling(window=50).mean()

df["Daily_Return"] = df["Close"].pct_change().fillna(0)
df["Cumulative_Return"] = (1 + df["Daily_Return"]).cumprod() - 1

df["Cumulative_Wealth"] = (1 + df["Daily_Return"]).cumprod()
df["Running_Max"] = df["Cumulative_Wealth"].cummax()
df["Drawdown"] = (df["Cumulative_Wealth"] / df["Running_Max"]) - 1
```

### What the chart shows

| Section | Meaning |
|---|---|
| Candlestick | Open, high, low and close prices. |
| MA20 | 20-day moving average, short-term trend. |
| MA50 | 50-day moving average, medium-term trend. |
| Volume | Trading activity. |
| Cumulative return | Total compounded return since the selected start date. |
| Drawdown | Decline from previous peak. |

### Financial interpretation

This tab is useful for detailed analysis of one selected asset.

It answers:

```text
How did the price move?
Is the asset above or below moving averages?
Was volume high during certain movements?
What was the cumulative return?
How deep were the drawdowns?
How volatile was the asset?
```

This addition makes the dashboard more complete because it now supports both:

```text
Portfolio-level analysis
+
Individual asset analysis
```

---

## 19. Tab 8 — Data & Export

The **Data & Export** tab allows the user to:

- download an Excel file;
- save the Excel file into the `Data` folder;
- view asset metrics;
- view portfolio contribution;
- view prices;
- view daily returns;
- view the correlation matrix.

The export is created in memory with:

```python
output = BytesIO()
```

and written with:

```python
with pd.ExcelWriter(output, engine="openpyxl") as writer:
    prices.to_excel(writer, sheet_name="Prices")
    daily_returns.to_excel(writer, sheet_name="Daily Returns")
    cumulative_returns.to_excel(writer, sheet_name="Cumulative Returns")
    metrics_df.to_excel(writer, sheet_name="Metrics", index=False)
    correlation_matrix.to_excel(writer, sheet_name="Correlation")
    contribution_df.to_excel(writer, sheet_name="Portfolio Contribution", index=False)
```

---

## 20. Excel Sheets Exported

The exported Excel file includes:

| Sheet | Contents |
|---|---|
| `Prices` | Historical close prices for each ticker. |
| `Daily Returns` | Daily percentage returns. |
| `Cumulative Returns` | Compounded cumulative returns. |
| `Metrics` | Return, volatility, Sharpe and drawdown per asset. |
| `Correlation` | Correlation matrix of daily returns. |
| `Portfolio Contribution` | Weights, returns, contribution, values and gain/loss. |

The Excel file is saved with a name like:

```text
AAPL_MSFT_AMZN_TSLA_NVDA_2024_01_01_multi_asset_dashboard.xlsx
```

If the save option is active, the file is also saved inside:

```text
Data/
```

---

## 21. Main Functions in the Code

| Function | Purpose |
|---|---|
| `parse_tickers()` | Converts comma-separated ticker input into a list. |
| `parse_weights()` | Converts and normalises portfolio weights. |
| `download_prices()` | Downloads close prices for multiple tickers. |
| `calculate_asset_metrics()` | Calculates returns, volatility, drawdown and Sharpe Ratio. |
| `calculate_portfolio_contribution()` | Calculates return contribution by asset. |
| `create_cumulative_returns_chart()` | Creates the multi-asset cumulative return chart. |
| `create_histogram_chart()` | Creates histogram of daily returns. |
| `create_boxplot_chart()` | Creates box plot of daily returns. |
| `create_correlation_heatmap()` | Creates correlation heatmap. |
| `create_risk_return_scatter()` | Creates risk-return scatter plot. |
| `create_portfolio_pie_chart()` | Creates portfolio allocation pie chart. |
| `create_waterfall_chart()` | Creates return contribution waterfall. |
| `download_single_asset_ohlcv()` | Downloads OHLCV data for one selected asset. |
| `calculate_single_asset_detail()` | Calculates single-asset MA20, MA50, return and drawdown. |
| `create_single_asset_detail_chart()` | Creates candlestick, volume, cumulative return and drawdown chart. |
| `create_excel_file()` | Creates Excel export file. |

---

## 22. Main Metrics Calculated

| Metric | Meaning |
|---|---|
| `Total Return` | Total price return over the selected period. |
| `Average Daily Return` | Mean daily return. |
| `Annualized Return` | Approximate annual return. |
| `Daily Volatility` | Standard deviation of daily returns. |
| `Annualized Volatility` | Daily volatility scaled to annual terms. |
| `Maximum Drawdown` | Worst peak-to-trough loss. |
| `Sharpe Ratio` | Simplified return-to-risk ratio. |
| `Return Contribution` | Asset weight multiplied by asset return. |
| `MA20` | 20-day moving average. |
| `MA50` | 50-day moving average. |

---

## 23. Portfolio Total Return

The dashboard calculates portfolio return using weighted contributions:

```python
portfolio_total_return = contribution_df["Return Contribution"].sum()
```

This means:

```text
Portfolio Total Return = Sum of all asset return contributions
```

Example:

```text
AAPL contribution = +4%
MSFT contribution = +3%
TSLA contribution = -1%

Portfolio total return = +6%
```

---

## 24. Important Financial Concepts Practised

This dashboard practises:

```text
Close prices
OHLCV data
Daily returns
Cumulative returns
Moving averages
Volatility
Annualisation
Correlation
Sharpe Ratio
Drawdown
Portfolio weights
Allocation
Return contribution
Performance attribution
Excel export
Interactive dashboards
```

---

## 25. Important Assumptions

The dashboard assumes:

- prices are downloaded from `yfinance`;
- close prices are used for return calculations;
- OHLCV data is used for the single-asset detail chart;
- risk-free rate is `0%` for Sharpe Ratio;
- portfolio weights are held constant over the selected period;
- no transaction costs;
- no taxes;
- no currency conversion;
- no rebalancing;
- no benchmark;
- no dividends unless reflected in the selected price series.

---

## 26. Limitations

This dashboard is for learning and analysis only.

Important limitations:

- it is not investment advice;
- historical performance does not predict future performance;
- results depend heavily on the selected start date;
- `yfinance` data may contain gaps, delays or revisions;
- raw close prices may not fully reflect dividends and corporate actions;
- Sharpe Ratio is simplified because the risk-free rate is assumed to be 0%;
- correlation can change over time;
- portfolio contribution assumes static weights;
- moving averages are descriptive and not predictive;
- no benchmark-relative analysis is included;
- no portfolio optimisation is included.

---

## 27. Debugging Notes

### Problem: Streamlit does not open correctly with Run Python File

Cause:

```text
VS Code runs the file as a normal Python script.
```

Wrong:

```bash
python 08_streamlit_multi_asset_dashboard.py
```

Correct:

```bash
py -3.14 -m streamlit run 08_streamlit_multi_asset_dashboard.py
```

or use the `launch.json` debug configuration.

---

### Problem: Streamlit command uses the wrong Python version

Use:

```bash
py -3.14 -m streamlit run 08_streamlit_multi_asset_dashboard.py
```

instead of:

```bash
streamlit run 08_streamlit_multi_asset_dashboard.py
```

This forces Python 3.14.

---

### Problem: Python path in `launch.json` is wrong

Run:

```bash
py -3.14 -c "import sys; print(sys.executable)"
```

Then copy the returned path into:

```json
"python": "PASTE_PATH_HERE"
```

---

## 28. Relationship with Previous Exercises

This dashboard integrates the previous exercises:

| Exercise | Integrated in Dashboard |
|---|---|
| `01_histogram_returns.py` | Distribution tab |
| `02_boxplot_returns.py` | Distribution tab |
| `03_multi_ticker_comparison.py` | Performance tab |
| `04_correlation_heatmap.py` | Correlation tab |
| `05_risk_return_scatter.py` | Risk-Return tab |
| `06_portfolio_pie_chart.py` | Allocation tab |
| `07_waterfall_return_contribution.py` | Contribution tab |
| `streamlit_financial_dashboard.py` | Single Asset Detail tab logic |

---

## 29. Suggested Next Improvements

Possible future upgrades:

1. Add benchmark comparison such as `SPY`, `QQQ` or `^GSPC`.
2. Add portfolio volatility.
3. Add portfolio Sharpe Ratio.
4. Add portfolio drawdown chart.
5. Add rolling volatility.
6. Add rolling correlation.
7. Add monthly returns heatmap.
8. Add sector allocation.
9. Add geographic allocation.
10. Add adjusted close option.
11. Add rebalancing logic.
12. Add benchmark-relative performance.
13. Add VaR and CVaR.
14. Add Monte Carlo portfolio simulation.
15. Add efficient frontier.
16. Improve Excel formatting with `openpyxl`.
17. Export the Single Asset Detail data to Excel.
18. Add a comparison between portfolio and benchmark.

---

## 30. Current Project Status

```text
Completed:
- Individual Plotly graph exercises from 01 to 07
- Multi-asset Streamlit dashboard created
- Sidebar inputs added
- Tabs added
- Multi-asset cumulative return chart added
- Histogram and box plot added
- Correlation heatmap added
- Risk-return scatter plot added
- Portfolio allocation pie chart added
- Return contribution waterfall added
- Single Asset Detail tab added
- Candlestick chart added inside dashboard 08
- MA20 and MA50 added inside dashboard 08
- Volume chart added inside dashboard 08
- Cumulative return chart added inside dashboard 08
- Drawdown chart added inside dashboard 08
- Excel export added
- Data folder export added
- VS Code Run and Debug configuration added
- Python 3.14 execution confirmed
```

---

## 31. How to Run Everything

### Terminal

```bash
py -3.14 -m streamlit run 08_streamlit_multi_asset_dashboard.py
```

### VS Code Run and Debug

Select:

```text
Run Multi-Asset Streamlit Dashboard - Python 3.14
```

Then press the green play button.

---

## 32. Final Note

This dashboard is now a solid practical Python for Finance mini-project.

It combines:

```text
data download
data cleaning
returns
risk metrics
correlation
portfolio allocation
performance attribution
technical single-asset analysis
interactive visualisation
Excel export
Streamlit workflow
VS Code debugging
```

It should be treated as a learning and analysis tool, not as investment advice.
