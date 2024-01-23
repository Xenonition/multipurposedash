import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

st.header("dashboard")
conn = st.connection("postgresql", type="sql")
df = conn.query('select payment_status, count(payment_status) from "order" GROUP BY payment_status ORDER BY count(payment_status);', ttl="10m")
fig = px.pie(df,
             values='count',
             names='payment_status'
            )
st.plotly_chart(fig, theme="streamlit", use_container_width=True)

st.dataframe(df)