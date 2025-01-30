import streamlit as st
import requests
import seat_selection_ui

st.title("Welcome to Blu Reserve")

# API URL
API_URL = "http://localhost:3000"  # Flask backend URL

def login():
    # Check if user is already logged in
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        st.success(f"Welcome back {st.session_state.role}! Wallet Money: {st.session_state.wallet_money}")
        if st.session_state.manager:
            st.write(f"Manager: {st.session_state.manager}")
        seat_selection_ui.seating()  # Show seat selection UI
        return  # Exit the function if already logged in

    # Login form
    email = st.text_input("IBM mail address")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        # Send login request to backend
        response = requests.post(f"{API_URL}/login", json={"email": email, "password": password})

        if response.status_code == 200:
            data = response.json()
            if data['role']=="employee":
                # Store user data in session state
                st.session_state.logged_in = True
                st.session_state.role = data['role']
                st.session_state.wallet_money = data['wallet_money']
                st.session_state.manager = data.get('manager', False)
                st.success(f"Welcome ! Wallet Money: {data['wallet_money']}")
                seat_selection_ui.seating()  # Show seat selection UI
            else:
                st.session_state.logged_in = True
                st.session_state.role = data['role']
                st.session_state.wallet_money = data['wallet_money']
                st.session_state.manager = data.get('manager', True)
                st.success(f"Welcome ! Wallet Money: {data['wallet_money']}")
                seat_selection_ui.see_billing() 

        else:
            st.error(response.json()['message'])


# Function to handle signup

def signup_manager():
    name = st.text_input("Full Name")
    email = st.text_input("IBM mail address")
    password = st.text_input("Password", type='password')

    if st.button("Sign Up"):
        # Send signup request to backend
        response = requests.post(f"{API_URL}/signup_manager", json={"role": "manager","name": name, "email": email, "password": password})

        if response.status_code == 201:
            st.success("Signup successful! Please login.")
        else:
            st.error(response.json()['message'])

def signup_employee():
    name = st.text_input("Full Name")
    manager_email= st.text_input("mail address of manager")
    email = st.text_input("IBM mail address")
    password = st.text_input("Password", type='password')

    if st.button("Sign Up"):
        # Send signup request to backend
        response = requests.post(f"{API_URL}/signup_employee", json={"role": "employee","name": name,"reports_to":manager_email, "email": email, "password": password})

        if response.status_code == 201:
            st.success("Signup successful! Please login.")
        else:
            st.error(response.json()['message'])

# Select between Login and Signup
choice = st.selectbox("Login/Signup", ['Login', 'Signup as employee','Signup as manager'])

if choice == 'Login':
    login()
elif choice == 'Signup as employee':
    signup_employee()
elif choice == 'Signup as manager':
    signup_manager() 