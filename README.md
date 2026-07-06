# Streamlit Multi-Asset Financial Dashboard

## 1. Project Objective

This project creates a complete **Streamlit multi-asset financial dashboard** using Python.

The dashboard allows the user to:

- enter multiple stock tickers;
- select a start date;
- define portfolio weights;
- set an initial portfolio value;
- compare cumulative returns;
- analyse daily return distributions;
- view a correlation heatmap;
- compare risk and return;
- analyse portfolio allocation using an interactive pie chart;
- hide/show tickers in the allocation pie chart and recalculate visible weights automatically;
- analyse return contribution by asset;
- inspect one selected asset in detail with candlesticks, MA20, MA50, volume, cumulative return and drawdown;
- view portfolio value evolution;
- export the analysis to Excel.

The goal of the project is educational and analytical. It is designed to help understand how Python, pandas, yfinance, Plotly and Streamlit can be combined to build a practical financial dashboard.

---

## 2. Main File

The main Streamlit file should be:

```text
Multi_Asset_Dashboard.py
```

If you are testing a corrected version with another name, such as:

```text
Multi_Asset_Dashboard_pie_hover_fixed.py
```

you can either run that file directly or copy its content into:

```text
Multi_Asset_Dashboard.py
```

For the final project structure, it is cleaner to keep one main file named:

```text
Multi_Asset_Dashboard.py
```

---

## 3. Recommended Project Structure

The project folder should look like this:

```text
Plotly Asset Visualization Program
│
├── .vscode
│   └── launch.json
│
├── Data
│   └── exported Excel files
│
├── Multi_Asset_Dashboard.py
│
└── README.md
```

### Folder and file meaning

| Folder / File | Purpose |
|---|---|
| `.vscode/launch.json` | Allows the dashboard to run through VS Code Run and Debug. |
| `Data/` | Stores exported Excel files if the save option is selected. |
| `Multi_Asset_Dashboard.py` | Main Streamlit dashboard file. |
| `README.md` | Documentation explaining the project, formulas and how to run it. |

---

## 4. Libraries Used

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
| `plotly.graph_objects` | Creates interactive financial charts such as line charts, pie charts, scatter plots, heatmaps, candlesticks and waterfalls. |
| `plotly.subplots.make_subplots` | Creates the multi-row single-asset technical chart. |
| `streamlit` | Builds the browser-based dashboard interface. |
| `pathlib.Path` | Handles project paths and creates the `Data` folder. |
| `BytesIO` | Creates Excel files in memory before downloading or saving them. |
| `datetime.date` | Sets default dates in Streamlit date inputs. |

---

## 5. Installation

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

## 6. How to Run from the Terminal

Open the project folder in VS Code, then run:

```bash
py -3.14 -m streamlit run Multi_Asset_Dashboard.py
```

Do **not** run the Streamlit app with:

```bash
python Multi_Asset_Dashboard.py
```

That command runs the file as a normal Python script. Streamlit apps must be launched through the Streamlit runtime.

Correct options:

```bash
streamlit run Multi_Asset_Dashboard.py
```

or:

```bash
python -m streamlit run Multi_Asset_Dashboard.py
```

For this project, the safest command is:

```bash
py -3.14 -m streamlit run Multi_Asset_Dashboard.py
```

---

## 7. VS Code Run and Debug Configuration

