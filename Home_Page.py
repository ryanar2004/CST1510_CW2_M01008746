from os import name
import streamlit as st
from hashing import generate_hash, is_valid_hash
from app_model.db import get_connection
from app_model.users import add_user, get_user
from app_model.it_tickets import get_all_it_tickets
from streamlit_lottie import st_lottie
import json
import time


st.set_page_config(
    page_title="Welcome",
    layout="centered",
    initial_sidebar_state="auto"
)


if 'splash_done' not in st.session_state:
    st.session_state.splash_done = False

if not st.session_state.splash_done:
   
    st.markdown("""
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            [data-testid="stSidebar"] {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

    splash_placeholder = st.empty()
    with splash_placeholder.container():
        with open("welcome_logo.json") as f:
            lottie_animation = json.load(f)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st_lottie(lottie_animation, speed=1, loop=True, height=400)

    time.sleep(3.2)

 
    splash_placeholder.empty()
    st.session_state.splash_done = True

st.markdown("""
    <style>
        #MainMenu {visibility: visible;}
        footer {visibility: visible;}
        header {visibility: visible;}
        [data-testid="stSidebar"] {visibility: visible;}
    </style>
""", unsafe_allow_html=True)

conn = get_connection()
data = get_all_it_tickets(conn)

st.set_page_config(page_title="Home", page_icon="🏠", layout="centered")

st.title("Home Page")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

tab_login, tab_logout, tab_register = st.tabs(["Login", "Logout", "Register"])

with tab_login:
    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")
    login_role = st.selectbox("Role", ["User", "Admin"], key="login_role")

    if st.button("Log In"):
        id, user_name, user_hash, role = get_user(conn, login_username)

        if login_username == user_name and is_valid_hash(login_password, user_hash) and login_role == role:
            st.session_state['logged_in'] = True
            st.success(f"Logged in successfuly as {login_role}")
            st.switch_page("pages/1_IT_tickets.py")
        st.session_state['logged_in'] = False
        st.error("Invalid username, password, or role. Please try again.")
       

with tab_logout:
    if st.button("Log Out"):
        st.session_state['logged_in'] = False
        st.info("You have been logged out")

with tab_register:
    regiserter_username = st.text_input("New Username")
    registered_password = st.text_input("New Password", type="password")
    registered_role = st.selectbox("Choose a role", ["User", "Admin"])
    hash_password = generate_hash(registered_password)

    if st.button("Register"):
        st.session_state['logged_in'] = False
        add_user(conn, regiserter_username, hash_password, registered_role)
        if registered_role == "Admin":
            st.success("Registered successfully as an admin, please log in")
        else:
            st.success("Registered successfully as a user, please log in")
