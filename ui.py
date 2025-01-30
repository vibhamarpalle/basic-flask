# views.py

import streamlit as st
# from models import is_valid_email

st.title("Welcome to Blu Reserve")
choice = st.selectbox("Login/Signup",['Login','Signup'])
if choice == 'Login':
    email = st.text_input("IBM mail address")
    # if is_valid_email(email):
    #     password = st.text_input("Password",type= 'password')
    password = st.text_input("Password",type= 'password')
    # else:
    #     st.write("Invalid Email used")
    st.button("Login")
elif choice == 'Signup':
    email = st.text_input("IBM mail address")
    # if is_valid_email(email): 
    #     password = st.text_input("Password",type= 'password')
    password = st.text_input("Password",type= 'password')
    st.button("Login")
else:
    st.write("Invalid")
