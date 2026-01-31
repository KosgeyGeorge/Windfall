import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. APP CONFIGURATION ---
st.set_page_config(
    page_title="Windfall Architect Pro",
    page_icon="💰",
    layout="wide"
)

# Custom CSS to make it look sleek on mobile
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    stMetric {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("💰 Windfall & Runway Architect")
st.markdown("---")

# --- 2. SIDEBAR INPUTS ---
st.sidebar.header("🚀 Primary Windfall")
initial_windfall = st.sidebar.number_input("Starting Capital ($)", min_value=0.0, value=50000.0, step=1000.0)
mmf_rate = st.sidebar.slider("MMF Annual Yield (%)", 0.0, 20.0, 10.0) / 100

st.sidebar.header("📉 Monthly Outflow")
monthly_spend = st.sidebar.number_input("Total Monthly Expenses ($)", min_value=0.0, value=2500.0, step=100.0)

st.sidebar.header("💸 The Tax Man")
tax_rate = st.sidebar.slider("Tax on Interest (%)", 0, 40, 15) / 100

st.sidebar.header("🎁 Future Injections")
add_inflow = st.sidebar.checkbox("Add a future windfall?")
if add_inflow:
    extra_amount = st.sidebar.number_input("Inflow Amount ($)", value=10000.0)
    extra_month = st.sidebar.number_input("Month Received (from now)", min_value=1, value=6)
else:
    extra_amount = 0
    extra_month = 0

st.sidebar.header("🎯 Financial Goal")
show_goal = st.sidebar.checkbox("Set a Savings Goal?")
target_goal = st.sidebar.number_input("Target Goal ($)", value=100000.0) if show_goal else None

# --- 3. CALCULATION ENGINE ---
monthly_interest_rate = mmf_rate / 12
balance = initial_windfall
total_tax_paid = 0
total_interest_earned = 0
data = []

# Simulate for 120 months (10 years) max
for month in range(121):
    # Record current state
    data.append({
        "Month": month,
        "Balance": max(0, balance),
        "Event": "Injection" if add_inflow and month == extra_month else "Standard"
    })
    
    if balance <= 0:
        break
        
    # Apply Future Inflow
    if add_inflow and month == extra_month:
        balance += extra_amount
        
    # Calculate Interest & Tax
    gross_interest = balance * monthly_interest_rate
    tax_deduction = gross_interest * tax_rate
    net_interest = gross_interest - tax_deduction
    
    total_interest_earned += gross_interest
    total_tax_paid += tax_deduction
    
    # Update Balance
    balance = (balance + net_interest) - monthly_spend

df = pd.DataFrame(data)
runway_months = len(df) - 1

# --- 4. DASHBOARD METRICS ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("Runway", f"{runway_months} Months")
m2.metric("Total Tax Paid", f"${int(total_tax_paid):,}")
m3.metric("Total Interest", f"${int(total_interest_earned):,}")
m4.metric("Ending Balance", f"${int(df['Balance'].iloc[-1]):,}")

# --- 5. VISUALIZATION ---
fig = go.Figure()

# Balance Line
fig.add_trace(go.Scatter(
    x=df['Month'], 
    y=df['Balance'], 
    mode='lines', 
    name='Net Balance',
    fill='tozeroy',
    line=dict(color='#00d4ff', width=3)
))

# Goal Line
if show_goal:
    fig.add_hline(y=target_goal, line_dash="dash", line_color="#ff4b4b", annotation_text="Target Goal")

# Future Windfall Marker
if add_inflow and extra_month <= runway_months:
    injection_y = df.loc[df['Month'] == extra_month, 'Balance'].values[0]
    fig.add_trace(go.Scatter(
        x=[extra_month], y=[injection_y],
        mode='markers+text',
        name='Windfall Injection',
        text=["💰 BONUS"],
        textposition="top center",
        marker=dict(color='gold', size=12, symbol='star')
    ))

fig.update_layout(
    title="Projected Wealth Runway",
    xaxis_title="Months from Now",
    yaxis_title="Balance ($)",
    template="plotly_dark",
    hovermode="x unified",
    margin=dict(l=20, r=20, t=50, b=20)
)

st.plotly_chart(fig, use_container_width=True)

# --- 6. INSIGHTS & ALERTS ---
st.subheader("📋 Simulation Insights")
c1, c2 = st.columns(2)

with c1:
    if runway_months >= 120:
        st.success("✨ **Financial Infinity:** Your MMF interest is covering your expenses. Your money will theoretically last forever!")
    elif runway_months > 24:
        st.info(f"✅ Your runway is healthy at {runway_months // 12} years and {runway_months % 12} months.")
    else:
        st.warning(f"⚠️ Warning: Your runway is only {runway_months} months. Consider reducing expenses.")

with c2:
    if show_goal:
        max_val = df['Balance'].max()
        if max_val >= target_goal:
            st.success(f"🎯 You hit your goal of ${target_goal:,} in Month {df[df['Balance'] >= target_goal]['Month'].iloc[0]}!")
        else:
            st.error(f"❌ With current settings, you peak at ${int(max_val):,}. You need ${int(target_goal - max_val):,} more to hit your goal.")

# Option to view raw data
if st.checkbox("Show Raw Monthly Data"):
    st.dataframe(df)
