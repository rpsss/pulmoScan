import streamlit as st
import sys
import os

# Setting the page configuration
st.set_page_config(page_title="PulmoScan App")

# Adding paths to import backend and pages
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from backend.sql_users_connection import verify_user, add_user
import frontend.Prediction_page as Prediction_page
import frontend.Home_page as Home_page

def main():
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    
    if not st.session_state['authenticated']:
        login_or_register()
    else:
        navigation()

def login_or_register():
    st.title("Login / Register")
    choice = st.radio("Select Action", ["Login", "Register"])

    if choice == "Login":
        login()
    else:
        register()

def login():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if verify_user(username, password):
            st.session_state['authenticated'] = True
            st.rerun()
        else:
            st.error("Invalid username or password")

def register():
    st.title("Register New User")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if new_password != confirm_password:
            st.error("Passwords do not match")
        else:
            add_user(new_username, new_password)
            st.success("User registered successfully. You can now log in.")

def navigation():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Select a page", ["Home", "Prediction_page"])

    if page == "Home":
        Home_page.show()
    elif page == "Prediction_page":
        Prediction_page.show()

if __name__ == "__main__":
    main()
