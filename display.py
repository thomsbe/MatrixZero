import copy
import imp
import os
import threading

import yaml
from luma.core.legacy import show_message
from luma.core.legacy.font import proportional, CP437_FONT
from luma.core.serial import spi, noop
from luma.led_matrix.device import max7219

PluginFolder = "./plugins"
MainModule = "plugin"

displaydict = ()


def getPlugins():
    plugins = []
    possibleplugins = os.listdir(PluginFolder)
    for i in possibleplugins:
        location = os.path.join(PluginFolder, i)
        if not os.path.isdir(location) or not MainModule + ".py" in os.listdir(location):
            continue
        info = imp.find_module(MainModule, [location])
        plugins.append({"name": i, "info": info})
    return plugins


def loadPlugin(plugin):
    return imp.load_module(MainModule, *plugin["info"])


def showmsg(device, content):
    show_message(device, content, fill="white", font=proportional(CP437_FONT))


def display(cascaded, block_orientation):
    global displaydict
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=cascaded or 1, block_orientation=block_orientation)

    showmsg(device, "MatrixZero Start")

    for item in displaydict:
        print item


if __name__ == "__main__":
    plugins = []
    for i in getPlugins():
        print("Loading plugin " + i["name"])
        p = loadPlugin(i)
        plugins.append(p)

    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    cascaded = cfg['max7219']['cascaded'] or 4
    block_orientation = cfg['max7219']['block_orientation'] or 'vertical'

    threads = []

    try:
        displayer = threading.Thread(target=display, args=(cascaded, block_orientation))
        threads.append(displayer)
        displayer.start()
        for p in plugins:
            p = threading.Thread(name=p.get_name(), target=p.run, args=(cfg, displaydict))
            threads.append(p)
            p.start()
    except KeyboardInterrupt:
        pass
