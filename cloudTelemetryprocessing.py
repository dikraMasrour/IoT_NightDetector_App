import time
import paho.mqtt.client as mqtt
import json
import csv
import pandas as pd

LIGHT = 0

with open('light_data.csv', 'w', newline='') as csvfile:
    fieldnames = ['timestamp', 'light']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

# gotten from https://www.guidgen.com/
client_id = '278320da-7c3d-4236-905c-4518170a814f'

client_telemetry_topic = client_id + '/lightTelemetry'
client_command_topic = client_id + '/command'

mqtt_client = mqtt.Client(client_id + 'cloudTelemetryProcessing')
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()

STATE = ''
def handle_telemetry(client, userdata, telemetry):
    global STATE

    new_state = ''
    
    payload = json.loads(telemetry.payload.decode())
    LIGHT = payload.get('light')

    print('Telemetry received: ' , LIGHT)

    with open('light_data.csv', 'a', newline='') as csvfile:
        fieldnames = ['timestamp', 'light']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # save to csv
        writer.writerow(payload)

    on_command = json.dumps({'led' : 'on', 'brightness' : 123, 'blinkFreq' : 123})
    off_command = json.dumps({'led' : 'off'})

    th = 500
    if LIGHT < th:
        new_state = 'on'
        if STATE != new_state:
            STATE = 'on'
            print('Sending on command ', on_command)
            mqtt_client.publish(client_command_topic, on_command, qos=1)

    elif LIGHT > th:
        new_state = 'off'
        if STATE != new_state:
            STATE = 'off'
            print('Sending off command ', off_command)
            mqtt_client.publish(client_command_topic, off_command, qos=1)

mqtt_client.subscribe(client_telemetry_topic, qos=1)
mqtt_client.on_message = handle_telemetry


while True:

    time.sleep(5)     
    