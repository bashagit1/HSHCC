import streamlit as st
from utils.auth import authenticate_user

def login_page():
    st.title("Login")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.role = None

    if st.session_state.logged_in:
        st.success(f"Welcome, {st.session_state.username}!")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.role = None
            st.rerun()
    else:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")

            if submit:
                user = authenticate_user(username, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.role = user[3]
                    st.session_state.username = user[1]
                    st.success(f"Welcome, {user[1]}! Redirecting...")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
