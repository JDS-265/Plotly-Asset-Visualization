from pathlib import Path
from io import BytesIO
from datetime import date

import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st


# ======================================================
# STREAMLIT MULTI-ASSET FINANCIAL DASHBOARD
# Multi-asset analysis + single-asset technical detail
# ======================================================


# -----------------------------
# 1. Page configuration
# -----------------------------
st.set_page_config(
    page_title="Multi-Asset Financial Dashboard",
    layout="wide"
)


# -----------------------------
# 2. Helper functions
# -----------------------------
def parse_tickers(tickers_input):
    if tickers_input.strip() == "":
        return ["UNH", "OKLO", "TSM", "AMD"]

    tickers = [
        ticker.strip().upper()
        for ticker in tickers_input.split(",")
        if ticker.strip() != ""
    ]

    return tickers


def parse_weights(weights_input, number_of_assets):
    if weights_input.strip() == "":
        equal_weight = 100 / number_of_assets
        return [equal_weight] * number_of_assets

    weights = [
        float(weight.strip())
        for weight in weights_input.split(",")
        if weight.strip() != ""
    ]

    if len(weights) != number_of_assets:
        raise ValueError(
            "The number of weights must match the number of valid tickers."
        )

    total_weight = sum(weights)

    if total_weight <= 0:
        raise ValueError("Total weight must be greater than zero.")

    normalized_weights = [(weight / total_weight) * 100 for weight in weights]

    return normalized_weights


def format_percent(value):
    if pd.isna(value):
        return "N/A"
    return f"{value:.2%}"


def format_number(value):
    if pd.isna(value):
        return "N/A"
    return f"{value:,.2f}"


def format_money(value):
    if pd.isna(value):
        return "N/A"
    return f"{value:,.2f}"


def add_portfolio_value_columns(contribution_df, portfolio_value):
    """
    Add monetary portfolio columns using the sidebar Portfolio value as
    the initial capital invested at the selected start date.

    Financial logic:
    Initial allocated value = portfolio_value * initial weight
    Estimated shares = initial allocated value / first price
    Current value = estimated shares * last price
    Gain/Loss = current value - initial allocated value
    """
    portfolio_df = contribution_df.copy()

    portfolio_df["Initial Allocated Value"] = (
        portfolio_value * (portfolio_df["Weight"] / 100)
    )

    portfolio_df["Estimated Shares"] = (
        portfolio_df["Initial Allocated Value"] / portfolio_df["First Price"]
    )

    portfolio_df["Current Value"] = (
        portfolio_df["Estimated Shares"] * portfolio_df["Last Price"]
    )

    portfolio_df["Gain/Loss"] = (
        portfolio_df["Current Value"] - portfolio_df["Initial Allocated Value"]
    )

    current_total_value = portfolio_df["Current Value"].sum()

    if current_total_value != 0:
        portfolio_df["Current Portfolio Weight"] = (
            portfolio_df["Current Value"] / current_total_value
        ) * 100
    else:
        portfolio_df["Current Portfolio Weight"] = float("nan")

    return portfolio_df


@st.cache_data(show_spinner=False)
def download_prices(tickers, start_date):
    prices = pd.DataFrame()
    skipped_tickers = []

    for ticker in tickers:
        stock = yf.Ticker(ticker)

        df = stock.history(
            start=start_date,
            auto_adjust=False
        )

        if df.empty:
            skipped_tickers.append(ticker)
            continue

        if df.index.tz is not None:
            df.index = df.index.tz_localize(None)

        prices[ticker] = df["Close"]

    if prices.empty:
        return pd.DataFrame(), skipped_tickers

    prices = prices.dropna(how="all")
    prices = prices.ffill()
    prices = prices.dropna()

    return prices, skipped_tickers


def calculate_asset_metrics(prices):
    daily_returns = prices.pct_change().dropna()
    cumulative_returns = (1 + daily_returns).cumprod() - 1

    metrics_rows = []

    for ticker in daily_returns.columns:
        first_price = prices[ticker].iloc[0]
        last_price = prices[ticker].iloc[-1]

        total_return = (last_price / first_price) - 1

        average_daily_return = daily_returns[ticker].mean()
        daily_volatility = daily_returns[ticker].std()

        annualized_return = average_daily_return * 252
        annualized_volatility = daily_volatility * (252 ** 0.5)

        cumulative_wealth = (1 + daily_returns[ticker]).cumprod()
        running_max = cumulative_wealth.cummax()
        drawdown = (cumulative_wealth / running_max) - 1
        maximum_drawdown = drawdown.min()

        if pd.notna(annualized_volatility) and annualized_volatility != 0:
            sharpe_ratio = annualized_return / annualized_volatility
        else:
            sharpe_ratio = float("nan")

        metrics_rows.append({
            "Ticker": ticker,
            "First Price": first_price,
            "Last Price": last_price,
            "Total Return": total_return,
            "Average Daily Return": average_daily_return,
            "Annualized Return": annualized_return,
            "Daily Volatility": daily_volatility,
            "Annualized Volatility": annualized_volatility,
            "Maximum Drawdown": maximum_drawdown,
            "Sharpe Ratio": sharpe_ratio
        })

    metrics_df = pd.DataFrame(metrics_rows)

    return daily_returns, cumulative_returns, metrics_df


