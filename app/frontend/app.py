import streamlit as st
import sys
import os

st.set_page_config(page_title="PulmoScan App")

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from backend.sql_users_connection import verify_user, add_user, get_user_id
import frontend.Prediction_page as Prediction_page
import frontend.Home_page as Home_page
import frontend.Update_prediction as Update_prediction
import frontend.History_page as History_page

def main():
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    
    if not st.session_state['authenticated']:
        login_or_register()
    else:
        if 'page' not in st.session_state:
            st.session_state['page'] = 'Home'
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
            st.session_state['user_id'] = get_user_id(username)  # Ensure user_id is stored in session
            st.experimental_rerun()
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
    if 'image_data' in st.session_state and st.session_state['page'] == 'Update_prediction':
        Update_prediction.show()
    else:
        page = st.sidebar.radio("Go to", ["Home", "Prediction", "History"])
        if page == "Home":
            Home_page.show()
        elif page == "Prediction":
            Prediction_page.show()
        elif page == "History":
            History_page.show()

if __name__ == "__main__":
    main()
