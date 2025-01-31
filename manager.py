import streamlit as st
import pandas as pd
import plotly.express as px

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
    # Set the page title and layout
    st.set_page_config(page_title="Manager Dashboard", layout="wide")

    # Custom CSS for styling
    st.markdown("""
    <style>
        body {
            background-color: #f4f7fc;
            font-family: 'Arial', sans-serif;
        }
        .blue-box {
            padding: 20px;
            background-color: #1E88E5;
            color: white;
            text-align: center;
            border-radius: 10px;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .table-container {
            margin-top: 30px;
            padding: 20px;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .back-button {
            margin-top: 20px;
            padding: 10px 30px;
            background-color: #ff4081;
            color: white;
            border-radius: 10px;
            cursor: pointer;
            border: none;
        }
        .back-button:hover {
            background-color: #e0376e;
        }
        .progress-bar {
            margin-top: 20px;
            margin-bottom: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

    # Title for the dashboard
    st.title("Manager Dashboard")

    # Wallet section with a custom box style
    st.markdown(f"""
    <div class="blue-box">
        {total_blue_dollars} Blue Dollars Remaining
    </div>
    """, unsafe_allow_html=True)

    # Progress bar for remaining Blue Dollars
    used_dollars = sum(emp["used"] for emp in employees)
    remaining_dollars = total_blue_dollars - used_dollars
    progress = remaining_dollars / total_blue_dollars
    st.markdown(f"**Remaining Blue Dollars:** {remaining_dollars} / {total_blue_dollars}")
    st.progress(progress)

    # Employee Blue Dollar usage table
    st.markdown("### 📋 Employee Blue Dollar Usage")
    st.markdown("""
    <div class="table-container">
    """, unsafe_allow_html=True)

    # Convert employee data to a DataFrame for better visualization
    df = pd.DataFrame(employees)
    st.table(df)

    st.markdown("</div>", unsafe_allow_html=True)  # Close table container

    # Bar chart for employee usage
    st.markdown("### 📊 Employee Usage Chart")
    fig = px.bar(df, x="name", y="used", labels={"name": "Employee Name", "used": "Used Blue Dollars"}, 
                 title="Blue Dollars Used by Employees", color="used", color_continuous_scale="Blues")
    st.plotly_chart(fig, use_container_width=True)

    # Back button (styled)
    if st.button("🔙 Back to Login", key="back", help="Go back to the login page"):
        st.session_state.page = "login"
        st.rerun()

# Run the dashboard
if __name__ == "__main__":
    show()