def calculate_portfolio_contribution(prices, weights):
    portfolio_rows = []

    for ticker, weight in zip(prices.columns, weights):
        weight_decimal = weight / 100

        first_price = prices[ticker].iloc[0]
        last_price = prices[ticker].iloc[-1]

        asset_return = (last_price / first_price) - 1
        return_contribution = weight_decimal * asset_return

        latest_price = last_price

        portfolio_rows.append({
            "Ticker": ticker,
            "Weight": weight,
            "First Price": first_price,
            "Last Price": last_price,
            "Latest Close Price": latest_price,
            "Asset Return": asset_return,
            "Return Contribution": return_contribution
        })

    contribution_df = pd.DataFrame(portfolio_rows)
    portfolio_total_return = contribution_df["Return Contribution"].sum()

    return contribution_df, portfolio_total_return


# -----------------------------
# 3. Chart functions
# -----------------------------
def create_cumulative_returns_chart(cumulative_returns):
    fig = go.Figure()

    for ticker in cumulative_returns.columns:
        fig.add_trace(
            go.Scatter(
                x=cumulative_returns.index,
                y=cumulative_returns[ticker],
                mode="lines",
                name=ticker,
                line=dict(width=2)
            )
        )

    fig.add_hline(
        y=0,
        line_width=2,
        line_dash="dash",
        annotation_text="0% Return",
        annotation_position="top left"
    )

    fig.update_layout(
        title="Multi-Asset Cumulative Returns",
        xaxis_title="Date",
        yaxis_title="Cumulative Return",
        template="plotly_white",
        height=650,
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        )
    )

    fig.update_yaxes(tickformat=".0%")

    return fig


def create_histogram_chart(daily_returns, selected_ticker):
    returns = daily_returns[selected_ticker].dropna()
    mean_return = returns.mean()

    fig = go.Figure()

    fig.add_trace(
        go.Histogram(
            x=returns,
            nbinsx=50,
            name="Daily Returns",
            opacity=0.75
        )
    )

    fig.add_vline(
        x=mean_return,
        line_width=2,
        line_dash="dash",
        annotation_text="Mean",
        annotation_position="top"
    )

    fig.update_layout(
        title=f"{selected_ticker} - Histogram of Daily Returns",
        xaxis_title="Daily Return",
        yaxis_title="Frequency",
        template="plotly_white",
        height=550,
        bargap=0.05
    )

    fig.update_xaxes(tickformat=".1%")

    return fig


def create_boxplot_chart(daily_returns, selected_ticker):
    returns = daily_returns[selected_ticker].dropna()

    fig = go.Figure()

    fig.add_trace(
        go.Box(
            y=returns,
            name=f"{selected_ticker} Daily Returns",
            boxmean=True,
            boxpoints="outliers",
            marker=dict(size=6)
        )
    )

    fig.add_hline(
        y=0,
        line_width=2,
        line_dash="dash",
        annotation_text="0% Return",
        annotation_position="top left"
    )

    fig.update_layout(
        title=f"{selected_ticker} - Box Plot of Daily Returns",
        yaxis_title="Daily Return",
        template="plotly_white",
        height=550,
        showlegend=False
    )

    fig.update_yaxes(tickformat=".1%")

    return fig


def create_correlation_heatmap(daily_returns):
    correlation_matrix = daily_returns.corr()

    fig = go.Figure()

    fig.add_trace(
        go.Heatmap(
            z=correlation_matrix.values,
            x=correlation_matrix.columns,
            y=correlation_matrix.index,
            zmin=-1,
            zmax=1,
            zmid=0,
            colorscale="RdBu",
            text=correlation_matrix.round(2).astype(str).values,
            texttemplate="%{text}",
            hovertemplate=(
                "Ticker X: %{x}<br>"
                "Ticker Y: %{y}<br>"
                "Correlation: %{z:.2f}<extra></extra>"
            ),
            colorbar=dict(title="Correlation")
        )
    )

    fig.update_layout(
        title="Correlation Heatmap - Daily Returns",
        xaxis_title="Ticker",
        yaxis_title="Ticker",
        template="plotly_white",
        height=700
    )

    return fig


