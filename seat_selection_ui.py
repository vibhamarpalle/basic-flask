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

def select_seat(seat_index):
    """Send a request to the Flask backend to select a seat."""
    response = requests.post(
        f"{BACKEND_URL}/select-seat",
        json={"seat_index": seat_index}
    )
    if response.status_code == 200:
        return response.json()["seats"]  # Return the updated seat list
    else:
        st.error(response.json()["error"])
        return None

def reset_seats():
    """Reset all seats to available."""
    response = requests.post(f"{BACKEND_URL}/reset-seats")
    if response.status_code == 200:
        st.success(response.json()["message"])
    else:
        st.error("Failed to reset seats")

def main():
    st.title("Cafeteria Seat Selection")
    st.write("Select a seat from the available options below.")

    # Fetch current seat status
    seats = fetch_seats()

    # Display seats in a grid layout
    cols = st.columns(10)  # 10 seats per row
    for i, seat in enumerate(seats):
        with cols[i % 10]:
            if seat:
                st.button(f"Seat {i} 🚫", key=f"seat_{i}", disabled=True)
            else:
                if st.button(f"Seat {i} ✅", key=f"seat_{i}"):
                    updated_seats = select_seat(i)
                    if updated_seats:
                        seats = updated_seats  # Update the local seat list

    # Add a button to reset all seats (for testing purposes)
    if st.button("Reset All Seats"):
        reset_seats()

if __name__ == "__main__":
    main()