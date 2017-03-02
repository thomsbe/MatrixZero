import argparse
import threading

import paho.mqtt.client as mqtt
from luma.core.legacy import show_message
from luma.core.legacy.font import proportional, CP437_FONT
from luma.core.serial import spi, noop
from luma.led_matrix.device import max7219


def showmsg(device, content):
    show_message(device, content, fill="white", font=proportional(CP437_FONT))


def display(cascaded, block_orientation):
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=cascaded or 1, block_orientation=block_orientation)

    showmsg(device, "MatrixZero Start")

    d = displayer(device)
    d.start()


class displayer(threading.Thread):
    def __init__(self, device):
        threading.Thread.__init__(self)
        self.device = device

    def run(self):
        pass

    def start(self):
        pass


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


def subscriber(mqtt_server, mqtt_port, topic):
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect

    client.connect(mqtt_server, mqtt_port, 60)
    client.subscribe(topic)

    client.loop_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MatrixZero Arguments',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--cascaded', '-n', type=int, default=4, help='Number of cascaded MAX7219 LED matrices')
    parser.add_argument('--block-orientation', '-o', type=str, default='vertical', choices=['horizontal', 'vertical'],
                        help='Corrects block orientation when wired vertically')
    parser.add_argument('--mqtt-server', '-s', type=str, default='localhost', help='MQTT Server')
    parser.add_argument('--mqtt-port', '-p', type=int, default=1883, help='MQTT Port')
    parser.add_argument('--topic', '-t', type=str, default='matrixzero', help='Subscribe this topic for messages')

    args = parser.parse_args()

    try:
        display(args.cascaded, args.block_orientation)
        subscriber(args.mqtt_server, args.mqtt_port, args.topic)
    except KeyboardInterrupt:
        pass