def create_risk_return_scatter(metrics_df):
    marker_size = metrics_df["Sharpe Ratio"].abs().fillna(0) * 20 + 15
    marker_color = metrics_df["Sharpe Ratio"].fillna(0)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=metrics_df["Annualized Volatility"],
            y=metrics_df["Annualized Return"],
            mode="markers+text",
            text=metrics_df["Ticker"],
            textposition="top center",
            marker=dict(
                size=marker_size,
                color=marker_color,
                colorscale="Viridis",
                showscale=True,
                colorbar=dict(title="Sharpe Ratio"),
                line=dict(width=1)
            ),
            customdata=metrics_df[
                [
                    "Ticker",
                    "Total Return",
                    "Sharpe Ratio",
                    "First Price",
                    "Last Price"
                ]
            ],
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "Annualized Volatility: %{x:.2%}<br>"
                "Annualized Return: %{y:.2%}<br>"
                "Total Return: %{customdata[1]:.2%}<br>"
                "Sharpe Ratio: %{customdata[2]:.2f}<br>"
                "First Price: %{customdata[3]:.2f}<br>"
                "Last Price: %{customdata[4]:.2f}"
                "<extra></extra>"
            )
        )
    )

    fig.add_hline(
        y=0,
        line_width=2,
        line_dash="dash",
        annotation_text="0% Return",
        annotation_position="top left"
    )

    average_volatility = metrics_df["Annualized Volatility"].mean()

    fig.add_vline(
        x=average_volatility,
        line_width=2,
        line_dash="dash",
        annotation_text="Average Volatility",
        annotation_position="top"
    )

    fig.update_layout(
        title="Risk-Return Scatter Plot",
        xaxis_title="Annualized Volatility",
        yaxis_title="Annualized Return",
        template="plotly_white",
        height=700,
        hovermode="closest"
    )

    fig.update_xaxes(tickformat=".0%")
    fig.update_yaxes(tickformat=".0%")

    return fig


def create_portfolio_pie_chart(contribution_df, portfolio_value):
    portfolio_df = add_portfolio_value_columns(contribution_df, portfolio_value)

    portfolio_initial_value = portfolio_df["Initial Allocated Value"].sum()
    portfolio_current_value = portfolio_df["Current Value"].sum()
    portfolio_gain_loss = portfolio_current_value - portfolio_initial_value
    portfolio_total_return = (
        portfolio_current_value / portfolio_initial_value - 1
        if portfolio_initial_value != 0
        else float("nan")
    )

    # Build pre-formatted hover text instead of relying on indexed customdata.
    # This is more reliable for Plotly pie charts and prevents NaN / '-' values
    # from appearing in the tooltip.
    hover_text = []

    for _, row in portfolio_df.iterrows():
        hover_text.append(
            f"<b>{row['Ticker']}</b><br>"
            f"Initial Weight: {row['Weight']:.2f}%<br>"
            f"Initial Allocated Value: {format_money(row['Initial Allocated Value'])}<br>"
            f"Asset Return Since Start: {format_percent(row['Asset Return'])}<br>"
            f"Current Value Held: {format_money(row['Current Value'])}<br>"
            f"Gain/Loss: {format_money(row['Gain/Loss'])}<br>"
            f"First Price: {format_money(row['First Price'])}<br>"
            f"Latest Close Price: {format_money(row['Last Price'])}<br>"
            f"Estimated Shares Bought: {row['Estimated Shares']:,.4f}<br>"
            f"Current Portfolio Weight: {row['Current Portfolio Weight']:.2f}%"
        )

    fig = go.Figure()

    fig.add_trace(
        go.Pie(
            labels=portfolio_df["Ticker"],
            # Current Value makes the pie chart show the portfolio allocation today.
            # The initial allocation is still visible in the hover tooltip.
            values=portfolio_df["Current Value"],
            hole=0.35,
            textinfo="label+percent",
            hovertext=hover_text,
            hoverinfo="text",
            sort=False
        )
    )

    fig.update_layout(
        title=(
            "Portfolio Allocation Pie Chart - Current Value"
            f"<br><sup>Initial Portfolio Value: {portfolio_initial_value:,.2f} | "
            f"Current Portfolio Value: {portfolio_current_value:,.2f} | "
            f"Gain/Loss: {portfolio_gain_loss:,.2f} | "
            f"Total Return: {portfolio_total_return:.2%}</sup>"
        ),
        template="plotly_white",
        height=650,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.05,
            xanchor="center",
            x=0.5
        )
    )

    return fig

