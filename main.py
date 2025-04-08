import streamlit as st
from auth import signup_user, login_user
from transactions import get_user_balance, make_transaction, get_transactions

from models.branch_model import create_branch, get_all_branches
from models.customer_model import create_customer, get_customer
from models.manager_model import create_manager, get_manager_by_branch

st.set_page_config(page_title="Bank Management System")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.is_admin = False

st.title("🏦 Bank Management System")

# Admin hardcoded (for now)
ADMIN_USERNAME = "admin"

menu = ["Login", "Sign Up"] if not st.session_state.logged_in else (
    ["Dashboard", "Profile", "Logout", "Admin Panel"] if st.session_state.username == ADMIN_USERNAME else ["Dashboard", "Profile", "Logout"]
)
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Sign Up":
    st.subheader("Create a New Account")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")

    branches = get_all_branches()
    branch_names = [b['branch_name'] for b in branches]
    branch_choice = st.selectbox("Select Branch", branch_names)

    if st.button("Sign Up"):
        success, msg = signup_user(username, password)
        if success:
            branch_id = next(b['_id'] for b in branches if b['branch_name'] == branch_choice)
            create_customer(username, full_name, email, branch_id)
            st.success("User registered and customer profile created.")
        else:
            st.error(msg)

elif choice == "Login":
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        success, user = login_user(username, password)
        if success:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.is_admin = (username == ADMIN_USERNAME)
            st.success("Logged in successfully!")
            st.rerun()
        else:
            st.error("Invalid credentials.")

elif choice == "Dashboard":
    st.subheader(f"Welcome, {st.session_state.username}")
    balance = get_user_balance(st.session_state.username)
    st.info(f"Your current balance is: ₹{balance}")

    col1, col2 = st.columns(2)
    with col1:
        deposit_amount = st.number_input("Amount to Deposit", min_value=1)
        if st.button("Deposit"):
            success, msg = make_transaction(st.session_state.username, deposit_amount, "deposit")
            st.success(msg) if success else st.error(msg)

    with col2:
        withdraw_amount = st.number_input("Amount to Withdraw", min_value=1)
        if st.button("Withdraw"):
            success, msg = make_transaction(st.session_state.username, withdraw_amount, "withdraw")
            st.success(msg) if success else st.error(msg)

    st.subheader("📋 Transaction History")
    transactions = get_transactions(st.session_state.username)
    for t in transactions:
        st.write(f"{t['date'].strftime('%Y-%m-%d %H:%M:%S')} - {t['type'].capitalize()} ₹{t['amount']}")

elif choice == "Profile":
    st.subheader("Customer Profile")
    customer = get_customer(st.session_state.username)
    if customer:
        branch = get_all_branches()
        branch_map = {str(b['_id']): b['branch_name'] for b in branch}
        st.write(f"👤 Full Name: {customer['full_name']}")
        st.write(f"📧 Email: {customer['email']}")
        st.write(f"🏢 Branch: {branch_map.get(str(customer['branch_id']), 'N/A')}")
    else:
        st.warning("Customer profile not found.")

elif choice == "Admin Panel":
    if st.session_state.username != ADMIN_USERNAME:
        st.error("Access denied.")
    else:
        st.subheader("🔧 Admin Panel")

        admin_tabs = st.tabs(["Create Branch", "Assign Manager", "View Branches"])
        
        with admin_tabs[0]:
            st.write("➕ Create a New Branch")
            branch_name = st.text_input("Branch Name")
            location = st.text_input("Location")
            if st.button("Add Branch"):
                success, msg = create_branch(branch_name, location)
                st.success(msg) if success else st.error(msg)

        with admin_tabs[1]:
            st.write("👔 Assign a Manager")
            manager_name = st.text_input("Manager Name")
            branches = get_all_branches()
            branch_ids = [b['_id'] for b in branches]
            branch_names = [b['branch_name'] for b in branches]
            selected_branch = st.selectbox("Select Branch", branch_names)
            if st.button("Assign Manager"):
                branch_id = branch_ids[branch_names.index(selected_branch)]
                success, msg = create_manager(manager_name, branch_id)
                st.success(msg) if success else st.error(msg)

        with admin_tabs[2]:
            st.write("🏢 All Branches")
            for b in get_all_branches():
                st.write(f"📍 {b['branch_name']} - {b['location']}")
                manager = get_manager_by_branch(b['_id'])
                if manager:
                    st.write(f"👔 Manager: {manager['manager_name']}")
                st.markdown("---")

elif choice == "Logout":
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.is_admin = False
    st.success("Logged out.")
    st.rerun()
