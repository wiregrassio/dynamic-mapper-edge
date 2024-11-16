#!/usr/bin/env python

import paho.mqtt.client as mqtt
import time, signal, datetime, json, random, math

# client, user and device details
serverUrl   = "127.0.0.1"
port        = 1883
clientId    = "doesnt_matter"
connection_flag = False

#---------- Clean Exit Handler
def signal_handler(signum, frame):
	global run
	run = False
	exit()
	
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

#---------- MQTT Handlers
def on_connect(client, userdata, flags, reason_code_list, properties):
    global connection_flag
    connection_flag = True
    print ('Running...')


if __name__ == "__main__":
#---------- MQTT Client Connect
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, clientId)
    client.on_connect = on_connect

    client.connect(serverUrl, port)
    client.loop_start()

    while not connection_flag:
        time.sleep(0.1)

    start = time.time()
    run = True
    while run: #Triggered by SIGINT or SIGTERM. See Clean Exit Handler function
        temp = round(mean_temp + 5* math.sin(math.radians((time.time()-start)*360/cycle_time))+random.random()-0.5,2)

        payload = {
            "type": "c8y_TemperatureMeasurement",
            "time": datetime.datetime.now().isoformat(),
            'c8y_Temperature': {
                'reportedTemp': {
                    "value": temp,
                    "unit": 'C'
                }
            }
        }

        client.publish(pub_topic, json.dumps(payload))

        time.sleep(5)