def create_waterfall_chart(contribution_df, portfolio_total_return, portfolio_value):
    contribution_df = add_portfolio_value_columns(contribution_df, portfolio_value)

    portfolio_initial_value = contribution_df["Initial Allocated Value"].sum()
    portfolio_final_value = contribution_df["Current Value"].sum()
    portfolio_gain_loss = contribution_df["Gain/Loss"].sum()

    waterfall_labels = list(contribution_df["Ticker"]) + ["Portfolio Total"]
    waterfall_values = list(contribution_df["Return Contribution"]) + [portfolio_total_return]
    waterfall_measures = ["relative"] * len(contribution_df) + ["total"]

    waterfall_text = [
        f"{value:.2%}" for value in contribution_df["Return Contribution"]
    ] + [f"{portfolio_total_return:.2%}"]

    customdata = []

    for _, row in contribution_df.iterrows():
        customdata.append([
            row["Ticker"],
            row["Weight"],
            row["Asset Return"],
            row["Return Contribution"],
            row["Initial Allocated Value"],
            row["Current Value"],
            row["Gain/Loss"]
        ])

    customdata.append([
        "Portfolio Total",
        100.0,
        portfolio_total_return,
        portfolio_total_return,
        portfolio_initial_value,
        portfolio_final_value,
        portfolio_gain_loss
    ])

    fig = go.Figure()

    fig.add_trace(
        go.Waterfall(
            x=waterfall_labels,
            y=waterfall_values,
            measure=waterfall_measures,
            text=waterfall_text,
            textposition="outside",
            customdata=customdata,
            connector=dict(
                line=dict(width=1)
            ),
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "Weight: %{customdata[1]:.2f}%<br>"
                "Asset / Portfolio Return: %{customdata[2]:.2%}<br>"
                "Return Contribution: %{customdata[3]:.2%}<br>"
                "Initial Value: %{customdata[4]:,.2f}<br>"
                "Current Value: %{customdata[5]:,.2f}<br>"
                "Gain/Loss: %{customdata[6]:,.2f}"
                "<extra></extra>"
            )
        )
    )

    fig.add_hline(
        y=0,
        line_width=2,
        line_dash="dash",
        annotation_text="0%",
        annotation_position="top left"
    )

    fig.update_layout(
        title=(
            "Portfolio Return Contribution Waterfall"
            f"<br><sup>Total Return: {portfolio_total_return:.2%}</sup>"
        ),
        xaxis_title="Assets",
        yaxis_title="Return Contribution",
        template="plotly_white",
        height=700,
        showlegend=False
    )

    fig.update_yaxes(tickformat=".0%")

    return fig, contribution_df


# -----------------------------
# 4. Single asset detail functions
# -----------------------------
@st.cache_data(show_spinner=False)
def download_single_asset_ohlcv(ticker, start_date):
    stock = yf.Ticker(ticker)

    df = stock.history(
        start=start_date,
        auto_adjust=False
    )

    if df.empty:
        return pd.DataFrame()

    if df.index.tz is not None:
        df.index = df.index.tz_localize(None)

    df = df.reset_index()

    if "Datetime" in df.columns:
        df = df.rename(columns={"Datetime": "Date"})

    return df


def calculate_single_asset_detail(df):
    df = df.copy()

    df["MA20"] = df["Close"].rolling(window=20).mean()
    df["MA50"] = df["Close"].rolling(window=50).mean()

    daily_returns_raw = df["Close"].pct_change()

    df["Daily_Return"] = daily_returns_raw.fillna(0)
    df["Cumulative_Return"] = (1 + df["Daily_Return"]).cumprod() - 1

    df["Cumulative_Wealth"] = (1 + df["Daily_Return"]).cumprod()
    df["Running_Max"] = df["Cumulative_Wealth"].cummax()
    df["Drawdown"] = (df["Cumulative_Wealth"] / df["Running_Max"]) - 1

    returns_clean = daily_returns_raw.dropna()

    first_close = df["Close"].iloc[0]
    last_close = df["Close"].iloc[-1]

    total_return = (last_close / first_close) - 1
    average_daily_return = returns_clean.mean()
    daily_volatility = returns_clean.std()

    annualized_return = average_daily_return * 252
    annualized_volatility = daily_volatility * (252 ** 0.5)

    maximum_drawdown = df["Drawdown"].min()

    if pd.notna(annualized_volatility) and annualized_volatility != 0:
        sharpe_ratio = annualized_return / annualized_volatility
    else:
        sharpe_ratio = float("nan")

    metrics = {
        "First Close Price": first_close,
        "Last Close Price": last_close,
        "Total Return": total_return,
        "Average Daily Return": average_daily_return,
        "Annualized Return": annualized_return,
        "Daily Volatility": daily_volatility,
        "Annualized Volatility": annualized_volatility,
        "Maximum Drawdown": maximum_drawdown,
        "Sharpe Ratio": sharpe_ratio
    }

    return df, metrics


