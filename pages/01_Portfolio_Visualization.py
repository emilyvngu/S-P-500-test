import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Set page title
st.title("Portfolio Visualization")

# Set the header for SPY visualization
st.header("SPY: Growth of $100 Investment")

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

# Plot the Investment Value over time using Plotly
fig_spy = go.Figure()
fig_spy.add_trace(go.Scatter(x=spy.index, y=spy['Investment Value'], mode='lines', name='SPY Investment'))
fig_spy.update_layout(
    title="Principal Growth over Time for SPY ($100 Investment)",
    xaxis_title="Time",
    yaxis_title="Investment Value ($)",
    template="plotly_white"
)
st.plotly_chart(fig_spy)

# Set the header for the Equal-Weighted Portfolio visualization
st.header("Magnificent 7: Equal-Weighted Portfolio")

file_path = '/assets/mag7_adjclose_data.csv'

try:
    mag7_data = pd.read_csv(file_path, index_col=0, parse_dates=True)
except FileNotFoundError:
    st.error(f"File not found: {file_path}")
    st.stop()

tickers = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'TSLA', 'NVDA']

# Convert the values to numeric (if needed)
data = mag7_data.apply(pd.to_numeric, errors='coerce')

# Calculate Log Returns
log_returns = np.log(data / data.shift(1))

# Define equal weights for the portfolio
weights = np.array([1 / len(tickers)] * len(tickers))

# Calculate weighted log returns for the portfolio
weighted_log_returns = log_returns.dot(weights)

# Calculate cumulative weighted log returns and convert to actual returns
cumulative_weighted_log_returns = weighted_log_returns.cumsum()
compounded_returns = np.exp(cumulative_weighted_log_returns)

# Calculate Investment Value
investment_values = initial_investment * compounded_returns

# Plot the growth of the $100 investment using Plotly
fig_portfolio = go.Figure()
fig_portfolio.add_trace(go.Scatter(x=data.index, y=investment_values, mode='lines', name='Equal-Weighted Portfolio', line=dict(color='red')))
fig_portfolio.update_layout(
    title="Principal Growth: Magnificent 7 Equal-Weighted Portfolio ($100 Investment)",
    xaxis_title="Time",
    yaxis_title="Investment Value ($)",
    template="plotly_white"
)
st.plotly_chart(fig_portfolio)

fig_combined = go.Figure()

# Add SPY line
fig_combined.add_trace(
    go.Scatter(x=spy.index, y=spy['Investment Value'], mode='lines', name='SPY')
)

# Add Magnificent 7 line
fig_combined.add_trace(
    go.Scatter(x=data.index, y=investment_values, mode='lines', name='Magnificent 7')
)

# Update layout
fig_combined.update_layout(
    title="Portfolio Comparison: SPY vs. Magnificent 7 ($100 Investment)",
    xaxis_title="Time",
    yaxis_title="Investment Value ($)",
    template="plotly_white",
    legend_title="Portfolios"
)

# Display the combined plot
st.plotly_chart(fig_combined)