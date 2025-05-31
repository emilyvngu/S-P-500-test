import streamlit as st

# Set page configuration
st.set_page_config(page_title="About", page_icon="ℹ️")

# Hide Streamlit footer and menu
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Title
st.title("About This Project")

# Intro
st.markdown("""
This interactive portfolio optimization tool was developed to demonstrate how data science, finance, and optimization modeling can come together to support smarter investment decisions.

It features two core components:
""")

# Features
st.markdown("""
### 📈 Portfolio Visualization
A side-by-side comparison of SPY and an equal-weighted **Magnificent 7** portfolio, showing the growth of a $100 investment over time using real historical data.

### 🧮 Backtesting (Julia)
A rolling-window **constrained minimum-variance optimizer** implemented in Julia using `JuMP` and `COSMO`. It solves for optimal portfolio weights under return and allocation constraints and simulates how the portfolio would have performed.

---

### Key Skills Demonstrated
- Data engineering with Python (pandas, yfinance)
- Portfolio theory and risk-return metrics
- Convex optimization modeling with Julia
- Rolling window backtesting and simulation
- Streamlit dashboard development
""")

# Footer
st.markdown("---")
st.caption("Built by Emily Nguyen | Powered by Python, Julia, and Streamlit")