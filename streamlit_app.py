import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. PAGE CONFIG & DYNAMIC LOGO ---
st.set_page_config(page_title="Windfall Architect", page_icon="💰", layout="wide")

# Custom CSS for the Pastel Blue/Green Dynamic Logo
st.markdown("""
    <style>
    .logo-text {
        font-weight: 800;
        font-size: 50px !important;
        background: -webkit-linear-gradient(#7ed9ad, #80ced7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Helvetica Neue', sans-serif;
    }
    </style>
    <p class="logo-text">Windfall</p>
    """, unsafe_allow_input=True)

# --- 2. FOREX DATA ---
# Approx rates for KES base
EXCHANGE_RATES = {
    "KES (Shillings)": 1.0,
    "USD (Dollars)": 0.0078, 
    "EUR (Euros)": 0.0071,
    "GBP (Pounds)": 0.0061
}

# --- 3. SIDEBAR CONTROLS ---
st.sidebar.header("🌍 Global Settings")
selected_currency = st.sidebar.selectbox("Display Currency", list(EXCHANGE_RATES.keys()))
rate = EXCHANGE_RATES[selected_currency]
symbol = selected_currency.split(" ")[0]

st.sidebar.divider()

st.sidebar.header("🚀 Initial Capital")
initial_kes = st.sidebar.number_input("Starting Amount (KSh)", min_value=0.0, value=1000000.0, step=10000.0)

st.sidebar.header("📈 Growth & Tax")
mmf_rate = st.sidebar.slider("Annual Yield (%)", 0.0, 20.0, 15.0) / 100
tax_rate = st.sidebar.slider("Tax on Interest (%)", 0, 30, 15) / 100

st.sidebar.header("📉 Monthly Outflow")
monthly_spend_kes = st.sidebar.number_input("Monthly Expenses (KSh)", value=50000.0)

st.sidebar.header("🎁 Additional Windfalls")
add_bonus = st.sidebar.checkbox("Expect a future bonus?")
bonus_amount_kes = st.sidebar.number_input("Bonus Amount (KSh)", value=200000.0) if add_bonus else 0
bonus_month = st.sidebar.number_input("Month Received (1-120)", min_value=1, value=12) if add_bonus else 0

# --- 4. THE ENGINE ---
monthly_yield = mmf_rate / 12
balance = initial_kes
data = []
total_tax_kes = 0
total_interest_kes = 0

for month in range(121): # 10 Year Horizon
    # Convert to selected currency for data storage
    data.append({"Month": month, "Balance": max(0, balance * rate)})
    
    if balance <= 0:
        break
    
    # Apply Bonus
    if add_bonus and month == bonus_month:
        balance += bonus_amount_kes
        
    # Compounding Logic
    gross_interest = balance * monthly_yield
    tax_hit = gross_interest * tax_rate
    net_interest = gross_interest - tax_hit
    
    total_tax_kes += tax_hit
    total_interest_kes += gross_interest
    
    balance = (balance + net_interest) - monthly_spend_kes

df = pd.DataFrame(data)

# --- 5. DASHBOARD ---
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Financial Runway", f"{len(df)-1} Months")
with c2:
    st.metric(f"Interest Earned ({symbol})", f"{total_interest_kes * rate:,.2f}")
with c3:
    st.metric(f"Final Balance ({symbol})", f"{df['Balance'].iloc[-1]:,.2f}")

# Plotly Chart
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df['Month'], 
    y=df['Balance'], 
    fill='tozeroy', 
    line=dict(color='#7ed9ad', width=4),
    name="Wealth Path"
))

fig.update_layout(
    template="plotly_dark",
    title=f"Wealth Growth Projection in {selected_currency}",
    xaxis_title="Months from Now",
    yaxis_title=f"Balance ({symbol})",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig, use_container_width=True)

# Celebration
if balance > initial_kes:
    st.success("Your money is growing faster than you spend it! 🥂")
    st.balloons()