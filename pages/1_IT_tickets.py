import streamlit as st
import pandas as pd
import altair as alt
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
    assigned = st.selectbox('Assigned To', data['assigned_to'].unique())


data['Time'] = pd.to_datetime(data['created_at'])
filtered_data = data[data['status'] == status]
filtered_data = filtered_data[filtered_data['assigned_to'] == assigned]

st.title("IT Tickets Dashboard 💻")

st.subheader("IT Tickets Overview")

col1, col2, col3 = st.columns(3)


with col1:
    st.subheader(f"Tickets with status: {status}")
    st.bar_chart(filtered_data["status"].value_counts())
    st.write("This chart shows the distribution of ticket statuses.")


with col2:
    st.subheader(f"Tickets assigned to: {assigned}")
    assigned_counts = filtered_data[filtered_data['assigned_to'] == assigned]['assigned_to'].value_counts()
    st.bar_chart(assigned_counts)
    st.write("This chart shows the number of tickets assigned to the selected IT support specialist.")


with col3: 
    st.subheader("Tickets Over Time") 
    tickets_over_time = filtered_data.groupby(filtered_data['Time'].dt.date).size().reset_index(name='counts') 
    line_chart = alt.Chart(tickets_over_time).mark_line(point=True).encode( 
        x='Time:T', y='counts:Q' 
        ).properties( 
            width=300, height=200 ) 
    
    st.altair_chart(line_chart, use_container_width=True) 
    st.write("This chart shows the number of tickets created over time.")

st.subheader("Filtered Tickets")
st.dataframe(filtered_data)



