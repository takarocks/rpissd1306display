#!/bin/python3

# import socket
import busio
import adafruit_ssd1306
# from PIL import Image, ImageDraw, ImageFont

SCL    = 1
SDA    = 0
HEIGHT = 32
WIDTH  = 128

i2c = busio.I2C(SCL, SDA)
disp = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)
