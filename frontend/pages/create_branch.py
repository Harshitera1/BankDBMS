import streamlit as st
from models.branch_model import create_branch

def create_branch_page():
    if st.session_state.get("role") != "manager":
        st.error("Unauthorized: Only managers can create branches.")
        return

    st.title("🏢 Create New Bank Branch")

    branch_name = st.text_input("Branch Name")
    location = st.text_input("Branch Location")

    if st.button("Create Branch"):
        success, message = create_branch(branch_name, location)
        if success:
            st.success(message)
        else:
            st.error(message)