The dashboard can also run directly from **Run and Debug** in VS Code.

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
        "${workspaceFolder}/Multi_Asset_Dashboard.py"
      ],
      "console": "integratedTerminal",
      "justMyCode": true
    }
  ]
}
```

If your Python path is different, run:

```bash
py -3.14 -c "import sys; print(sys.executable)"
```

Then replace this part:

```json
"python": "C:/Users/Lenovo/AppData/Local/Python/pythoncore-3.14-64/python.exe"
```

with the path returned by the terminal.

Important: if you rename the Python file, you must also update the file name inside `launch.json`.

---

## 8. Sidebar Inputs

The dashboard contains the following sidebar controls:

| Input | Meaning |
|---|---|
| `Tickers` | Comma-separated list of stock tickers. |
| `Start date` | Start date for the historical analysis. |
| `Portfolio weights (%)` | Portfolio weights entered in the same order as the tickers. Leave blank for equal weights. |
| `Portfolio value` | Initial capital invested at the selected start date. |
| `Save Excel file to Data folder` | Saves the exported Excel file automatically inside the `Data/` folder. |

Example tickers:

```text
UNH, OKLO, TSM, AMD
```

Example weights:

```text
25, 20, 15, 40
```

The order matters:

| Ticker | Weight |
|---|---:|
| `UNH` | 25% |
| `OKLO` | 20% |
| `TSM` | 15% |
| `AMD` | 40% |

If weights are left blank, the dashboard creates an equal-weight portfolio.

If the weights do not add up to 100, the code normalises them automatically.

### Weight normalisation formula

```text
Normalised Weight_i = Input Weight_i / Sum of Input Weights × 100
```

Example:

```text
Input weights = 10, 10, 30
Total = 50
Normalised weights = 20%, 20%, 60%
```

---

## 9. Main Dashboard Tabs

The dashboard contains eight tabs:

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

Each tab answers a different financial question.

| Tab | Main question answered |
|---|---|
| `Performance` | How did each asset and the portfolio perform over time? |
| `Distribution` | How are daily returns distributed? |
| `Correlation` | How strongly do the assets move together? |
| `Risk-Return` | Which assets delivered more return for more or less risk? |
| `Allocation` | How is the portfolio allocated by initial weights and how do values change? |
| `Contribution` | Which assets contributed most to total portfolio return? |
| `Single Asset Detail` | What happened inside one selected asset? |
| `Data & Export` | What data and calculated outputs can be exported to Excel? |

---

## 10. Data Download Logic

The function `download_prices()` downloads historical close prices for each ticker using `yfinance`.

The data cleaning process is:

```python
prices = prices.dropna(how="all")
prices = prices.ffill()
prices = prices.dropna()
```

### Meaning

| Step | Meaning |
|---|---|
| `dropna(how="all")` | Removes rows where all tickers have missing data. |
| `ffill()` | Forward-fills missing prices using the previous available value. |
| `dropna()` | Removes remaining rows with missing values. |

### Financial interpretation

The dashboard only analyses dates where the final cleaned dataset has valid prices for all selected assets.

If a ticker has no data, it is skipped and the app displays a warning.

---

## 11. Core Return Formulas

### Daily return

```text
Daily Return_t = Price_t / Price_(t-1) - 1
```

Python:

```python
daily_returns = prices.pct_change().dropna()
```

### Cumulative return

```text
Cumulative Return_t = (1 + Daily Return_1) × ... × (1 + Daily Return_t) - 1
```

Python:

```python
cumulative_returns = (1 + daily_returns).cumprod() - 1
```

### Asset total return

```text
Asset Total Return = Last Price / First Price - 1
```

Python:

```python
total_return = (last_price / first_price) - 1
```

### Financial interpretation

Returns are used instead of raw prices because raw prices are not directly comparable between stocks with different price levels.

Example:

```text
A stock moving from 100 to 120 returns 20%.
A stock moving from 500 to 600 also returns 20%.
```

The raw price change is different, but the percentage return is the same.

---

## 12. Asset Metrics

For each asset, the dashboard calculates:

| Metric | Formula | Meaning |
|---|---|---|
| `First Price` | First available close price | Starting price in the analysis. |
| `Last Price` | Last available close price | Most recent close price in the dataset. |
| `Total Return` | `Last Price / First Price - 1` | Total asset return over the period. |
| `Average Daily Return` | Mean of daily returns | Average daily return. |
| `Annualized Return` | `Average Daily Return × 252` | Simple annualised return estimate. |
| `Daily Volatility` | Standard deviation of daily returns | Daily return dispersion. |
| `Annualized Volatility` | `Daily Volatility × sqrt(252)` | Annualised risk estimate. |
| `Maximum Drawdown` | Minimum drawdown | Worst peak-to-trough decline. |
| `Sharpe Ratio` | `Annualized Return / Annualized Volatility` | Return per unit of volatility. |

### Annualized return

```text
Annualized Return = Average Daily Return × 252
```

This uses 252 because there are approximately 252 trading days in a year.

### Annualized volatility

```text
Annualized Volatility = Daily Volatility × √252
```

### Sharpe Ratio

```text
Sharpe Ratio = Annualized Return / Annualized Volatility
```

Important: this dashboard uses a simplified Sharpe Ratio without subtracting a risk-free rate.

A more complete Sharpe Ratio would be:

```text
Sharpe Ratio = (Portfolio Return - Risk-Free Rate) / Portfolio Volatility
```

---

## 13. Drawdown Formula

Drawdown measures how far the asset has fallen from its previous peak.

### Cumulative wealth

```text
Cumulative Wealth_t = (1 + Daily Return_1) × ... × (1 + Daily Return_t)
```

Python:

```python
cumulative_wealth = (1 + daily_returns[ticker]).cumprod()
```

### Running maximum

```text
Running Max_t = Maximum value of cumulative wealth up to time t
```

Python:

```python
running_max = cumulative_wealth.cummax()
```

### Drawdown

```text
Drawdown_t = Cumulative Wealth_t / Running Max_t - 1
```

Python:

```python
drawdown = (cumulative_wealth / running_max) - 1
```

### Maximum drawdown

```text
Maximum Drawdown = Minimum Drawdown over the period
```

Python:

```python
maximum_drawdown = drawdown.min()
```

### Financial interpretation

A drawdown of `-30%` means the asset lost 30% from a previous peak before recovering or continuing lower.

Maximum drawdown is useful because volatility does not fully show the severity of losses.

---

## 14. Portfolio Contribution Formula

The dashboard calculates each asset's contribution to total portfolio return.

### Asset return

```text
Asset Return_i = Last Price_i / First Price_i - 1
```

### Weight decimal

```text
Weight Decimal_i = Weight_i / 100
```

### Return contribution

```text
Return Contribution_i = Weight Decimal_i × Asset Return_i
```

Python:

```python
return_contribution = weight_decimal * asset_return
```

### Portfolio total return

```text
Portfolio Total Return = Sum of all Return Contributions
```

Python:

```python
portfolio_total_return = contribution_df["Return Contribution"].sum()
```

### Financial interpretation

An asset contributes more to total portfolio performance when:

- its return is high; and/or
- its portfolio weight is high.

A high-return stock with a small weight may contribute less than a moderate-return stock with a large weight.

---

## 15. Portfolio Value Formulas

The sidebar field:

```text
Portfolio value
```

represents the **initial capital invested at the selected start date**.

Example:

```text
Portfolio value = 250,000
```

This means the dashboard assumes the portfolio starts with 250,000 monetary units.

The currency symbol is not fixed. The value can be interpreted as USD, EUR, GBP or another currency depending on the user's context. Since Yahoo Finance prices are usually in the asset's trading currency, currency consistency should be checked by the user.

---

## 16. Initial Allocated Value

Each asset receives an initial amount based on the sidebar weight.

### Formula

```text
Initial Allocated Value_i = Portfolio Value × Weight_i / 100
```

Python:

```python
portfolio_df["Initial Allocated Value"] = (
    portfolio_value * (portfolio_df["Weight"] / 100)
)
```

Example:

```text
Portfolio value = 250,000
AMD weight = 40%
Initial AMD allocation = 250,000 × 40% = 100,000
```

---

## 17. Estimated Shares Bought

The dashboard estimates how many shares could have been bought at the start date.

### Formula

```text
Estimated Shares_i = Initial Allocated Value_i / First Price_i
```

Python:

```python
portfolio_df["Estimated Shares"] = (
    portfolio_df["Initial Allocated Value"] / portfolio_df["First Price"]
)
```

### Financial interpretation

This assumes fractional shares are allowed.

Example:

```text
Initial allocated value = 100,000
First price = 50
Estimated shares = 100,000 / 50 = 2,000 shares
```

---

## 18. Current Value Held

The current value of each position is calculated using the estimated shares and the latest close price.

### Formula

```text
Current Value_i = Estimated Shares_i × Last Price_i
```

Python:

```python
portfolio_df["Current Value"] = (
    portfolio_df["Estimated Shares"] * portfolio_df["Last Price"]
)
```

Example:

```text
Estimated shares = 2,000
Latest close price = 70
Current value = 2,000 × 70 = 140,000
```

---

## 19. Gain/Loss Formula

Gain/loss measures the monetary profit or loss of each position.

### Formula

```text
Gain/Loss_i = Current Value_i - Initial Allocated Value_i
```

Python:

```python
portfolio_df["Gain/Loss"] = (
    portfolio_df["Current Value"] - portfolio_df["Initial Allocated Value"]
)
```

Example:

```text
Current value = 140,000
Initial allocated value = 100,000
Gain/Loss = 40,000
```

---

## 20. Current Portfolio Value

The current portfolio value is calculated from the initial portfolio value and portfolio total return.

### Formula

```text
Current Portfolio Value = Initial Portfolio Value × (1 + Portfolio Total Return)
```

Python:

```python
portfolio_current_value = portfolio_initial_value * (1 + portfolio_total_return)
```

It can also be interpreted as the sum of the current values of all positions:

```text
Current Portfolio Value = Sum of Current Value_i
```

---

## 21. Portfolio Gain/Loss

### Formula

```text
Portfolio Gain/Loss = Current Portfolio Value - Initial Portfolio Value
```

Python:

```python
portfolio_gain_loss = portfolio_current_value - portfolio_initial_value
```

Example:

```text
Initial portfolio value = 250,000
Current portfolio value = 300,000
Portfolio gain/loss = 50,000
```

---

## 22. Allocation Tab

The **Allocation** tab contains the interactive portfolio pie chart.

In the latest version, the pie chart uses:

```python
values=portfolio_df["Weight"]
```

This means the pie chart reflects the **sidebar weights** entered by the user.

Example:

```text
Tickers: UNH, OKLO, TSM, AMD
Weights: 25, 20, 15, 40
```

The pie chart displays:

```text
UNH 25%
OKLO 20%
TSM 15%
AMD 40%
```

---

## 23. Interactive Hide/Show Ticker Logic

The allocation pie chart allows the user to click tickers in the legend.

When a ticker is hidden, Plotly recalculates the visible allocation weights automatically.

### Example

Initial weights:

| Ticker | Initial weight |
|---|---:|
| `UNH` | 25% |
| `OKLO` | 20% |
| `TSM` | 15% |
| `AMD` | 40% |

If `UNH` is hidden, the visible weights are recalculated using only:

```text
OKLO + TSM + AMD = 20 + 15 + 40 = 75
```

New visible weights:

| Ticker | Calculation | Visible weight |
|---|---:|---:|
| `OKLO` | `20 / 75` | 26.67% |
| `TSM` | `15 / 75` | 20.00% |
| `AMD` | `40 / 75` | 53.33% |

### Formula

```text
Visible Allocation Weight_i = Weight_i / Sum of Weights of Visible Tickers × 100
```

This is the value shown by Plotly as:

```text
%{percent}
```

---

## 24. Hover Information in the Allocation Pie Chart

The hover box shows two different types of information:

1. information recalculated by Plotly based on visible tickers;
2. fixed portfolio information calculated by the dashboard.

### Hover fields

| Hover field | Meaning |
|---|---|
| `Visible Allocation Weight` | Weight among the tickers currently visible in the pie chart. This changes when tickers are hidden. |
| `Initial Weight in Full Portfolio` | Original weight entered in the sidebar after normalisation. This does not change when tickers are hidden. |
| `Initial Allocated Value` | Monetary amount initially allocated to the asset. |
| `Asset Return Since Start` | Total return of that asset from the first price to the last price. |
| `Current Value Held` | Estimated current value of that position. |
| `Gain/Loss` | Monetary gain or loss of that position. |
| `First Price` | First available close price in the selected period. |
| `Latest Close Price` | Last available close price in the selected period. |
| `Estimated Shares Bought` | Estimated number of shares bought at the start date. |
| `Current Market Weight in Full Portfolio` | Current weight of the asset in the full portfolio after price movements. |

---

## 25. Difference Between Initial Weight, Visible Weight and Current Market Weight

These three concepts are different and should not be confused.

| Metric | Formula | Changes when hiding tickers? | Meaning |
|---|---|---|---|
| `Initial Weight in Full Portfolio` | User input weight after normalisation | No | The original allocation chosen by the user. |
| `Visible Allocation Weight` | Weight among visible tickers only | Yes | The recalculated percentage after hiding/showing tickers in the chart. |
| `Current Market Weight in Full Portfolio` | Current value of asset / current total portfolio value | No | The asset's real current weight after price movements. |

### Current Market Weight formula

```text
Current Market Weight_i = Current Value_i / Current Total Portfolio Value × 100
```

Python:

```python
portfolio_df["Current Market Weight"] = (
    portfolio_df["Current Value"] / portfolio_current_value
) * 100
```

### Interpretation

If AMD starts at 40% and rises more than the other assets, it may become 45% of the current portfolio value.

That means:

```text
Initial Weight in Full Portfolio = 40%
Current Market Weight in Full Portfolio = 45%
```

The difference is caused by price movement.

---

## 26. Why the Pie Chart Uses Sidebar Weights Instead of Current Value

The pie chart uses:

```python
values=portfolio_df["Weight"]
```

instead of:

```python
values=portfolio_df["Current Value"]
```

because the goal of the Allocation tab is to show the **user-defined allocation** and allow the visible allocation to recalculate when tickers are hidden.

If the pie chart used `Current Value`, the slices would show the current market composition instead of the chosen input weights.

Both views are useful, but they answer different questions.

| Pie chart basis | Question answered |
|---|---|
| `Weight` | What allocation did I choose? |
| `Current Value` | What does the portfolio look like after price movements? |

The current market composition is still shown in the hover and in the allocation table through:

```text
Current Market Weight in Full Portfolio
```

---

## 27. Performance Tab

The **Performance** tab shows:

```text
Portfolio Value Evolution
Multi-Asset Cumulative Returns
```

### Portfolio value metrics

| Metric | Meaning |
|---|---|
| `Initial Portfolio Value` | Portfolio value entered in the sidebar. |
| `Current Portfolio Value` | Estimated current value after applying portfolio return. |
| `Portfolio Gain/Loss` | Monetary change in portfolio value. |
| `Portfolio Total Return` | Total percentage return of the portfolio. |

### Cumulative returns chart

The cumulative returns chart compares the compounded performance of all selected assets.

Python:

```python
cumulative_returns = (1 + daily_returns).cumprod() - 1
```

### Financial interpretation

All assets start at `0%`, so their performance can be compared fairly.

A higher cumulative return line indicates stronger performance over the selected period.

---

## 28. Distribution Tab

The **Distribution** tab contains:

```text
Histogram of Daily Returns
Box Plot of Daily Returns
```

The user selects one ticker from a dropdown.

### Histogram

The histogram shows how often different daily return values occurred.

It helps identify:

- whether returns are concentrated around zero;
- whether the asset had extreme positive or negative days;
- whether the distribution is wide or narrow;
- whether there are possible outliers.

### Box plot

The box plot summarises:

- median daily return;
- interquartile range;
- dispersion;
- outliers.

### Financial interpretation

An asset with a wider distribution is usually more volatile.

Extreme outliers may indicate earnings announcements, market shocks, news events or data anomalies.

---

## 29. Correlation Tab

The **Correlation** tab shows the correlation matrix of daily returns.

Python:

```python
correlation_matrix = daily_returns.corr()
```

### Interpretation

| Correlation | Meaning |
|---|---|
| Close to `+1` | Assets moved very similarly. |
| Around `0` | Weak linear relationship. |
| Negative | Assets tended to move in opposite directions. |

### Financial interpretation

High correlation can reduce diversification benefits.

Low or negative correlation can improve diversification, but correlation should not be analysed alone. It should be considered together with returns, volatility, drawdown and portfolio weights.

---

## 30. Risk-Return Tab

The **Risk-Return** tab shows a scatter plot.

| Chart element | Meaning |
|---|---|
| X-axis | Annualized volatility. |
| Y-axis | Annualized return. |
| Marker colour | Sharpe Ratio. |
| Marker size | Sharpe Ratio magnitude. |
| Each point | One asset. |

### Main formulas

```text
Annualized Return = Average Daily Return × 252
```

```text
Annualized Volatility = Daily Volatility × √252
```

```text
Sharpe Ratio = Annualized Return / Annualized Volatility
```

### Financial interpretation

In general:

- upper-left is better: higher return with lower volatility;
- lower-right is weaker: lower return with higher volatility;
- higher Sharpe Ratio means better return per unit of volatility.

This is not investment advice. It is a historical risk-return comparison.

---

## 31. Contribution Tab

The **Contribution** tab shows a waterfall chart.

### Main formula

```text
Return Contribution_i = Portfolio Weight_i × Asset Return_i
```

### Portfolio total return

```text
Portfolio Total Return = Sum of Return Contributions
```

### Financial interpretation

The contribution tab helps answer:

```text
Which asset helped the portfolio most?
Which asset reduced performance?
Did a high-return asset matter enough to move the portfolio?
Did a high-weight asset dominate the result?
```

A stock can have strong performance but low contribution if it has a small weight.

A stock can dominate the portfolio result if it has both high weight and strong performance.

---

## 32. Single Asset Detail Tab

The **Single Asset Detail** tab allows the user to inspect one selected asset in more depth.

It includes:

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

### Moving averages

```text
MA20 = 20-day moving average of close price
MA50 = 50-day moving average of close price
```

Python:

```python
df["MA20"] = df["Close"].rolling(window=20).mean()
df["MA50"] = df["Close"].rolling(window=50).mean()
```

### Daily return

```python
df["Daily_Return"] = df["Close"].pct_change().fillna(0)
```

### Cumulative return

```python
df["Cumulative_Return"] = (1 + df["Daily_Return"]).cumprod() - 1
```

### Drawdown

```python
df["Cumulative_Wealth"] = (1 + df["Daily_Return"]).cumprod()
df["Running_Max"] = df["Cumulative_Wealth"].cummax()
df["Drawdown"] = (df["Cumulative_Wealth"] / df["Running_Max"]) - 1
```

### Financial interpretation

| Component | Meaning |
|---|---|
| Candlestick | Shows open, high, low and close prices. |
| MA20 | Short-term trend. |
| MA50 | Medium-term trend. |
| Volume | Trading activity. |
| Cumulative return | Compounded return since the start date. |
| Drawdown | Fall from previous peak. |

This tab combines technical price analysis with return and risk analysis.

---

## 33. Data & Export Tab

The **Data & Export** tab allows the user to:

- download an Excel file;
- save the Excel file to the `Data/` folder;
- view portfolio value summary;
- view asset metrics;
- view portfolio contribution;
- view prices;
- view daily returns;
- view the correlation matrix.

The Excel export is created in memory using:

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

## 34. Excel Sheets Exported

The exported Excel file includes:

| Sheet | Contents |
|---|---|
| `Prices` | Historical close prices for each ticker. |
| `Daily Returns` | Daily percentage returns. |
| `Cumulative Returns` | Compounded cumulative returns. |
| `Metrics` | Return, volatility, Sharpe Ratio and drawdown per asset. |
| `Correlation` | Correlation matrix of daily returns. |
| `Portfolio Contribution` | Weights, returns, contribution, values and gain/loss. |

The Excel file name follows this pattern:

```text
TICKER1_TICKER2_TICKER3_STARTDATE_multi_asset_dashboard.xlsx
```

Example:

```text
UNH_OKLO_TSM_AMD_2024_01_01_multi_asset_dashboard.xlsx
```

If the save option is active, the file is also saved inside:

```text
Data/
```

---

## 35. Main Functions in the Code

| Function | Purpose |
|---|---|
| `parse_tickers()` | Converts comma-separated ticker input into a clean list of uppercase tickers. |
| `parse_weights()` | Converts, validates and normalises portfolio weights. |
| `format_percent()` | Formats percentage outputs. |
| `format_number()` | Formats numerical outputs. |
| `format_money()` | Formats monetary outputs. |
| `add_portfolio_value_columns()` | Adds initial allocated value, estimated shares, current value, gain/loss and current portfolio weight. |
| `download_prices()` | Downloads close prices for multiple tickers. |
| `calculate_asset_metrics()` | Calculates returns, volatility, drawdown and Sharpe Ratio per asset. |
| `calculate_portfolio_contribution()` | Calculates asset return contribution to portfolio return. |
| `create_cumulative_returns_chart()` | Creates the multi-asset cumulative returns chart. |
| `create_histogram_chart()` | Creates the histogram of daily returns. |
| `create_boxplot_chart()` | Creates the box plot of daily returns. |
| `create_correlation_heatmap()` | Creates the correlation heatmap. |
| `create_risk_return_scatter()` | Creates the risk-return scatter plot. |
| `create_portfolio_pie_chart()` | Creates the interactive allocation pie chart. |
| `create_waterfall_chart()` | Creates the portfolio return contribution waterfall. |
| `download_single_asset_ohlcv()` | Downloads OHLCV data for one selected asset. |
| `calculate_single_asset_detail()` | Calculates moving averages, returns, cumulative return and drawdown for one asset. |
| `create_single_asset_detail_chart()` | Creates the single-asset technical analysis chart. |
| `create_excel_file()` | Creates the Excel export file. |

---

## 36. Important Financial Assumptions

The dashboard makes several simplifying assumptions:

| Assumption | Explanation |
|---|---|
| Historical close prices | The multi-asset analysis uses close prices downloaded from Yahoo Finance. |
| Fractional shares allowed | Estimated shares may be fractional. |
| No transaction costs | Commissions and spreads are ignored. |
| No taxes | Tax effects are ignored. |
| No dividends modelled separately | The code uses the `Close` column with `auto_adjust=False`; dividend-adjusted analysis would require adjusted prices. |
| No FX conversion | If tickers trade in different currencies, the dashboard does not convert currencies. |
| No rebalancing | Portfolio return is based on starting weights and asset total returns. |
| Simplified Sharpe Ratio | The risk-free rate is not subtracted. |
| Historical analysis only | Results describe past performance, not future returns. |

---

## 37. Important Technical Notes

### Streamlit must be stopped before rerunning

If the app is already running and you change the file, stop it with:

```bash
CTRL + C
```

Then run again:

```bash
py -3.14 -m streamlit run Multi_Asset_Dashboard.py
```

### VS Code Run and Debug may run the wrong file

If Run and Debug opens an older version of the dashboard, check:

```text
.vscode/launch.json
```

The `
`args` section must point to the file you are currently editing:

