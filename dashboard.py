import time
import json
from datetime import datetime

import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development
import paho.mqtt.client as mqtt

def handle_led_mode():
    st.session_state.led_mode = st.session_state.led_mode_value
def handle_freq():
    st.session_state.freq = st.session_state.freq_value
def handle_brightness():
    st.session_state.brightness = st.session_state.bright_value

def initialize_session():
    if 'led_mode' not in st.session_state:
        st.session_state.led_mode = 'off'
    if 'brightness' not in st.session_state:
        st.session_state.brightness = 10
    if 'freq' not in st.session_state:
        st.session_state.freq = '1'
    if 'led_mode_value' not in st.session_state:
        st.session_state.led_mode_value = 'off'
    if 'freq_value' not in st.session_state:
        st.session_state.freq_value = 1
    if 'bright_value' not in st.session_state:
        st.session_state.bright_value = 0

initialize_session()

def parse_values(led_mode, brightness, frequency):
    return json.dumps({'led' : led_mode, 'brightness' : brightness, 'blinkFrequency' : frequency})

def send_commands(led_mode, brightness, frequency):
    # gotten from https://www.guidgen.com/
    client_id = '278320da-7c3d-4236-905c-4518170a814f'

    client_command_topic = client_id + '/command'

    mqtt_client = mqtt.Client(client_id + 'dashboard')
    mqtt_client.connect('test.mosquitto.org')

    mqtt_client.loop_start()

    commands = parse_values(led_mode, brightness, frequency)

    mqtt_client.publish(client_command_topic, commands, qos=1)


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
    st.session_state.led_mode = st.radio(
        "LED Mode",
        options=["off", "on", "blink"], on_change= handle_led_mode, key='led_mode_value'
    )
    st.slider('LED brightness', 0, 500, 10, key='bright_value', on_change=handle_brightness)
    st.select_slider('LED blinking frequency', options=[1, 2, 3, 4, 5], key='freq_value', on_change=handle_freq)
    send = st.button('Send commands')

    if send:
        send_commands(st.session_state.led_mode, st.session_state.brightness, st.session_state.freq)
# st.button('Refresh')
time.sleep(5)
st.experimental_rerun()