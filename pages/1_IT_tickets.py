import streamlit as st
import pandas as pd
from app_model.it_tickets import get_all_it_tickets
from app_model.db import get_connection



if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.warning("Please log in to access the Dashboard")
    if st.button("Go to Login Page"):
        st.session_state["logged_in"] = False
        st.switch_page("Home_Page.py")
    st.stop()


conn = get_connection()
data = get_all_it_tickets(conn)


with st.sidebar:
    status = st.selectbox('Status of Tickets', data['status'].unique())


data['timestamp'] = pd.to_datetime(data['created_at'])
filtered_data = data[data['status'] == status]


st.title("IT Tickets Dashboard 💻")

st.subheader("IT Tickets Overview")

col1, col2 = st.columns(2)


with col1:
    st.subheader(f"Tickets with status: {status}")
    st.bar_chart(filtered_data["status"].value_counts())
    st.write("This chart shows the distribution of ticket statuses.")


with col2:
    st.subheader("Priority Trend Over Time")
    st.line_chart(filtered_data, x='timestamp', y='priority')
    st.write("This chart shows how ticket priorities have changed over time.")


st.subheader("Filtered Tickets")
st.dataframe(filtered_data)
