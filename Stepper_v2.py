""" This is v2.0 of the GUI (for windows computers) to control stepper motos (Author: Htoo Wai Htet)
    It communates with the stepper motor through the arduino connected through the serial port
    If you do not hav serial library in your python, you must install it from here: https://pypi.python.org/pypi/pyserial
    This GUI allows user to input the direction, amount of revolutions, the amount of microsteps 
    and the delay needed between each microsteps and sends it to the preprogrammed arduino.
"""

""" New in v2.0 are the ability to convert the linear distance and speed values into delay and rev values
    The user have the freedom to choose different methods of input
    There is also a help menu added for addition questions.
"""

import serial                   #Serial Library must be installed
from Tkinter import *

microstep_per_rev = 1600        #driver's microstepping value
overshoot = 30                  #overshoot (in ms) by the program as tested by speed test
arduino = serial.Serial()

def openPort():
    arduino.baudrate = 9600
    arduino.port = '/dev/cu.usbmodem1411'         #-1 is added since the serial library uses index values
    arduino.timeout = 1
    arduino.open()
    return

def send():
    if (input_method.get()):
        command = "R" + rev.get() + "D" + str(direction.get()) + "m" + dlym.get() + "u" + dlyu.get() + "M" + ms.get()
    else:
        rev.set(dist.get()*1000/con.get())
        if (spd.get() != 0):
            dly_float = ((con.get()*1000.0)/float(spd.get())) - (int(rev.get())*overshoot)
            dly_ms = dly_float/1600
            dlym_int = int(dly_ms)
            dlym.set(dlym_int)
            dlyu_int = int((dly_ms - dlym_int) * 1000)
            dlyu.set(dlyu_int)
        command = "R" + rev.get() + "D" + str(direction.get()) + "m" + dlym.get() + "u" + dlyu.get() + "M" + ms.get()         
    arduino.write(command)

def closePort():
    arduino.close()
    return

mGui = Tk()
port = IntVar(value = 5)        #default to COM5
input_method = IntVar()
direction = IntVar()
#circular motion variables
rev = StringVar()
dlym = StringVar()
dlyu = StringVar()
ms = StringVar()
#linear motion variables
con = IntVar(value = 500)
dist = IntVar()
spd = StringVar()

mGui.geometry('500x500+500+100')
mGui.title("Stepper Motor Control")

#Choosing the serial port
port_label = Label(mGui, text = "Port: ").place(x=210,y=25)
port_entry = Entry(mGui, textvariable = port, width = 5).place(x=260,y=25)

#Input choice
input_label = Label(mGui, text = "Choice of input:"). place(x=210, y=65)
dist_radio = Radiobutton(mGui, text = "By linear distance", variable = input_method, value =0).place(x=95,y=85)
rev_radio = Radiobutton(mGui, text = "By circular distance", variable = input_method, value =1).place(x=285,y=85)

#Linear distance inputs
up_radio = Radiobutton(mGui, text = "Upward", variable = direction, value = 1).place(x=75, y=145)
down_radio= Radiobutton(mGui, text = "Downward", variable = direction, value = 0).place(x=75, y=165)

con_label = Label(mGui, text = "Conversion: ").place(x=40, y=205)
con_spin = Spinbox(mGui, textvariable = con, from_=1, to =1000, width = 4).place(x=145, y=205)

dist_label = Label(mGui, text = "Distance (in mm): ").place(x=40, y=235)
dist_spin = Spinbox(mGui, textvariable = dist, from_=1, to =2000, width = 4).place(x=145, y=235)

spd_label = Label(mGui, text = "Speed (in um/s): ").place(x=40, y=265)
spd_spin = Spinbox(mGui, textvariable = spd, from_=0.0, to =999.0, width = 4).place(x=145, y=265)

#Circular distane inputs
ccw_radio = Radiobutton(mGui, text = "Counter-lockwise", variable = direction, value = 1).place(x=305, y=145)
cw_radio= Radiobutton(mGui, text = "Clockwise", variable = direction, value = 0).place(x=305, y=165)

rev_label = Label(mGui, text = "Revolutions: ").place(x=300, y=205)
rev_spin = Spinbox(mGui, textvariable = rev, from_=0, to =1000, width = 4).place(x=390, y=205)

dlym_label = Label(mGui, text = "Delay (in ms): ").place(x=300, y=235)
dlym_spin = Spinbox(mGui, textvariable = dlym, from_=0, to =2000, width = 4).place(x=390, y=235)

dlyu_label = Label(mGui, text = "Delay (in us): ").place(x=300, y=265)
dlyu_spin = Spinbox(mGui, textvariable = dlyu, from_=0, to =999, width = 4).place(x=390, y=265)

ms_label = Label(mGui, text = "Microsteps: ").place(x=300, y=295)
ms_spin = Spinbox(mGui, textvariable = ms, from_=0, to =1599, width = 4).place(x=390, y=295)

#Command buttons
open_button = Button(mGui, text = "Open Port", command = openPort, width = 15).place(x=25,y=400)
send_button = Button(mGui, text = "Send to Arduino", command = send, width = 15).place(x=190,y=400)
close_button = Button(mGui, text = "Close Port", command= closePort, width = 15).place(x=355,y=400)

mGui.mainloop()
