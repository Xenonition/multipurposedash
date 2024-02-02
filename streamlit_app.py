import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Persib Dashboard", layout="wide")
st.header("Dashboards")

col1, col2, col3 = st.columns([2, 2, 1])
with st.spinner('Connecting to Database...'):
    po_conn = st.connection("postgresql", type="sql")
    po_df = po_conn.query('select payment_status, count(payment_status) from "order" GROUP BY payment_status ORDER BY count(payment_status);', ttl=0)
    
po_fig = px.pie(po_df,
             values='count',
             names='payment_status'
            )
col1.subheader("PO Jersey Successful Transactions")
col1.plotly_chart(po_fig, theme="streamlit", use_container_width=True)

col2.subheader("Ticket Payment Methods")
days = col3.number_input('Look for payment in for the past X days', step=1)
payment_conn = st.connection("payments", type="sql")
payment_df = payment_conn.query('select payment_method, count(payment_method) from "payments" WHERE created_at > CURRENT_DATE - {} GROUP BY payment_method ORDER BY count(payment_method);'.format(days), ttl=0)

payment_fig = px.pie(payment_df,
             values='count',
             names='payment_method'
            )

col2.plotly_chart(payment_fig, theme="streamlit", use_container_width=True)
col3.dataframe(po_df)
col3.dataframe(payment_df)

OLD_DB_WAITLIST_COUNT = 5936
st.subheader("Email Registration")
col3, col4 = st.columns([3, 2])
with st.spinner('Connecting to Database...'):
    email_conn = st.connection("sql")
    email_df = email_conn.query("Select created_at from waitlists;", ttl=0)
email_df['date'] = pd.to_datetime(email_df['created_at'])
email_count = (
    email_df.groupby(email_df['date'].dt.date)[['date']]
    .count()
    .rename(columns={'date':'count'})
    .reset_index()
)
total = str(sum(email_count['count'])+OLD_DB_WAITLIST_COUNT)
delta = str(email_count.iloc[-1]['count'])

email_fig = px.line(email_count, x='date', y="count")
col3.plotly_chart(email_fig, theme="streamlit", use_container_width=True)
col4.metric("Registered Emails", total, delta)
col4.dataframe(email_count)