def create_single_asset_detail_chart(df, ticker, metrics):
    fig = make_subplots(
        rows=4,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.055,
        row_heights=[0.50, 0.18, 0.17, 0.15],
        subplot_titles=(
            "",
            "Trading Volume",
            "Cumulative Return",
            "Drawdown"
        )
    )

    fig.add_trace(
        go.Candlestick(
            x=df["Date"],
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name=f"{ticker} OHLC"
        ),
        row=1,
        col=1
    )

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["MA20"],
            mode="lines",
            name="MA20 - 20 Day Moving Average",
            line=dict(width=2)
        ),
        row=1,
        col=1
    )

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["MA50"],
            mode="lines",
            name="MA50 - 50 Day Moving Average",
            line=dict(width=2)
        ),
        row=1,
        col=1
    )

    fig.add_trace(
        go.Bar(
            x=df["Date"],
            y=df["Volume"],
            name="Volume",
            opacity=0.65
        ),
        row=2,
        col=1
    )

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Cumulative_Return"],
            mode="lines",
            name="Cumulative Return",
            line=dict(width=2)
        ),
        row=3,
        col=1
    )

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Drawdown"],
            mode="lines",
            name="Drawdown",
            fill="tozeroy",
            line=dict(width=2)
        ),
        row=4,
        col=1
    )

    fig.update_layout(
        title=dict(
            text=(
                f"{ticker} Single Asset Detail"
                f"<br><sup>"
                f"Total Return: {format_percent(metrics['Total Return'])} | "
                f"Annualized Return: {format_percent(metrics['Annualized Return'])} | "
                f"Annualized Volatility: {format_percent(metrics['Annualized Volatility'])} | "
                f"Max Drawdown: {format_percent(metrics['Maximum Drawdown'])} | "
                f"Sharpe Ratio: {metrics['Sharpe Ratio']:.2f}"
                f"</sup>"
            ),
            x=0.5,
            xanchor="center",
            y=0.98,
            yanchor="top"
        ),
        template="plotly_white",
        height=1100,
        hovermode="x unified",
        margin=dict(l=80, r=50, t=160, b=70),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        )
    )

    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    fig.update_yaxes(title_text="Return", tickformat=".0%", row=3, col=1)
    fig.update_yaxes(title_text="Drawdown", tickformat=".0%", row=4, col=1)
    fig.update_xaxes(title_text="Date", row=4, col=1)

    fig.update_xaxes(
        rangeslider_visible=False,
        rangeselector=dict(
            x=0,
            y=1.10,
            xanchor="left",
            yanchor="top",
            buttons=[
                dict(count=1, label="1M", step="month", stepmode="backward"),
                dict(count=3, label="3M", step="month", stepmode="backward"),
                dict(count=6, label="6M", step="month", stepmode="backward"),
                dict(count=1, label="1Y", step="year", stepmode="backward"),
                dict(step="all", label="All")
            ]
        ),
        row=1,
        col=1
    )

    return fig


# -----------------------------
# 5. Excel export function
# -----------------------------
def create_excel_file(
    prices,
    daily_returns,
    cumulative_returns,
    metrics_df,
    correlation_matrix,
    contribution_df
):
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        prices.to_excel(writer, sheet_name="Prices")
        daily_returns.to_excel(writer, sheet_name="Daily Returns")
        cumulative_returns.to_excel(writer, sheet_name="Cumulative Returns")
        metrics_df.to_excel(writer, sheet_name="Metrics", index=False)
        correlation_matrix.to_excel(writer, sheet_name="Correlation")
        contribution_df.to_excel(
            writer,
            sheet_name="Portfolio Contribution",
            index=False
        )

    output.seek(0)

    return output.getvalue()


