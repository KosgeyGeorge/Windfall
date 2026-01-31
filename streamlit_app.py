import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. APP CONFIG ---
st.set_page_config(page_title="Windfall Master Architect", page_icon="💰", layout="wide")

st.markdown("""
    <style>
    .main-title { font-size:40px !important; font-weight: bold; color: #00ffcc; text-align: center; }
    </style>
    <p class="main-title">💰 Windfall Master: Compounding & Forex Edition</p>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR: THE INPUTS ---
st.sidebar.header("🚀 Initial Capital")
currency = st.sidebar.selectbox("Base Currency", ["USD", "KES", "GBP", "EUR", "UGX"])
initial_windfall = st.sidebar.number_input(f"Starting Amount ({currency})", min_value=0.0, value=50000.0, step=1000.0)

st.sidebar.header("📈 Growth & Taxes")
mmf_rate = st.sidebar.slider("Annual Yield (%)", 0.0, 20.0, 12.0) / 100
tax_rate = st.sidebar.slider("Tax on Interest (%)", 0, 40, 15) / 100

st.sidebar.header("📉 Monthly Expenses")
monthly_spend = st.sidebar.number_input(f"Monthly Spend ({currency})", value=2000.0, step=100.0)

st.sidebar.header("🌍 Forex Converter")
target_currency = st.sidebar.selectbox("Convert Final Balance To:", ["KES", "USD", "GBP", "EUR", "TZS"])
# Mock exchange rates (You can update these or use an API later)
exchange_rates = {"USD": 1.0, "KES": 130.0, "GBP": 0.79, "EUR": 0.92, "UGX": 3800.0, "TZS": 2500.0}

# --- 3. THE CALCULATION ENGINE ---
monthly_rate = mmf_rate / 12
balance = initial_windfall
data = []
total_tax = 0

for month in range(121):
    data.append({"Month": month, "Balance": round(max(0, balance), 2)})
    if balance <= 0:
        break
    
    # Compounding Logic
    gross_interest = balance * monthly_rate
    tax_hit = gross_interest * tax_rate
    net_interest = gross_interest - tax_hit
    total_tax += tax_hit
    
    balance = (balance + net_interest) - monthly_spend

df = pd.DataFrame(data)

# --- 4. DISPLAY METRICS ---
final_bal_base = df['Balance'].iloc[-1]
# Convert to target currency
rate = exchange_rates.get(target_currency, 1.0) / exchange_rates.get(currency, 1.0)
converted_bal = final_bal_base * rate

m1, m2, m3 = st.columns(3)
m1.metric("Runway", f"{len(df)-1} Months")
m2.metric(f"Final Balance ({currency})", f"{final_bal_base:,.2f}")
m3.metric(f"Value in {target_currency}", f"{converted_bal:,.2f}")

# --- 5. VISUALS ---
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['Month'], y=df['Balance'], fill='tozeroy', 
                         line=dict(color='#00ffcc', width=3), name="Wealth Path"))
fig.update_layout(template="plotly_dark", title="Wealth Projection (Compounded)", 
                  xaxis_title="Months", yaxis_title=f"Balance ({currency})")
st.plotly_chart(fig, use_container_width=True)

# --- 6. CELEBRATION ---
if final_bal_base > initial_windfall:
    st.success("Your money is growing faster than you spend it! 🚀")
    st.balloons()