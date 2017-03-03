import threading

import paho.mqtt.client as mqtt

display = ()


def get_name():
    return 'MQTT Plugin'


def run(cfg, displaydict):
    print threading.currentThread().getName(), ' starting'
    global display
    display = displaydict
    mqtt_server = cfg['mqtt']['server'] or 'localhost'
    mqtt_port = cfg['mqtt']['port'] or 1883
    mqtt_topic = cfg['mqtt']['topic'] or 'matrixzero'

    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect

    client.connect(mqtt_server, mqtt_port, 60)
    client.subscribe(mqtt_topic)

    client.loop_forever()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
