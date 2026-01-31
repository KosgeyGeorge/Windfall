import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. APP CONFIG ---
st.set_page_config(page_title="Windfall Architect: Compound Edition", page_icon="📈", layout="wide")

# Corrected Title Section (Fixes the TypeError)
st.markdown("""
    <style>
    .main-title {
        font-size:40px !important;
        font-weight: bold;
        color: #00ffcc;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    <p class="main-title">📈 Windfall Architect: Compounding Simulator</p>
    """, unsafe_allow_html=True)

st.markdown("This simulator calculates your financial runway with **Monthly Compounding Interest** and **Tax Withholding**.")

# --- 2. SIDEBAR INPUTS ---
st.sidebar.header("🚀 Initial Capital")
initial_windfall = st.sidebar.number_input("Starting Amount ($)", min_value=0.0, value=50000.0, step=1000.0)
mmf_rate = st.sidebar.slider("MMF Annual Yield (%)", 0.0, 20.0, 12.0) / 100

st.sidebar.header("📉 Monthly Outflow")
monthly_spend = st.sidebar.number_input("Total Monthly Expenses ($)", value=2000.0, step=100.0)

st.sidebar.header("💸 The Tax Man")
tax_rate = st.sidebar.slider("Tax on Interest (%)", 0, 40, 15) / 100

# --- 3. THE COMPOUNDING ENGINE ---
monthly_rate = mmf_rate / 12
balance = initial_windfall
data = []
total_tax = 0

for month in range(121): # Simulate 10 years (120 months)
    # Record current state
    data.append({"Month": month, "Balance": round(max(0, balance), 2)})
    
    if balance <= 0:
        break
        
    # A. COMPOUNDING CALCULATION
    # 1. Earn interest on current balance
    gross_interest = balance * monthly_rate
    # 2. Subtract tax from that interest
    tax_hit = gross_interest * tax_rate
    net_interest = gross_interest - tax_hit
    total_tax += tax_hit
    
    # 3. Add net interest back to balance (Compounding) and subtract spending
    balance = (balance + net_interest) - monthly_spend

df = pd.DataFrame(data)

# --- 4. VISUALS & METRICS ---
col1, col2, col3 = st.columns(3)
col1.metric("Runway", f"{len(df)-1} Months")
col2.metric("Total Tax Paid", f"${int(total_tax):,}")
col3.metric("Final Balance", f"${int(df['Balance'].iloc[-1]):,}")

# Plotly Graph
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df['Month'], 
    y=df['Balance'], 
    fill='tozeroy', 
    line=dict(color='#00ffcc', width=3), 
    name="Compounded Wealth"
))

fig.update_layout(
    template="plotly_dark", 
    title="The Compounding Snowball Effect", 
    xaxis_title="Months", 
    yaxis_title="Balance ($)",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# --- 5. THE CELEBRATION ---
if len(df) > 1:
    st.balloons()