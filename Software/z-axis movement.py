# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 13:20:14 2023

@author: luke_
"""

import matplotlib.pyplot as plt
import numpy as np
import serial
from picamera2 import Picamera2
import time

baudrate=115200
ser = serial.Serial('/dev/ttyUSB0', baudrate)
folder = "/home/pipi/Desktop/snakez/"

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start()
    
speed=1500
pas =0.2
nb_image= 50
for i in range (nb_image):
    picam2.capture_file(f"{folder}_{i}.tif")#We capture the camera photo and put it into the folder
    time.sleep(0.2)
    zcode ="G91\n G0Z-"+ str(pas) + "F" +str(speed) + "\n"
    zcode=zcode.encode('utf-8')
    ser.write(zcode)
    time.sleep(0.2)

