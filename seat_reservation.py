import streamlit as st

def show():
    st.title("Seat Reservation")
    st.write("Welcome to the Employee Seat Reservation Page!")

    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()
