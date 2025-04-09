import streamlit as st

def display_home():
    st.markdown("""
        <div style='text-align: center;'>
            <h1 style='color: #0077b6;'>🏦 THE POT BANK</h1>
            <h3>Secure • Reliable • Modern Banking</h3>
            <p>Welcome to THE POT BANK. Your money, your future, our responsibility.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📜 Guidelines & Regulatory Information")
    st.markdown("""
    - All transactions are encrypted and secured.
    - Login tokens expire every 30 minutes.
    - Only managers and employees can transfer on behalf of others.
    - Customers can access only their own account.
    - Funds are transferred instantly between verified accounts.
    - Your data is secured and complies with regulatory standards.
    """)

    st.info("Need help? Visit your nearest POT BANK branch or call our 24x7 helpline.")
