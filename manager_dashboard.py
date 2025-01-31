import streamlit as st

# Dummy data
total_blue_dollars = 500  # Available Blue Dollars for the manager
employees = [
    {"name": "Alice Johnson", "used": 120},
    {"name": "Bob Smith", "used": 80},
    {"name": "Charlie Brown", "used": 150},
    {"name": "David Lee", "used": 90},
    {"name": "Emma Watson", "used": 60},
]

def show():
    st.title("Manager Dashboard")

    # Wallet section
    st.markdown("### Wallet Balance")
    st.markdown(
        f"""
        <div style='padding: 20px; background-color: #1E88E5; color: white; 
                    text-align: center; border-radius: 10px; font-size: 24px;'>
            <strong>{total_blue_dollars} Blue Dollars Remaining</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 📋 Employee Blue Dollar Usage")

    # Employee list with a table
    st.table(
        [{"Employee Name": emp["name"], "Used Blue Dollars": emp["used"]} for emp in employees]
    )

    # Back button
    if st.button("🔙 Back to Login"):
        st.session_state.page = "login"
        st.rerun()

