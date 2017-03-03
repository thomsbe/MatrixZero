import threading
from time import sleep

display = ()


def get_name():
    return 'Time Plugin'


def run(cfg, displaydict):
    global display
    print threading.currentThread().getName(), ' starting'
    while True:
        print display['time']
        sleep(30)
