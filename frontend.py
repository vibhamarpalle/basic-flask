import streamlit as st
import requests

st.title("My App")

def get_details_from_backend():
    details = requests.get("http://localhost:3000/get-details").text
    return details

st.text(get_details_from_backend())
