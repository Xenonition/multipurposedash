import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

st.header("Dashboards")
st.subheader("PO Jersey Successful Transactions")
po_conn = st.connection("postgresql", type="sql")
po_df = po_conn.query('select payment_status, count(payment_status) from "order" GROUP BY payment_status ORDER BY count(payment_status);', ttl="10m")
po_fig = px.pie(po_df,
             values='count',
             names='payment_status'
            )
st.plotly_chart(po_fig, theme="streamlit", use_container_width=True)

st.dataframe(po_df)

st.subheader("Email Registration")

email_conn = st.connection("sql")
email_df = email_conn.query("Select created_at from notify_me;")
email_df['date'] = pd.to_datetime(email_df['created_at'])
email_count = (
    email_df.groupby(email_df['date'].dt.date)[['date']]
    .count()
    .rename(columns={'date':'count'})
    .reset_index()
)

email_fig = px.line(email_count, x='date', y="count")
st.plotly_chart(email_fig, theme="streamlit", use_container_width=True)
st.dataframe(email_count)