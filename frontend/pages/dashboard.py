import streamlit as st
from backend.utils.auth import get_current_user
from database.connection import db
from models.transaction_model import get_transactions_by_account
from datetime import datetime
import pandas as pd

def dashboard():
    st.title("📊 POT BANK Dashboard")

    if "token" not in st.session_state:
        st.warning("Please login first.")
        return

    user_data = get_current_user(st.session_state.token)
    if not user_data:
        st.warning("Session expired. Please login again.")
        return

    account = db.accounts.find_one({"user_id": user_data["user_id"]})
    if not account:
        st.error("❌ No account found for this user.")
        return

    account_number = account.get("account_number", "N/A")
    balance = account.get("balance", 0)

    # ✅ Welcome box with account info
    # Inside dashboard()

    st.markdown(f"""
      <div style='
    background-color: #e6f0fa; /* Softer blue background for a clean look */
    padding: 20px 30px; /* Slightly more padding for better spacing */
    border-radius: 12px; /* Softer, modern rounded corners */
    margin-bottom: 25px; /* Increased margin for separation */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
    border-left: 5px solid #0288d1; /* Accent border for visual pop */
'>
    <h3 style='
        color: #01579b; /* Darker blue for better contrast and readability */
        font-family: "Arial", sans-serif; /* Clean, modern font */
        margin-bottom: 10px; /* Spacing below the heading */
    '>
        👋 Welcome, {user_data['username'].capitalize()} ({user_data['role'].capitalize()})
    </h3>
    <p style='
        font-size: 16px; 
        color: #333; /* Darker text for better readability */
        font-family: "Arial", sans-serif;
        margin: 5px 0; /* Consistent spacing between paragraphs */
    '>
        <b>💳 Account Number:</b> <code style='background-color: #f5f5f5; padding: 2px 6px; border-radius: 4px;'>{account_number}</code>
    </p>
    <p style='
        font-size: 16px; 
        color: #333; 
        font-family: "Arial", sans-serif;
        margin: 5px 0;
    '>
        <b>💰 Balance:</b> <span style='color: #2e7d32; font-weight: bold;'>₹{balance:,.2f}</span> <!-- Green for balance to indicate money -->
    </p>
</div>
    """, unsafe_allow_html=True)


    # 🏢 Branch Info
    branch = db.branches.find_one({"ifsc_code": user_data.get("branch_id")})
    if branch:
        st.subheader("🏢 Branch Info")
        st.text(f"Branch Name: {branch.get('branch_name')}")
        st.text(f"IFSC Code: {branch.get('ifsc_code')}")
        st.text(f"Location: {branch.get('location', 'N/A')}")
    else:
        st.info("Branch information not available.")

    # 📋 Bank Schemes
    st.markdown("---")
    st.subheader("📄 Bank Schemes & Benefits")
    schemes = db.get_collection("schemes").find()
    has_schemes = False
    for scheme in schemes:
        has_schemes = True
        st.markdown(f"**📝 {scheme['name']}** — {scheme['description']}")
    if not has_schemes:
        st.info("No schemes available at the moment.")

    # 🧾 Transaction Summary
    st.markdown("---")
    st.subheader("📄 Recent Transactions")
    transactions = get_transactions_by_account(account_number)

    if not transactions:
        st.info("No transactions to show.")
    else:
        for tx in transactions[:5]:  # Show last 5
            direction = "🔺 Sent" if tx["sender_id"] == account_number else "🔻 Received"
            other_party = tx["receiver_id"] if direction == "🔺 Sent" else tx["sender_id"]
            st.markdown(f"""
                **{direction} ₹{tx['amount']}**  
                ↔️ With: `{other_party}`  
                🕒 {tx['timestamp'].strftime("%d %b %Y, %I:%M %p")}
                ---
            """)

    # 📈 Balance Trend
    st.markdown("### 📈 Balance Trend Overview")

    trend_data = []
    running_balance = balance

    for tx in sorted(transactions, key=lambda x: x["timestamp"], reverse=True):
        if tx["sender_id"] == account_number:
            running_balance += tx["amount"]
        else:
            running_balance -= tx["amount"]
        trend_data.append({
            "Timestamp": tx["timestamp"],
            "Balance": running_balance
        })

    trend_data.reverse()

    if trend_data:
        df = pd.DataFrame(trend_data)
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        df.set_index("Timestamp", inplace=True)
        st.line_chart(df)
    else:
        st.info("Not enough data for balance trend.")

    # 🛠 Manager Scheme Add Form
    if user_data["role"] == "manager":
        st.markdown("---")
        st.subheader("🛠 Add New Scheme")

        with st.form("add_scheme_form"):
            name = st.text_input("Scheme Name")
            description = st.text_area("Description")
            submitted = st.form_submit_button("➕ Add Scheme")

            if submitted and name and description:
                db.get_collection("schemes").insert_one({
                    "name": name,
                    "description": description
                })
                st.success("✅ Scheme added successfully.")