# -----------------------------
# 6. Sidebar inputs
# -----------------------------
st.sidebar.title("Dashboard Settings")

tickers_input = st.sidebar.text_input(
    "Tickers",
    value="AAPL, MSFT, AMZN, TSLA, NVDA",
    help="Separate tickers with commas."
)

start_date = st.sidebar.date_input(
    "Start date",
    value=date(2024, 1, 1)
)

weights_input = st.sidebar.text_input(
    "Portfolio weights (%)",
    value="",
    help="Example: 30, 25, 20, 15, 10. Leave blank for equal weights."
)

portfolio_value = st.sidebar.number_input(
    "Portfolio value",
    min_value=1.0,
    value=10000.0,
    step=1000.0
)

save_excel_to_data_folder = st.sidebar.checkbox(
    "Save Excel file to Data folder",
    value=True
)


# -----------------------------
# 7. Main app
# -----------------------------
st.title("Multi-Asset Financial Dashboard")

st.write(
    """
    This dashboard combines several Plotly finance charts:
    cumulative returns, histogram, box plot, correlation heatmap,
    risk-return scatter, portfolio allocation pie chart, waterfall contribution,
    and detailed single-asset technical analysis.
    """
)

tickers = parse_tickers(tickers_input)

if len(tickers) == 0:
    st.error("Please enter at least one valid ticker.")
    st.stop()


# -----------------------------
# 8. Download multi-asset data
# -----------------------------
with st.spinner("Downloading stock data..."):
    prices, skipped_tickers = download_prices(
        tuple(tickers),
        start_date.strftime("%Y-%m-%d")
    )

if skipped_tickers:
    st.warning(f"Skipped tickers with no data: {', '.join(skipped_tickers)}")

if prices.empty:
    st.error("No valid price data was downloaded.")
    st.stop()

valid_tickers = list(prices.columns)

try:
    weights = parse_weights(weights_input, len(valid_tickers))
except ValueError as error:
    st.error(str(error))
    st.stop()


# -----------------------------
# 9. Calculate multi-asset data
# -----------------------------
daily_returns, cumulative_returns, metrics_df = calculate_asset_metrics(prices)

contribution_df, portfolio_total_return = calculate_portfolio_contribution(
    prices,
    weights
)

best_sharpe = metrics_df.sort_values("Sharpe Ratio", ascending=False).iloc[0]
highest_return = metrics_df.sort_values("Annualized Return", ascending=False).iloc[0]
highest_volatility = metrics_df.sort_values("Annualized Volatility", ascending=False).iloc[0]

correlation_matrix = daily_returns.corr()

portfolio_initial_value = portfolio_value
portfolio_current_value = portfolio_initial_value * (1 + portfolio_total_return)
portfolio_gain_loss = portfolio_current_value - portfolio_initial_value


# -----------------------------
# 10. Key metrics
# -----------------------------
st.subheader("Portfolio Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Valid Assets", len(valid_tickers))
col2.metric("Portfolio Total Return", format_percent(portfolio_total_return))
col3.metric(
    "Best Sharpe",
    f"{best_sharpe['Ticker']} ({best_sharpe['Sharpe Ratio']:.2f})"
)
col4.metric(
    "Highest Volatility",
    f"{highest_volatility['Ticker']} "
    f"({format_percent(highest_volatility['Annualized Volatility'])})"
)

col5, col6, col7, col8 = st.columns(4)

col5.metric(
    "Highest Annualized Return",
    f"{highest_return['Ticker']} "
    f"({format_percent(highest_return['Annualized Return'])})"
)
col6.metric("Start Date", str(prices.index[0].date()))
col7.metric("End Date", str(prices.index[-1].date()))
col8.metric(
    "Current Portfolio Value",
    format_money(portfolio_current_value),
    delta=format_percent(portfolio_total_return)
)


# -----------------------------
# 11. Tabs
# -----------------------------
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(
    [
        "Performance",
        "Distribution",
        "Correlation",
        "Risk-Return",
        "Allocation",
        "Contribution",
        "Single Asset Detail",
        "Data & Export"
    ]
)


