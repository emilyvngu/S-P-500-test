import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import os

# --- Page Title ---
st.title("Portfolio Visualization")

# --- SPY Data ---
spy_file_path = 'assets/sp500_raw_data.csv'

try:
    spy = pd.read_csv(spy_file_path, index_col=0, parse_dates=True)
except FileNotFoundError:
    st.error(f"File not found: {spy_file_path}")
    st.stop()

spy['Adj Close'] = pd.to_numeric(spy['Adj Close'], errors='coerce')
spy['Log Returns'] = np.log(spy['Adj Close'] / spy['Adj Close'].shift(1))
spy['Cumulative Log Returns'] = spy['Log Returns'].cumsum()
spy['Compounded Return'] = np.exp(spy['Cumulative Log Returns'])
initial_investment = 100
spy['Investment Value'] = initial_investment * spy['Compounded Return']

# --- Magnificent 7 Data ---
mag7_file_path = 'assets/mag7_adjclose_data.csv'

try:
    mag7_data = pd.read_csv(mag7_file_path, index_col=0, parse_dates=True)
except FileNotFoundError:
    st.error(f"File not found: {mag7_file_path}")
    st.stop()

tickers = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'TSLA', 'NVDA']
data = mag7_data.apply(pd.to_numeric, errors='coerce')

log_returns = np.log(data / data.shift(1))
weights = np.array([1 / len(tickers)] * len(tickers))
weighted_log_returns = log_returns.dot(weights)
cumulative_weighted_log_returns = weighted_log_returns.cumsum()
compounded_returns = np.exp(cumulative_weighted_log_returns)
investment_values = initial_investment * compounded_returns

# --- Combined Visualization ---
st.subheader("Portfolio Comparison: SPY vs. Magnificent 7")

fig_combined = go.Figure()

fig_combined.add_trace(
    go.Scatter(x=spy.index, y=spy['Investment Value'], mode='lines', name='SPY')
)
fig_combined.add_trace(
    go.Scatter(x=data.index, y=investment_values, mode='lines', name='Magnificent 7')
)

fig_combined.update_layout(
    title="Portfolio Growth Over Time ($100 Investment)",
    xaxis_title="Time",
    yaxis_title="Investment Value ($)",
    template="plotly_white",
    legend_title="Portfolio"
)

st.plotly_chart(fig_combined, use_container_width=True)

# Optional caption
st.caption("This chart compares the growth of a $100 investment in SPY vs. an equal-weighted Magnificent 7 portfolio.")

# --- Optional Explanatory Section ---
st.markdown("### Why This Visualization?")
st.markdown("""
This visualization highlights the difference in performance between a broad-market ETF (SPY) and a concentrated portfolio of high-growth tech stocks (the Magnificent 7).

By comparing cumulative log returns and compounding them into investment value, we gain insight into how portfolio composition impacts long-term growth. Log returns are used for their time-additive property, and compounding provides a real-world perspective on investment performance over time.
""")
