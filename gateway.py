import time
import paho.mqtt.client as mqtt
import json
from datetime import datetime
import random

# gotten from https://www.guidgen.com/
client_id = '278320da-7c3d-4236-905c-4518170a814f'

client_telemetry_topic = client_id + '/lightTelemetry'
client_command_topic = client_id + '/command'

mqtt_client = mqtt.Client(client_id + 'gateway')
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()


def handle_command(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print('Message received: ' , payload)

mqtt_client.subscribe(client_command_topic, qos=1)
mqtt_client.on_message = handle_command

while True:
    # Getting the current date and time
    dt = datetime.now()
    # getting the timestamp
    ts = datetime.timestamp(dt)
    rand_light = random.randint(100, 900)
    telemetry = json.dumps({'timestamp' : ts, 'light' : rand_light})
    print('Sending light telemetry ', telemetry)
    mqtt_client.publish(client_telemetry_topic, telemetry, qos=1)

    time.sleep(5)