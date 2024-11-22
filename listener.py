#!/usr/bin/env python

import paho.mqtt.client as mqtt
import signal, json, subprocess, os

# client, user and device details
serverUrl   = "127.0.0.1"
port        = 1883
clientId    = "dynamic_mapper_edge"

# Clean Exit Handler
def signal_handler(signum, frame):
    client.loop_stop()
    client.disconnect()
	
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# MQTT Handlers
def on_connect(client, userdata, flags, reason_code, properties=None):
    client.subscribe(inbound_topic)

def on_message(client, userdata, msg): 
    message_json = msg.payload.decode()

    result = subprocess.run(['python', 'app.py', '--message', message_json], capture_output=True, text=True)

    try:
        response = json.loads(result.stdout)

    except json.JSONDecodeError:
        print('Error: Mapper Did Not Return JSON')

    else:
        client.publish(response['topic'], json.dumps(response['message']))

if __name__ == "__main__":
    try:
        with open('template.json', 'r') as f:
            template = json.loads(f.read())[0]
        inbound_topic = template['subscriptionTopic']
        print(f'Found Dynamic Mapper Template')

    except FileNotFoundError:
        inbound_topic = os.getenv('INBOUND_TOPIC')
        print(f'Using Environment Topic: {inbound_topic}')

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, clientId)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(serverUrl, port)
    client.loop_forever()

    print("Exiting...")
    exit(0)