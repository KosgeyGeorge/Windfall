import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. GLOBAL SETTINGS & FOREX ---
st.set_page_config(page_title="Windfall Architect: Kenya Edition", page_icon="🇰🇪", layout="wide")

# Mock exchange rates (You can update these manually or I can show you how to pull live ones)
# Rates: 1 USD = 129 KES, 1 EUR = 140 KES, 1 GBP = 165 KES (Approximate)
EXCHANGE_RATES = {
    "KES (Shillings)": 1.0,
    "USD (Dollars)": 0.0078, 
    "EUR (Euros)": 0.0071,
    "GBP (Pounds)": 0.0061
}

st.title("🇰🇪 Windfall Architect: Global Compounder")

# --- 2. SIDEBAR: CURRENCY & INPUTS ---
st.sidebar.header("🌍 Currency Settings")
selected_currency = st.sidebar.selectbox("Display Currency", list(EXCHANGE_RATES.keys()))
rate = EXCHANGE_RATES[selected_currency]
symbol = selected_currency.split(" ")[0]

st.sidebar.header("🚀 Initial Capital")
# We input in KES because that's where your MMF likely sits
initial_kes = st.sidebar.number_input("Starting Amount (KSh)", min_value=0.0, value=1000000.0, step=50000.0)

st.sidebar.header("📈 MMF & Taxes")
mmf_rate = st.sidebar.slider("Annual Yield (%)", 0.0, 20.0, 15.0) / 100
tax_rate = st.sidebar.slider("Withholding Tax (%)", 0, 30, 15) / 100

st.sidebar.header("📉 Monthly Outflow")
monthly_spend_kes = st.sidebar.number_input("Monthly Expenses (KSh)", value=50000.0)

# --- 3. COMPOUNDING ENGINE ---
monthly_yield = mmf_rate / 12
balance = initial_kes
data = []
total_tax_kes = 0

for month in range(121):
    # Convert current KES balance to selected currency for the chart
    display_balance = balance * rate
    data.append({"Month": month, "Balance": max(0, display_balance)})
    
    if balance <= 0:
        break
        
    # Compounding Calculation (In KES)
    gross_interest = balance * monthly_yield
    tax_hit = gross_interest * tax_rate
    net_interest = gross_interest - tax_hit
    total_tax_kes += tax_hit
    
    balance = (balance + net_interest) - monthly_spend_kes

df = pd.DataFrame(data)

# --- 4. DASHBOARD ---
# Convert metrics to selected currency
final_bal = df['Balance'].iloc[-1]
tax_display = total_tax_kes * rate

col1, col2, col3 = st.columns(3)
col1.metric("Runway", f"{len(df)-1} Months")
col2.metric(f"Total Tax ({symbol})", f"{tax_display:,.2f}")
col3.metric(f"Final Value ({symbol})", f"{final_bal:,.2f}")

# --- 5. CHART ---
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df['Month'], 
    y=df['Balance'], 
    fill='tozeroy', 
    line=dict(color='#00ffcc', width=3),
    name=f"Wealth in {symbol}"
))

fig.update_layout(
    template="plotly_dark", 
    title=f"Compounding Wealth Projection ({selected_currency})",
    xaxis_title="Months",
    yaxis_title=f"Amount ({symbol})"
)
st.plotly_chart(fig, use_container_width=True)

st.info(f"💡 Note: Rates used: 1 USD = {1/EXCHANGE_RATES['USD (Dollars) Aidan']:,.1f} KES")