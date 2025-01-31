# views.py

import streamlit as st
# from models import is_valid_email
def is_ibm_email(email):
    return email.endswith("@ibm.com")
# Set page state
if "page" not in st.session_state:
    st.session_state.page = "login"

def navigate_to(page):
    st.session_state.page = page
    st.rerun()

# Login UI
if st.session_state.page=="login":
    st.title("Welcome to Blu-Reserve")
    choice = st.selectbox("Login as",['Employee','Manager'])
    email = st.text_input("IBM mail address")

    if email and not is_ibm_email(email):
        st.error("You need to enter a valid email address")
        # if is_valid_email(email):
        #     password = st.text_input("Password",type= 'password')
    else:
        password = st.text_input("Password",type= 'password')
            # else:
            #     st.write("Invalid Email used")
        if choice == 'Employee':
            
            if st.button("Login as employee"):
                navigate_to("employee")
        elif choice == 'Manager':
            
            if st.button("Login as manager"):
                navigate_to("manager")
        else:
            st.write("Invalid")

# Route to Manager Dashboard
elif st.session_state.page == "manager":
    import manager_dashboard  # Importing manager dashboard
    manager_dashboard.show()

# Route to Seat Reservation Page
elif st.session_state.page == "employee":
    import seat_reservation  # Importing employee seat reservation page
    seat_reservation.show()
