import time
import paho.mqtt.client as mqtt
import json
from datetime import datetime
import random
import serial 

# define serial connection over bluetooth and its params
s = serial.Serial(
        port='/dev/rfcomm0', # using the defined rfcomm0 as the port
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)


# gotten from https://www.guidgen.com/
client_id = '278320da-7c3d-4236-905c-4518170a814f'

client_telemetry_topic = client_id + '/lightTelemetry'
client_command_topic = client_id + '/command'

mqtt_client = mqtt.Client(client_id + 'gateway')
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()


def handle_command(client, userdata, message):
    payload = json.loads(message.payload.decode())
    # commands
    print('Message received: ' , payload)
    if 'led' in payload.keys():
        if payload.led == 'on': s.write(b'lightOn\n')
        elif payload.led == 'off': s.write(b'lightOff\n')
        elif payload.led == 'blink': s.write(b'blink\n')
    if 'brightness' in payload.keys():
        s.write(b'bright:',payload.brightness, '\n')
    if 'blinkFrequency' in payload.keys():
        s.write(b'freq',payload.blinkFrequency, '\n')

mqtt_client.subscribe(client_command_topic, qos=1)
mqtt_client.on_message = handle_command

while True:
    # Getting the current date and time
    dt = datetime.now()
    # getting the timestamp
    ts = datetime.timestamp(dt)

    # read telemetry coming from arduino
    arduino_telemetry = s.readline
    # decode received bytes into string
    str_message = arduino_telemetry.decode('utf-8-sig')
    # remove newline symbols
    str_message = str_message.replace('\n', '')
    light_telemetry = str_message.replace('\r', '')

    telemetry = json.dumps({'timestamp' : ts, 'light' : light_telemetry})
    print('Sending light telemetry ', telemetry)
    mqtt_client.publish(client_telemetry_topic, telemetry, qos=1)

    time.sleep(5)


