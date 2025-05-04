import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import date

# Initialize session state for data
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=[
        "Date", "Account", "Category", "Amount"])
if "capital" not in st.session_state:
    st.session_state.capital = {
        "Cash": 0, "Bank": 0, "Savings": 0
    }

st.title("Spending Tracker App")

st.sidebar.header("Input Capital and Spendings")

# Input capital amounts
st.sidebar.subheader("Set Initial Capital")
for acc in st.session_state.capital:
    st.session_state.capital[acc] = st.sidebar.number_input(
        f"{acc} Capital", value=st.session_state.capital[acc], step=100
    )

# Input spending data
st.sidebar.subheader("Log Spending")
spend_date = st.sidebar.date_input("Date", value=date.today())
account = st.sidebar.selectbox("Account", ["Cash", "Bank", "Savings"])
category = st.sidebar.selectbox("Category", [
    "Food", "Drinks", "Study cafe", "Swimming tickets", "Parking fees",
    "Transportation fees", "Gaming", "Shopping", "Dating", 
    "Self-entertainment", "Travelling", "Others"])
amount = st.sidebar.number_input("Amount Spent", min_value=0.0, step=10.0)

if st.sidebar.button("Add Spending"):
    new_row = {"Date": spend_date, "Account": account, "Category": category, "Amount": amount}
    st.session_state.data = pd.concat([
        st.session_state.data, pd.DataFrame([new_row])], ignore_index=True)
    st.success(f"Added {amount} to {account} for {category} on {spend_date}")

# Display current data
st.subheader("Spending Data")
st.dataframe(st.session_state.data)

# Create visualizations
if not st.session_state.data.empty:
    df = st.session_state.data.copy()
    df["Date"] = pd.to_datetime(df["Date"])

    # Plot 1: Histograms for each account
    st.subheader("Spending Distribution by Account")
    fig, axs = plt.subplots(1, 3, figsize=(18, 5))
    colors = sns.color_palette("bright", 3)
    for i, acc in enumerate(["Cash", "Bank", "Savings"]):
        sns.histplot(df[df["Account"] == acc]["Amount"], kde=True, ax=axs[i], color=colors[i])
        axs[i].set_title(f"{acc} Spending Distribution")
        axs[i].set_xlabel("Amount")
        axs[i].set_ylabel("Frequency")
    st.pyplot(fig)

    # Plot 2: Line graph of daily spending per account
    st.subheader("Daily Spending per Account")
    daily = df.groupby(["Date", "Account"])["Amount"].sum().reset_index()
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=daily, x="Date", y="Amount", hue="Account", palette="bright", marker="o", ax=ax2)
    ax2.set_title("Daily Spending by Account")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Total Spending")
    st.pyplot(fig2)
else:
    st.info("Add some spending data to see visualizations.")