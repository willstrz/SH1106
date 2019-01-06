import os
import time
from time import sleep, strftime
from lib_sh1106 import sh1106
from PIL import ImageFont, ImageDraw, Image
from smbus import SMBus

i2cbus = SMBus(1)
oled = sh1106(i2cbus)
draw = oled.canvas

font = ImageFont.load_default()

while True:
    timeFont = ImageFont.truetype('04B_30__.ttf', 13)
    dateFont = ImageFont.truetype('Pixellari.ttf', 15)
    draw.text((0, 14), strftime('%I:%M:%S %p')  , font=timeFont, fill=1)
    draw.text((0, 30), strftime('%a, %b %d %Y'), font=dateFont, fill=1)
    oled.display()
    oled.cls()
