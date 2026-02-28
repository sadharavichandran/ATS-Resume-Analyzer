import streamlit as st
from database import add_user, login_user, create_table

create_table()

def login_page():
    st.subheader("🔐 Login")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_user(user, pwd):
            st.session_state["logged_in"] = True
            st.session_state["user"] = user
            st.success("Login Successful")
        else:
            st.error("Invalid credentials")

def register_page():
    st.subheader("📝 Register")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Register"):
        add_user(user, pwd)
        st.success("Account Created")