# -----------------------------
# Tab 1 - Performance
# -----------------------------
with tab1:
    st.subheader("Portfolio Value Evolution")

    perf_col1, perf_col2, perf_col3, perf_col4 = st.columns(4)

    perf_col1.metric(
        "Initial Portfolio Value",
        format_money(portfolio_initial_value)
    )

    perf_col2.metric(
        "Current Portfolio Value",
        format_money(portfolio_current_value),
        delta=format_percent(portfolio_total_return)
    )

    perf_col3.metric(
        "Portfolio Gain/Loss",
        format_money(portfolio_gain_loss)
    )

    perf_col4.metric(
        "Portfolio Total Return",
        format_percent(portfolio_total_return)
    )

    st.write(
        "Current Portfolio Value = Initial Portfolio Value × (1 + Portfolio Total Return)."
    )

    st.subheader("Multi-Asset Cumulative Returns")

    fig = create_cumulative_returns_chart(cumulative_returns)

    st.plotly_chart(
        fig,
        width="stretch",
        config={
            "displayModeBar": True,
            "scrollZoom": True
        }
    )

    st.write(
        """
        This chart compares asset performance using cumulative returns.
        All assets start at 0%, which makes comparison fairer than using raw prices.
        """
    )


# -----------------------------
# Tab 2 - Distribution
# -----------------------------
with tab2:
    st.subheader("Return Distribution")

    selected_ticker = st.selectbox(
        "Select ticker for distribution analysis",
        valid_tickers
    )

    col_hist, col_box = st.columns(2)

    with col_hist:
        hist_fig = create_histogram_chart(daily_returns, selected_ticker)

        st.plotly_chart(
            hist_fig,
            width="stretch",
            config={
                "displayModeBar": True,
                "scrollZoom": True
            }
        )

    with col_box:
        box_fig = create_boxplot_chart(daily_returns, selected_ticker)

        st.plotly_chart(
            box_fig,
            width="stretch",
            config={
                "displayModeBar": True,
                "scrollZoom": True
            }
        )

    st.write(
        """
        The histogram shows the frequency of daily returns.
        The box plot summarises median, dispersion and outliers.
        """
    )


# -----------------------------
# Tab 3 - Correlation
# -----------------------------
with tab3:
    st.subheader("Correlation Heatmap")

    if len(valid_tickers) < 2:
        st.info("Correlation heatmap requires at least two valid tickers.")
    else:
        corr_fig = create_correlation_heatmap(daily_returns)

        st.plotly_chart(
            corr_fig,
            width="stretch",
            config={
                "displayModeBar": True,
                "scrollZoom": True
            }
        )

        st.write(
            """
            Correlation measures how assets move together.
            High correlation means lower diversification benefit.
            Lower correlation may improve diversification.
            """
        )


# -----------------------------
# Tab 4 - Risk-Return
# -----------------------------
with tab4:
    st.subheader("Risk-Return Scatter Plot")

    risk_return_fig = create_risk_return_scatter(metrics_df)

    st.plotly_chart(
        risk_return_fig,
        width="stretch",
        config={
            "displayModeBar": True,
            "scrollZoom": True
        }
    )

    st.write(
        """
        The X-axis shows annualized volatility.
        The Y-axis shows annualized return.
        Colour and marker size are based on Sharpe Ratio.
        """
    )


# -----------------------------
# Tab 5 - Allocation
# -----------------------------
with tab5:
    st.subheader("Portfolio Allocation")

    pie_fig = create_portfolio_pie_chart(contribution_df, portfolio_value)

    st.plotly_chart(
        pie_fig,
        width="stretch",
        config={
            "displayModeBar": True,
            "scrollZoom": True
        }
    )

    allocation_display_df = add_portfolio_value_columns(
        contribution_df,
        portfolio_value
    )[
        [
            "Ticker",
            "Weight",
            "Initial Allocated Value",
            "Asset Return",
            "Current Value",
            "Gain/Loss",
            "Estimated Shares",
            "First Price",
            "Last Price",
            "Current Portfolio Weight"
        ]
    ].copy()

    with st.expander("View portfolio allocation values"):
        st.dataframe(allocation_display_df, width="stretch")

    st.write(
        """
        The pie chart shows the initial allocation based on the portfolio weights.
        Hover over each slice to see the initial allocated value, current value held,
        estimated shares, gain/loss and current portfolio weight.
        """
    )


# -----------------------------
# Tab 6 - Contribution
# -----------------------------
with tab6:
    st.subheader("Portfolio Return Contribution")

    waterfall_fig, contribution_detail_df = create_waterfall_chart(
        contribution_df,
        portfolio_total_return,
        portfolio_value
    )

    st.plotly_chart(
        waterfall_fig,
        width="stretch",
        config={
            "displayModeBar": True,
            "scrollZoom": True
        }
    )

    st.write(
        """
        The waterfall chart shows how each asset contributed to the total portfolio return.
        Contribution is calculated as portfolio weight multiplied by asset return.
        """
    )


