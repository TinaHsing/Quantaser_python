import serial
import serial.tools.list_ports
from Tkinter import *

master =Tk()
master.title("Quantaser Single Photon Counting Module")
output ="waiting command"


def build_connection():
    global ser
    listports = serial.tools.list_ports.comports()
    c=0   
    for a in listports:
        if a[2] =='FTDIBUS\\VID_0403+PID_6001+A906QSELA\\0000':
            c = a[0]

    if c==0:
        outtext.config(text ="device not found")
    else:
        ser=serial.Serial(c)
        outtext.config(text ="device connnected")
        ser.baudrate = 115200
        ser.timeout = 0.5
def ask_datacount():
    global ser
    global datacount

    askcount = list([2])
    ser.write(askcount)
    outtext.config(text ="Asking Datacount...")
    d1 = ord(ser.read())
    d2 = ord(ser.read())
    d3 = ord(ser.read())
    datacount = d2*256+d1
    outtext.config(text ="Datacounts:"+str("%d" %datacount))
def read_time():
    global ser
    reqdata = list([8])
    ser.write(reqdata)
    outtext.config(text ="Asking Timing Data")
    d1 = ord(ser.read())

    d2 = ord(ser.read())

    d3 = ord(ser.read())

    d4 = ord(ser.read())

    coarse = (d4 & 0x3F)*65536 + d3*256+d2
    ch = (d4 & 0xC0)/64
    outtext.config(text ="ch:"+str("%d" %ch) + "fine code:"+str("%x" %d1)+"coarse code:"+str("%x" %coarse))
                   
  



    
    
request = Button(master, width = 20, text ="Read Timming Data:", command = read_time)

datacount = Button(master, width = 20,text ="CheckDataCount", command = ask_datacount)
filepath = Entry(master, width = 50)
outtext = Label(master, bg="black", fg="green", width =50,text = str(output))   
    
datacount.pack()
request.pack()

filepath.pack()
outtext.pack()
build_connection()
master.mainloop()
