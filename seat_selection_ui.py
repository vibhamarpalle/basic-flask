import streamlit as st
import requests

# Flask backend URL
BACKEND_URL = "http://127.0.0.1:5000"

def fetch_seats():
    """Fetch the current seat status from the Flask backend."""
    response = requests.get(f"{BACKEND_URL}/seats")
    if response.status_code == 200:
        return response.json()["seats"]
    else:
        st.error("Failed to fetch seat data")
        return [False] * 50

def select_seat(seat_index, user_id):
    """Send a request to the Flask backend to select a seat and bill the manager."""
    response = requests.post(
        f"{BACKEND_URL}/select-seat",
        json={"seat_index": seat_index, "user_id": user_id}
    )
    if response.status_code == 200:
        return response.json()  # Return the updated seat list and billing record
    else:
        st.error(response.json()["error"])
        return None

def fetch_billing_history():
    """Fetch the billing history from the Flask backend."""
    response = requests.get(f"{BACKEND_URL}/billing-history")
    if response.status_code == 200:
        return response.json()["billing_history"]
    else:
        st.error("Failed to fetch billing history")
        return []

def reset_seats():
    """Reset all seats and billing records."""
    response = requests.post(f"{BACKEND_URL}/reset-seats")
    if response.status_code == 200:
        st.success(response.json()["message"])
    else:
        st.error("Failed to reset seats")

def seating():
    st.title("Seat Selection")
    user_name = st.text_input("Enter your name:", "")
    st.write("Select a seat from the available options below.")

    # Fetch current seat status
    seats = fetch_seats()

    # Display seats in a grid layout
    cols = st.columns(10)  # 10 seats per row
    for i, seat in enumerate(seats):
        with cols[i % 10]:
            if seat:
                st.button(f"Seat {i} 🚫", key=f"seat_{i+1}", disabled=True)
            else:
                if st.button(f"Seat {i} ✅", key=f"seat_{i+1}"):
                    updated_seats = select_seat(i+1,user_name)
                    if updated_seats:
                        seats = updated_seats  # Update the local seat list
def see_billing():
    st.header("Billing History")
    st.write("View all billing records below.")

    # Fetch and display billing history
    billing_history = fetch_billing_history()
    if billing_history:
        for record in billing_history:
            st.write(
                f"**Transaction ID:** {record['transaction_id']}, "
                f"**Seat:** {record['seat_index']}, "
                f"**User:** {record['user_id']}, "
                f"**Amount:** ${record['amount']}, "
                f"**Time:** {record['timestamp']}"
            )
    else:
        st.write("No billing records found.")