```json
"args": [
  "run",
  "${workspaceFolder}/Multi_Asset_Dashboard.py"
]
```

If the file name is different, update it.

### Do not use Run Python File

Do not use:

```text
Run Python File
```

for Streamlit apps.

Use:

```bash
py -3.14 -m streamlit run Multi_Asset_Dashboard.py
```

or use the Run and Debug configuration above.

---

## 38. Common Errors and Fixes

### Error: number of weights must match number of valid tickers

Cause:

```text
The number of weights entered is different from the number of valid downloaded tickers.
```

Example:

```text
Tickers: AAPL, MSFT, FAKE
Weights: 40, 40, 20
```

If `FAKE` has no data, only two tickers remain valid. The app then expects two weights, not three.

Fix:

```text
Use only valid tickers or adjust the number of weights.
```

### Error: Streamlit opens an older version

Cause:

```text
VS Code launch.json is pointing to an older Python file.
```

Fix:

```text
Update .vscode/launch.json so it points to the correct file.
```

### Error: KeyError: 'Hover Text'

Cause:

```text
The code tries to use a column called Hover Text before creating it.
```

Fix:

```text
Use the updated allocation pie chart logic with Hover Details, or create the hover column before calling it.
```

### Pie chart shows different percentages than the sidebar

Cause:

