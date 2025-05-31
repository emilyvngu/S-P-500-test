import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Set page title
st.title("Portfolio Visualization")

# Project Overview
st.markdown("""
### Project Overview: Portfolio Visualization

This page compares two investment strategies:  
- **SPY**, a market-wide index fund  
- An **equal-weighted portfolio** of the "Magnificent 7" tech stocks: AAPL, MSFT, AMZN, GOOGL, META, TSLA, and NVDA.

We simulate how $100 would grow under each strategy over time using **log returns** and **compounded returns**.

#### Methodology
- **Log returns** are used for daily price changes because they are time-additive and stable for financial modeling.
- **Cumulative log returns** are summed across time and then exponentiated to get the total compounded return.
- **Investment value** is calculated by multiplying compounded return by the initial $100.

#### Why Visualize This?
This helps compare how a diversified index fund performs versus a concentrated tech-heavy portfolio—highlighting trade-offs between **diversification**, **risk**, and **potential return**.
""")

# SPY visualization:
# Load SPY data
file_path = 'assets/sp500_raw_data.csv'

try:
    spy = pd.read_csv(file_path, index_col=0, parse_dates=True)
except FileNotFoundError:
    st.error(f"File not found: {file_path}")
    st.stop()

# Calculate Log Returns, Cumulative Log Returns, Compounded Returns, and Investment Value
spy['Adj Close'] = pd.to_numeric(spy['Adj Close'], errors='coerce')
spy['Log Returns'] = np.log(spy['Adj Close'] / spy['Adj Close'].shift(1))
spy['Cumulative Log Returns'] = spy['Log Returns'].cumsum()
spy['Compounded Return'] = np.exp(spy['Cumulative Log Returns'])
initial_investment = 100
spy['Investment Value'] = initial_investment * spy['Compounded Return']

# Equal-Weighted Portfolio visualization:
file_path = 'assets/mag7_adjclose_data.csv'

try:
    mag7_data = pd.read_csv(file_path, index_col=0, parse_dates=True)
except FileNotFoundError:
    st.error(f"File not found: {file_path}")
    st.stop()

tickers = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'TSLA', 'NVDA']
data = mag7_data.apply(pd.to_numeric, errors='coerce')
log_returns = np.log(data / data.shift(1))
weights = np.array([1 / len(tickers)] * len(tickers))
weighted_log_returns = log_returns.dot(weights)
cumulative_weighted_log_returns = weighted_log_returns.cumsum()
compounded_returns = np.exp(cumulative_weighted_log_returns)
investment_values = initial_investment * compounded_returns

# Combined plot
fig_combined = go.Figure()
fig_combined.add_trace(go.Scatter(x=spy.index, y=spy['Investment Value'], mode='lines', name='SPY'))
fig_combined.add_trace(go.Scatter(x=data.index, y=investment_values, mode='lines', name='Magnificent 7'))

fig_combined.update_layout(
    title="Portfolio Comparison: SPY vs. Magnificent 7 ($100 Investment)",
    xaxis_title="Time",
    yaxis_title="Investment Value ($)",
    template="plotly_white",
    legend_title="Portfolios"
)

st.plotly_chart(fig_combined)
