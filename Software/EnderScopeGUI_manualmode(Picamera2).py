import tkinter as tk
import tkinter.ttk as ttk
import serial
from picamera2 import Picamera2, Preview
from PIL import Image, ImageTk
import time

ser = serial.Serial('/dev/ttyUSB0', baudrate=115200)
folder = "/home/pipi/Desktop/snakez/" #localisation des images de sortie
color="color"
class Manualguiv4:
    def __init__(self, master=None):
        # build ui
        self.fram_main = tk.Tk() if master is None else tk.Toplevel(master)
        self.fram_main.configure(height=800, width=800)
        self.fram_main.title("Manual Mode")
        #button creation

        Up = ttk.Button(self.fram_main)
        Up.configure(text='Up')
        Up.grid(column=5, padx=20, row=3, pady=20)
        Up.configure(command=self.MoveForwards)
        
        Left = ttk.Button(self.fram_main)
        Left.configure(text='Left')
        Left.grid(column=4, padx="20 0", row=4)
        Left.configure(command=self.MoveLeft)
        Right = ttk.Button(self.fram_main)
        Right.configure(text='Right')
        Right.grid(column=6, row=4)
        Right.configure(command=self.MoveRight)
        Down = ttk.Button(self.fram_main)
        Down.configure(text='Down')
        Down.grid(column=5, row=5)
        Down.configure(command=self.MoveBackwards)
        label1 = ttk.Label(self.fram_main)
        label1.configure(font="TkHeadingFont", text='XY')
        label1.grid(column=5, row=4)
        label3 = ttk.Label(self.fram_main)
        label3.configure(justify="center", font="TkHeadingFont", text='Z')
        label3.grid(column=2, padx=10, row=4)
        button5 = ttk.Button(self.fram_main)
        button5.configure(text='Back to Home')
        button5.grid(column=7, row=6)
        button5.configure(command=self.Backtohome)
        button1 = ttk.Button(self.fram_main)
        button1.configure(text='^^')
        button1.grid(column=2, row=2, pady=20)
        button1.configure(command=self.Zupcoarse)
        button2 = ttk.Button(self.fram_main)
        button2.configure(text='⌄')
        button2.grid(column=2, row=5, pady=20)
        button2.configure(command=self.Zdownfine)
        button3 = ttk.Button(self.fram_main)
        button3.configure(text='^')
        button3.grid(column=2, row=3, pady=20)
        button3.configure(command=self.Zupfine)
        button4 = ttk.Button(self.fram_main)
        button4.configure(text='⌄⌄')
        button4.grid(column=2, row=6, pady=20)
        button4.configure(command=self.Zdowncoarse)
        frame2 = ttk.Frame(self.fram_main)
        frame2.configure(height=400, width=400)
        frame2.grid(column=1, row=4, padx=20)
        
        self.label_cam = ttk.Label(frame2)
        self.label_cam.grid(column=1, row=1)
        
        button6 = ttk.Button(self.fram_main)
        button6.configure(text='Snap Image')
        button6.grid(column=1, row=5)
        button6.configure(command=self.Snap)

        # Main widget
        self.mainwindow = self.fram_main
        
        # initialize picamera2
        self.picam2 =Picamera2()
        #create windows preview
        self.picam2_config=self.picam2.create_preview_configuration(main={"size":(320,240)})
        self.picam2.configure(self.picam2_config)
        #Start the camera
        self.picam2.start()
        #Pre-allocate the  buffer for efficiency
        self.photo= None
        #start capturing and updating the GUI
        self.update_preview()
        
        

        
    def update_preview(self):
        
        
        image = self.picam2.capture_array() #take image
        photo= ImageTk.PhotoImage(image=Image.fromarray(image))#transform the array in an Image and display it
        self.label_cam.config(image=photo)
        self.label_cam.image=photo #Update the camera slot with the new photo
        self.fram_main.after(10,self.update_preview)#time=10, after countdown reloop the update_preview
        
        
        
    def run(self):
        self.mainwindow.mainloop()
        
    def Snap(self):
       #save the current photo into the directory folder
        self.picam2.capture_file(f"{folder}" + color + time.strftime("%H%M%S") + ".tif")
        print("snap")
        
        
    def Backtohome(self):
        #colse the windows
        print("back to home")
        self.mainwindow.destroy()
        
    def MoveLeft(self):
        Left = b'G91\n G1X-8.5F1000\n' #G21 is metric units, G91 means move in relative postion, G1X means move X, F is speed
       # Left = Left.encode('utf-8') #idk whats going on here something about converting bytes to unicode. We needed this in gesines old code and don't/can't use it for Amy Courtney's code
        ser.write(Left)
        print("I moved Left")
        print(Left)
    #     print (x, y)
        #have something here like __ = last x
        #how do you update 
            
    def MoveRight(self):
        Right = b'G91\n G1X8.5F1000\n' #G21 is metric units, G91 means move in relative postion, G1X means move X, F is speed
        ser.write(Right)
        print("I moved Right")
        print(Right)
        
    def MoveForwards(self):
        Forwards = b'G91\n G1Y10F1000\n' #G21 is metric units, G91 means move in relative postion, G1X means move X, F is speed
        ser.write(Forwards)
        print("I moved Forwards")
        print(Forwards)
        
    def MoveBackwards(self):
        Backwards = b'G91\n G1Y-10F1000\n' #G21 is metric units, G91 means move in relative postion, G1X means move X, F is speed
        ser.write(Backwards)
        print("I moved Backwards")
        print(Backwards)

    def Zupcoarse(self):
        Zupcoarse = b'G91\n G1Z5F1000\n' #G21 is metric units, G91 means move in relative postion, G1X means move X, F is speed
        ser.write(Zupcoarse)
        print("I moved Zupcoarse")
        print(Zupcoarse)

    def Zdownfine(self):
        Zdownfine = b'G91\n G1Z-0.1F1000\n' #G21 is metric units, G91 means move in relative postion, G1X means move X, F is speed
        ser.write(Zdownfine)
        print("I moved Zdownfine")
        print(Zdownfine)

    def Zupfine(self):
        Zupfine = b'G91\n G1Z0.1F1000\n' #G21 is metric units, G91 means move in relative postion, G1X means move X, F is speed
        ser.write(Zupfine)
        print("I moved Zupfine")
        print(Zupfine)

    def Zdowncoarse(self):
        Zdowncoarse = b'G91\n G1Z-5F1000\n' #G21 is metric units, G91 means move in relative postion, G1X means move X, F is speed
        ser.write(Zdowncoarse)
        print("I moved Zdowncoarse")
        print(Zdowncoarse)



if __name__ == "__main__":
    app = Manualguiv4()
    app.run()
        

