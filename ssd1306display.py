#!/bin/python3

#######################################
# RPi SSD1306 I2C display service
#
# Taka Kitazume
# Version 0.2
# March 1, 2021
#######################################

import time
import socket
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

from flask import Flask, request

# GLOBAL
# I2C 0 interface
SCL    = 1
SDA    = 0
HEIGHT = 32
WIDTH  = 128
TOP    = -2
BOTTOM = HEIGHT - TOP
LEFT   = 2
X0     = 0
Y0     = 0
X1     = WIDTH
Y1     = HEIGHT

i2c   = busio.I2C(SCL, SDA)
disp  = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)
image = Image.new("1", (WIDTH, HEIGHT))
draw  = ImageDraw.Draw(image)
font  = ImageFont.load_default()

# Flask server
app = Flask(__name__)

def getIpAddress():
    ip = None
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def setText(text, x=0, y=0, font=font):
    draw.text((LEFT + x, TOP + y), text=text, font=font, fill=255)

def setHostnameIP():
    hostname = socket.gethostname()
    ip = getIpAddress()
    setText(hostname)
    setText("IP: " + ip, y=10)

def clearArea(x0=X0, y0=Y0, x1=X1, y1=Y1):
    draw.rectangle((x0, y0, x1, y1), outline=0, fill=0)
    disp.image(image)
    disp.show()

def clearDisplay():
    clearArea()

def showDisplay():
    disp.image(image)
    disp.show()

@app.route('/showmessage', methods=['GET'])
def showMessage():
    clearArea(y0=20)
    text = request.args.get('text','')
    setText(text, y=20)
    showDisplay()
    return "Success"

@app.route('/shutdown', methods=['GET'])
def shutdown():
    clearDisplay()
    return "Success"

def main():
    clearDisplay()
    setHostnameIP()
    showDisplay()

if __name__ == '__main__':
    main()
    app.debug = True # Debug
    app.run(host='127.0.0.1', port='5000') # Accept access from any host
