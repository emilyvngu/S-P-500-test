import streamlit as st

# Set up page
st.set_page_config(page_title="Portfolio Optimization App", page_icon="📊")

# Hide Streamlit menu/footer (optional)
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Page title
st.title("📊 Portfolio Optimization Dashboard")

# Intro description
st.markdown("""
Welcome to a two-part portfolio analytics tool focused on understanding and visualizing investment strategies.

Use the buttons below to explore:
""")

# Layout with navigation buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("📈 Portfolio Visualization"):
        st.switch_page("pages/01_Portfolio_Visualization.py")

with col2:
    if st.button("🧮 Backtesting (Julia)"):
        st.switch_page("pages/03_Backtesting.py")