```text
The pie chart may be using Current Value instead of Weight.
```

Fix:

For sidebar allocation weights, use:

```python
values=portfolio_df["Weight"]
```

For current market value weights, use:

```python
values=portfolio_df["Current Value"]
```

These two versions answer different financial questions.

---

## 39. How to Interpret the Dashboard Correctly

### Higher return is not always better

A stock may have a high return but also very high volatility and deep drawdowns.

Always compare:

```text
Return
Volatility
Sharpe Ratio
Maximum Drawdown
Correlation
Portfolio weight
Contribution
```

### Portfolio contribution matters

A stock's standalone return does not show how much it affected the portfolio.

The portfolio impact depends on both:

```text
Asset return
Portfolio weight
```

### Correlation matters for diversification

A group of high-return assets may still be risky if all assets move together.

Low correlation can improve diversification, but only when combined with acceptable returns and risk.

### Allocation drift matters

If one asset rises much more than the others, its current market weight increases.

Example:

```text
Initial AMD weight = 40%
Current AMD market weight = 45%
```

This means the portfolio has become more concentrated in AMD after price movements.

---

## 40. Limitations

This dashboard is for learning and analysis purposes only.

Important limitations:

- it is not investment advice;
- it depends on Yahoo Finance data quality;
- it does not guarantee real-time accuracy;
- it does not model bid-ask spreads;
- it does not model transaction fees;
- it does not model taxes;
- it does not handle dividends separately;
- it does not perform currency conversion;
- it does not optimise portfolio weights;
- it uses historical data and cannot predict future returns;
- Sharpe Ratio is simplified because the risk-free rate is not included;
- annualized return is based on average daily return multiplied by 252, not CAGR.

