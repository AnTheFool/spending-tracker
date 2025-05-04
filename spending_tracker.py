import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="Spending Tracker", layout="wide")
st.title("💸 Personal Spending Tracker")

# Initialize session state
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Date", "Account", "Category", "Amount"])

if "capital" not in st.session_state:
    st.session_state.capital = {"Cash": 0, "Bank": 0, "Savings": 0}

def format_currency(value):
    return f"{value:,.0f} ₫".replace(",", ".")

def display_balance_cards(initial_capital, spending_data):
    accounts = ["Cash", "Bank", "Savings"]
    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]

    for i, acc in enumerate(accounts):
        initial = initial_capital[acc]
        spent = spending_data[spending_data["Account"] == acc]["Amount"].sum()
        current = initial - spent
        delta = current - initial
        delta_color = "green" if delta >= 0 else "red"
        delta_icon = "🔼" if delta >= 0 else "🔽"

        with cols[i]:
            st.markdown(f"""
                <div style='border:2px solid #00AEEF;padding:15px;border-radius:10px;'>
                    <h4>{acc} 💰</h4>
                    <h2 style='margin-top:-10px'>{format_currency(current)}</h2>
                    <p>Initial: {format_currency(initial)}</p>
                    <p style='color:{delta_color};font-weight:bold;'>{delta_icon} {format_currency(abs(delta))} change</p>
                </div>
            """, unsafe_allow_html=True)

# Display balance cards
st.subheader("💼 Account Summary")
display_balance_cards(st.session_state.capital, st.session_state.data)

# Set initial capital
with st.expander("💰 Set Initial Capital (VND)", expanded=False):
    with st.form("capital_form"):
        cash = st.number_input("Cash", min_value=0, value=st.session_state.capital["Cash"])
        bank = st.number_input("Bank Accounts", min_value=0, value=st.session_state.capital["Bank"])
        savings = st.number_input("Savings", min_value=0, value=st.session_state.capital["Savings"])
        submitted = st.form_submit_button("Update Capital")
        if submitted:
            st.session_state.capital = {"Cash": cash, "Bank": bank, "Savings": savings}
            st.success("Capital updated successfully!")

# Input spending
st.subheader("🧾 Add New Spending")
with st.form("spending_form"):
    date = st.date_input("Date", datetime.today())
    account = st.selectbox("Account", ["Cash", "Bank", "Savings"])
    category = st.selectbox("Category", [
        "Food", "Drinks", "Study cafe", "Swimming tickets", "Parking fees",
        "Transportation fees", "Gaming", "Shopping", "Dating",
        "Self-entertainment", "Travelling", "Others"
    ])
    amount = st.number_input("Amount Spent (VND)", min_value=0)
    add = st.form_submit_button("Add Spending")
    if add:
        new_entry = pd.DataFrame({"Date": [date], "Account": [account], "Category": [category], "Amount": [amount]})
        st.session_state.data = pd.concat([st.session_state.data, new_entry], ignore_index=True)
        st.success("Spending added!")

# Show full data
st.subheader("📋 Spending Records")
st.dataframe(st.session_state.data)

# Visualization
if not st.session_state.data.empty:
    st.subheader("📊 Visualizations")
    vis_col1, vis_col2 = st.columns([2, 3])

    with vis_col1:
        st.markdown("### 🔍 Distribution by Account")
        fig, axes = plt.subplots(1, 3, figsize=(15, 4))
        for i, acc in enumerate(["Cash", "Bank", "Savings"]):
            sns.histplot(
                st.session_state.data[st.session_state.data["Account"] == acc]["Amount"],
                bins=10,
                kde=False,
                ax=axes[i],
                color=sns.color_palette("bright")[i]
            )
            axes[i].set_title(f"{acc} Spending")
        st.pyplot(fig)

    with vis_col2:
        st.markdown("### 📈 Daily Spendings by Account")
        daily = st.session_state.data.groupby(["Date", "Account"])["Amount"].sum().reset_index()
        pivot = daily.pivot(index="Date", columns="Account", values="Amount").fillna(0)
        st.line_chart(pivot)
else:
    st.info("Add spendings to see the charts.")
