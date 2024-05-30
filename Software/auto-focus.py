import numpy as np
from PIL import Image
from picamera2 import Picamera2, Preview
import cv2
import serial
import time

# Define, baudrate (amount of bits per seconds), serial (Serial port) and the folder for  saved images
baudrate = 115200
ser = serial.Serial('/dev/ttyUSB0', baudrate)
folder = "/home/pipi/Desktop/Z/"

# Define and setup the camera
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start_preview(Preview.QTGL)
picam2.start()

# Convert the image into grey levels array
def prep(im):
    img = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    return img

############################################################################################
# Entropic calculus function
def H(im):
   p,n = np.histogram(im,bins = np.arange(256))
   p = p / im.size
   ent=0
   for i in p:
       if i != 0 :
           ent = ent - i*np.log2(i)
   return ent

# Laplacian variance calculus function
def Var(im):
    laplacian = cv2.Laplacian(im, cv2.CV_64F)
    variance = laplacian.var()
    return variance

# Sobel gradient calculus function
def sobel(image):
    sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
    sobel = np.sqrt(sobel_x**2 + sobel_y**2)

    variance = sobel.var()
    return variance

# Normalization function
def normalize_measure(measure, measure_min, measure_max):
    return (measure - measure_min) / (measure_max - measure_min)

# Combination of each function (Entropy, Variance of the Laplacian and the Sobel gradient)
def combined(image):
    img_entropy = H(image)
    variance_laplacian = Var(image)
    variance_sobel = sobel(image)

    norm_entropy = normalize_measure(img_entropy, entropy_min, entropy_max)
    norm_laplacian = normalize_measure(variance_laplacian, laplacian_min, laplacian_max)
    norm_sobel = normalize_measure(variance_sobel, sobel_min, sobel_max)

    combined_score = (norm_entropy + norm_laplacian + norm_sobel) / 3
    return combined_score

# Define maximm and minimum of each function to normalize them
entropy_min = 0.0
entropy_max = 8.0
laplacian_min = 0.0
laplacian_max = 1000.0
sobel_min = 0.0
sobel_max = 500.0
############################################################################################

gcode = "G91\n G0Z" + str(50) + "F" + str(1500) + "\n"
gcode = gcode.encode('utf-8')
ser.write(gcode)

def up(pas,speed=1500):
    gcode = "G91\n G0Z" + str(pas) + "F" + str(speed) + "\n"
    gcode = gcode.encode('utf-8')
    ser.write(gcode)
    time.sleep(0.2)
    return
    
def down(pas,speed=1500):
    gcode = "G91\n G0Z-" + str(pas) + "F" + str(speed) + "\n"
    gcode = gcode.encode('utf-8')
    ser.write(gcode)
    time.sleep(0.2)
    return

def boucle():
    pre_val =0
    i=0
    seuil = 0
    pas = 1
    p = pas
    brk = False
    a_monter=False
    while (brk == False):
        if (i != 0) : # Don't enter in the loop if i = 0
            picam2.capture_file(f"{folder}_{i}.tif")
            
            image = cv2.imread(f"{folder}_{i}.tif")
            image_pr = cv2.imread(f"{folder}_{i-1}.tif")

            #Convert into arrays
            image_array = prep(image)
            image_array_pr = prep(image_pr)
            
            print(combined(image_array))
            if (combined(image_array) < combined(image_array_pr)) and (a_monter==True) and (combined(image_array_pr) - combined(image_array) >=0.05 ):
                print(combined(image_array))
                if (p>=0.3):
                    up(2*p)
                    p = p-0.1
                else:
                    gcode = "G61 Z S0" + "\n"
                    gcode = gcode.encode('utf-8')
                    ser.write(gcode)
                    time.sleep(0.2)
                    brk = True
            else:
                if(combined(image_array) > pre_val):
                    pre_val = combined(image_array)
                    gcode = "G60 S0" + "\n"
                    gcode = gcode.encode('utf-8')
                    ser.write(gcode)
                if(a_monter==False):
                    if seuil == 3:
                        a_monter = True
                    else:
                        seuil+=1
                down(p)
        else:
            #Save the current image into the folder
            picam2.capture_file(f"{folder}_{i}.tif")
            pre_val = 0
        i+=1
    return

boucle()