---

## 41. Possible Future Improvements

Possible future upgrades:

| Upgrade | Benefit |
|---|---|
| Add adjusted close prices | More accurate total return analysis when dividends and splits matter. |
| Add benchmark comparison | Compare the portfolio against SPY, QQQ or another benchmark. |
| Add CAGR | Better annual return measure for multi-year periods. |
| Add risk-free rate input | More complete Sharpe Ratio calculation. |
| Add Sortino Ratio | Measures downside risk instead of total volatility. |
| Add beta vs benchmark | Measures market sensitivity. |
| Add Value at Risk | Estimates potential loss under a confidence level. |
| Add CVaR | Estimates expected loss beyond VaR. |
| Add portfolio rebalancing | Compare buy-and-hold vs rebalanced strategies. |
| Add current value pie chart as a second chart | Separates initial allocation from current market allocation. |
| Add currency selector | Improves usability for international portfolios. |
| Add Streamlit theme customisation | Improves visual presentation. |
| Add error logs | Easier debugging. |
| Add README screenshots | Easier project documentation for GitHub. |

---


## 42. Final Notes

This project is a practical Python for Finance dashboard.

It combines:

```text
Data download
Data cleaning
Return calculation
Risk metrics
Portfolio value logic
Interactive visualisation
Financial interpretation
Excel export
```

The most important correction in the latest version is the allocation logic:

```python
values=portfolio_df["Weight"]
```

This makes the allocation pie chart reflect the weights entered in the sidebar.

The hover box still shows current market value information, including:

```text
Current Value Held
Gain/Loss
Current Market Weight in Full Portfolio
```

This gives two useful perspectives:

| Perspective | Where it appears |
|---|---|
| Initial allocation chosen by the user | Pie chart slices. |
| Current value after price movements | Hover box and allocation table. |

The dashboard therefore helps separate:

```text
What I allocated at the start
```

from:

```text
What the portfolio became after market movements
```
