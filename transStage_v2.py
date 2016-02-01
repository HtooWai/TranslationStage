""" This is v_2.0 of the GUI (for windows computers) to control stepper motors for the 
    translation stage for the fibre optics cable trimmer (Author: Htoo Wai Htet)
    It communates with the stepper motor through the arduino connected through the serial port
    If you do not hav serial library in your python, you must install it from here: https://pypi.python.org/pypi/pyserial
    This GUI allows user to input the speed (in mm/s), acceleration (in mm/s^2), distance (in mm) and orientation
    (inwards or outwards) of the motor movements, and sends it to the preprogrammed arduino.
"""

""" Version 2.0 updates: conversion is now set to 3200 steps/mm
    Revised limits accordingly. Now updated to have the ability to select which motor to move
"""

""" Ideas for v3.0: Error message if invalid inputs are entered, such as speeed = 0
"""

import serial                   #Serial Library must be installed
from Tkinter import *

arduino = serial.Serial()
def openPort():
    arduino.baudrate = 9600
    arduino.port = port.get()-1         #-1 is added since the serial library uses index values
    arduino.timeout = 1
    arduino.open()
    return

def send():
    speed = str(float(spd.get())*conversion.get())
    acceleration = str(float(acel.get())*conversion.get())
    distance = str(int(dist.get())*conversion.get())
    command = "s" + speed + "a" + acceleration + "d" + distance + "o" + str(direction.get()) + "m" + str(input_method.get())
    #print command
    arduino.write(command)
    return

def closePort():
    arduino.close()
    return

mGui = Tk()
port = IntVar(value = 4)        #default to COM5
conversion = IntVar(value = 3200)    # 500 steps per mm
input_method = IntVar()
direction = IntVar()
spd = StringVar()
acel = StringVar()
dist = StringVar()

mGui.geometry('400x300+500+100')
mGui.title("Stepper Motor Control")

#Choosing the serial port
port_label = Label(mGui, text = "Port: COM ").grid(row = 0, column = 1, sticky = E)
port_entry = Entry(mGui, textvariable = port, width = 3).grid(row = 0, column = 2)

conversion_label = Label(mGui, text = "Conversion: ").grid(row = 1, column = 1, sticky = E)
conversion_entry = Entry(mGui, textvariable = conversion, width = 5).grid(row = 1, column = 2)
conversion_unit = Label(mGui, text = "steps/mm").grid(row = 1, column = 3, sticky = W)

#Input choice
left_radio = Radiobutton(mGui, text = "Left Motor", variable = input_method, value = 1).grid(row = 2, column  = 1, pady = 10)
both_radio = Radiobutton(mGui, text = "Both", variable = input_method, value = 0).grid(row = 2, column  = 2, pady = 10)
right_radio = Radiobutton(mGui, text = "Right Motor", variable = input_method, value =2).grid(row = 2, column  = 3, pady = 10)

#Inputs
spd_label = Label(mGui, text = "Speed: ").grid(row = 3, column = 1, sticky = E)
spd_spin = Spinbox(mGui, textvariable = spd, from_=0.1, to =2, width = 4).grid(row = 3, column = 2)
spd_unit = Label(mGui, text = "mm/s").grid(row = 3, column = 3, sticky = W)

acel_label = Label(mGui, text = "Acceleration: ").grid(row = 4, column = 1, sticky = E)
acel_spin = Spinbox(mGui, textvariable = acel, from_=0, to =1, width = 4).grid(row = 4, column = 2)
acel_unit = Label(mGui, text = "mm/s2").grid(row = 4, column = 3, sticky = W)

dist_label = Label(mGui, text = "Distance: ").grid(row = 5, column = 1, sticky = E)
dist_spin = Spinbox(mGui, textvariable = dist, from_=0, to =25, width = 4).grid(row = 5, column = 2)
dist_unit = Label(mGui, text = "mm").grid(row = 5, column = 3, sticky = W)

in_radio = Radiobutton(mGui, text = "Inwards", variable = direction, value = 1).grid(row = 6, column = 1, pady = 10)
out_radio= Radiobutton(mGui, text = "Outwards", variable = direction, value = 0).grid(row = 6, column = 3, pady = 10)  


#Command buttons
open_button = Button(mGui, text = "Open Port", command = openPort, width = 15).grid(row = 7, column = 1, pady = 10)
send_button = Button(mGui, text = "Send to Arduino", command = send, width = 15).grid(row = 7, column = 2, pady = 10)
close_button = Button(mGui, text = "Close Port", command= closePort, width = 15).grid(row = 7, column = 3, pady = 10)

mGui.mainloop()
