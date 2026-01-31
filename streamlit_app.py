import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. APP CONFIG ---
st.set_page_config(page_title="Windfall Architect: Compound Edition", page_icon="📈", layout="wide")
st.title("📈 Windfall Architect: Compounding Simulator")
st.markdown("This version factors in **Monthly Compounding Interest** and **Tax Withholding**.")

# --- 2. SIDEBAR INPUTS ---
st.sidebar.header("🚀 Initial Capital")
initial_windfall = st.sidebar.number_input("Starting Amount ($)", min_value=0.0, value=50000.0)
mmf_rate = st.sidebar.slider("MMF Annual Yield (%)", 0.0, 20.0, 12.0) / 100

st.sidebar.header("📉 Monthly Outflow")
monthly_spend = st.sidebar.number_input("Total Monthly Expenses ($)", value=2000.0)

st.sidebar.header("💸 The Tax Man")
tax_rate = st.sidebar.slider("Tax on Interest (%)", 0, 40, 15) / 100

st.sidebar.header("🎁 Future Injections")
add_inflow = st.sidebar.checkbox("Add future bonus?")
extra_amount = st.sidebar.number_input("Amount ($)", value=10000.0) if add_inflow else 0
extra_month = st.sidebar.number_input("Month Received", min_value=1, value=12) if add_inflow else 0

# --- 3. THE COMPOUNDING ENGINE ---
monthly_rate = mmf_rate / 12
balance = initial_windfall
data = []
total_tax = 0

for month in range(121): # Simulate 10 years
    # A. Record Start of Month Balance
    data.append({"Month": month, "Balance": max(0, balance)})
    
    if balance <= 0:
        break
        
    # B. Apply Mid-Run Windfalls
    if add_inflow and month == extra_month:
        balance += extra_amount
        
    # C. COMPOUNDING CALCULATION
    # 1. Earn interest on the current balance
    gross_interest = balance * monthly_rate
    # 2. Subtract tax from that interest
    tax_hit = gross_interest * tax_rate
    net_interest = gross_interest - tax_hit
    total_tax += tax_hit
    
    # 3. Reinvest the net interest (Compounding!) and subtract spending
    balance = (balance + net_interest) - monthly_spend

df = pd.DataFrame(data)

# --- 4. VISUALS ---
m1, m2, m3 = st.columns(3)
m1.metric("Runway", f"{len(df)-1} Months")
m2.metric("Total Tax Paid", f"${int(total_tax):,}")
m3.metric("Final Balance", f"${int(df['Balance'].iloc[-1]):,}")

fig = go.Figure()
fig.add_trace(go.Scatter(x=df['Month'], y=df['Balance'], fill='tozeroy', line=dict(color='#00ffcc', width=3), name="Compounded Wealth"))
fig.update_layout(template="plotly_dark", title="The Compounding Snowball", xaxis_title="Months", yaxis_title="Balance ($)")
st.plotly_chart(fig, use_container_width=True)

if st.success("Balloons incoming!"):
    st.balloons()