# -----------------------------
# Tab 7 - Single Asset Detail
# -----------------------------
with tab7:
    st.subheader("Single Asset Detail")

    selected_detail_ticker = st.selectbox(
        "Select ticker for detailed single-asset analysis",
        valid_tickers,
        key="single_asset_detail_ticker"
    )

    with st.spinner(f"Downloading OHLCV data for {selected_detail_ticker}..."):
        single_raw_df = download_single_asset_ohlcv(
            selected_detail_ticker,
            start_date.strftime("%Y-%m-%d")
        )

    if single_raw_df.empty:
        st.error("No OHLCV data found for the selected ticker.")
    else:
        single_df, single_metrics = calculate_single_asset_detail(single_raw_df)

        st.write(
            """
            This tab combines the single-stock technical view with the multi-asset dashboard.
            It shows candlesticks, moving averages, volume, cumulative return and drawdown.
            """
        )

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric(
            "Last Close",
            format_number(single_metrics["Last Close Price"])
        )

        col2.metric(
            "Total Return",
            format_percent(single_metrics["Total Return"])
        )

        col3.metric(
            "Annualized Volatility",
            format_percent(single_metrics["Annualized Volatility"])
        )

        col4.metric(
            "Maximum Drawdown",
            format_percent(single_metrics["Maximum Drawdown"])
        )

        col5.metric(
            "Sharpe Ratio",
            f"{single_metrics['Sharpe Ratio']:.2f}"
        )

        single_detail_fig = create_single_asset_detail_chart(
            single_df,
            selected_detail_ticker,
            single_metrics
        )

        st.plotly_chart(
            single_detail_fig,
            width="stretch",
            config={
                "displayModeBar": True,
                "scrollZoom": True
            }
        )

        with st.expander("View single-asset daily data"):
            single_display_df = single_df[
                [
                    "Date",
                    "Open",
                    "High",
                    "Low",
                    "Close",
                    "Volume",
                    "MA20",
                    "MA50",
                    "Daily_Return",
                    "Cumulative_Return",
                    "Drawdown"
                ]
            ].copy()

            st.dataframe(single_display_df, width="stretch")


# -----------------------------
# Tab 8 - Data & Export
# -----------------------------
with tab8:
    st.subheader("Data and Export")

    waterfall_fig, contribution_detail_df = create_waterfall_chart(
        contribution_df,
        portfolio_total_return,
        portfolio_value
    )

    excel_bytes = create_excel_file(
        prices,
        daily_returns,
        cumulative_returns,
        metrics_df,
        correlation_matrix,
        contribution_detail_df
    )

    safe_tickers = "_".join(valid_tickers)
    safe_start_date = start_date.strftime("%Y_%m_%d")
    excel_filename = f"{safe_tickers}_{safe_start_date}_multi_asset_dashboard.xlsx"

    if save_excel_to_data_folder:
        project_folder = Path(__file__).resolve().parent
        data_folder = project_folder / "Data"
        data_folder.mkdir(exist_ok=True)

        excel_path = data_folder / excel_filename

        with open(excel_path, "wb") as file:
            file.write(excel_bytes)

        st.success(f"Excel file saved in: {excel_path}")

    st.download_button(
        label="Download Excel file",
        data=excel_bytes,
        file_name=excel_filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    with st.expander("View portfolio value summary"):
        portfolio_summary_df = pd.DataFrame(
            [
                {
                    "Initial Portfolio Value": portfolio_initial_value,
                    "Current Portfolio Value": portfolio_current_value,
                    "Portfolio Gain/Loss": portfolio_gain_loss,
                    "Portfolio Total Return": portfolio_total_return
                }
            ]
        )
        st.dataframe(portfolio_summary_df, width="stretch")

    with st.expander("View asset metrics"):
        metrics_display_df = metrics_df.copy()
        st.dataframe(metrics_display_df, width="stretch")

    with st.expander("View portfolio contribution"):
        contribution_display_df = contribution_detail_df.copy()
        st.dataframe(contribution_display_df, width="stretch")

    with st.expander("View prices"):
        st.dataframe(prices, width="stretch")

    with st.expander("View daily returns"):
        st.dataframe(daily_returns, width="stretch")

    with st.expander("View correlation matrix"):
        st.dataframe(correlation_matrix, width="stretch")


# -----------------------------
# 12. Final notes
# -----------------------------
st.warning(
    """
    This dashboard is for learning and analysis purposes only.
    It is not investment advice.
    Results depend on the selected tickers, weights, time period and data quality.
    """
)