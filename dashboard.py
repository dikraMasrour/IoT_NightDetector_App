import time
from datetime import datetime

import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development

st.set_page_config(
    page_title="Real-Time IoT Dashboard",
    page_icon="💡",
    layout="wide",
)

# dashboard title
st.title("💡 Real-Time Night Detector Dashboard")

# @st.experimental_memo
def get_data() -> pd.DataFrame:
    return pd.read_csv('light_data.csv', delimiter=',')

df = get_data()

r, l = st.columns([3, 1])
n, m, p = st.columns([1, 2, 1])

with l:
    df
with r:
    fig = px.line(df, x="timestamp", y="light", title='Light values over time')
    st.plotly_chart(fig, use_container_width=True)

with m:
    st.radio(
        "LED Mode",
        key="led_mode",
        options=["off", "on", "blink"],
    )
    st.slider('LED brightness', 0, 500, 10)
    st.select_slider('LED blinking frequency', options=[1, 2, 3, 4, 5])


# st.button('Refresh')
time.sleep(5)
st.experimental_rerun()