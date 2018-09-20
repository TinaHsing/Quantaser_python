#! /usr/bin/env python

from Tkinter import *
from ttk import *
import serial
import serial.tools.list_ports

root = Tk() # create a top-level window

master = Frame(root, name='master') # create Frame in "root"
master.pack(fill=BOTH) # fill both sides of the parent
var = IntVar()
coarsestep = 10.0
finestep = 0.04
lengthcoarse =0



root.title('Quantum Optics Educational Experiment Set') # title for top-level window
# quit if the window is deleted
root.protocol("WM_DELETE_WINDOW", master.quit)

nb = Notebook(master, name='nb') # create Notebook in "master"
nb.pack(fill=BOTH, padx=2, pady=3) # fill "master" but pad sides

exp1 = Frame(nb, name='exp1')
SelectTimeLabel =Label(exp1, text="Set the analysis time interval(ns)")
TimeSet = Entry (exp1)
SelectChannelLabel = Label(exp1, text = "Select the analysis channel")
channelname = StringVar(exp1)
#channelname.set("CH0")
chselect = OptionMenu(exp1, channelname, "CH1" , "CH0" , "CH1")
chselect.config(width =15)

HistrogramLabel = Label (exp1, text ="Photon Counting Histrogram")
his1 = Label(exp1, text ="0")
his2 = Label(exp1, text ="0")
his3 = Label(exp1, text ="0")
his4 = Label(exp1, text ="0")
his5 = Label(exp1, text ="0")
plot = Canvas (exp1, width = 600, height = 480, bg ="white")
#plot.create_line(0,30, 30, 60, fill = "blue", width =3)

def loaddata():
	portlist = serial.tools.list_ports.comports()
	cp =0
	for a in portlist:
		if "0403:6001" in a[2]:
			cp = a[0]
	if cp == 0:
		DataCountLabel2.config(text ="Can't find COM PORT!")
	else:
		ser = serial.Serial(cp)
		DataCountLabel2.config(text = "Device Conneted")
		ser.baudrate = 115200
		ser.timeout =0.5
	askdc = list([1])
	askti = list([2])

	ser.write(askdc)
	d1 = ord(ser.read())
	d2 = ord(ser.read())
	d3 = ord(ser.read())
	datacount = (d3 << 16)|(d2 << 8) | d1
	print "d1:" + str(d1) + ", d2:" +str(d2) +", d3:" +str(d3) + ", datacount: " +str(datacount)

def loadfile():

	finearray0 =[]
	finearray1 =[]
	coarsearray0 =[]
	coarsearray1 =[]
	global analycoarse, analyfine
	global lengthcoarse

	f1 = open("testdata.txt","r")
	indata ='0'
	coarsedata0 =0
	coarsedata1 =0
	i =0;
	while True:
		try:
			indata = f1.readline()
			if not indata: break
			if i%2 == 0:
				int_indata = int(indata,16)
				ch = (int_indata & 0x4000)>>14
				if ch:
					coarsedata1 = int_indata & 0x3FFF
				else:
					coarsedata0 = int_indata & 0x3FFF
			else:
				int_indata = int(indata,16)
				coarse_temp = int_indata >>8
				if ch:
					coarsedata1 = (coarsedata1<<8) | coarse_temp
					coarsearray1.append(coarsedata1)
					finearray1.append (int_indata & 0x00FF)
					
				else:
					coarsedata0 = (coarsedata0<<8) | coarse_temp
					coarsearray0.append(coarsedata0)
					finearray0.append(int_indata & 0x00FF)
			i=i+1
		except:
			break

	f1.close()

	if channelname.get() == "CH0":
		analycoarse = coarsearray0
		analyfine = finearray0
	else:
		analycoarse = coarsearray1
		analyfine = finearray1\

	lengthcoarse = len (analycoarse)
	lengthfine = len(analyfine)

	if lengthcoarse == 0:
		DataCountLabel2.config(text ="Data load Error!")
		return
	if lengthcoarse != lengthfine:
		DataCountLabel2.config(text ="Data number Error!")
		return
	DataCountLabel2.config (text=str(lengthcoarse))

# start the analysis process
def analysis_array():
	global coarsestep
	global finestep
	global analyfine
	global analycoarse
	global lengthcoarse
	global plot
	plot.delete("all")
	int_timeset = int(TimeSet.get(), 10) 	
	i =0
	timearray =[]
	timemax =0;
	for i in range (0, lengthcoarse):
		timearray.append(float(analycoarse[i])*coarsestep + float(analyfine[i])*finestep)

	i = 0
	j = 1
	count =[]
	counttemp =0


	while i < lengthcoarse:
		
		if timearray[i] < j*int_timeset:
			counttemp = counttemp+1		
			i = i+1
		else:
			count.append(counttemp)
			counttemp =0	
			j = j+1
	count.append(counttemp)
	countmax = max(count)+1
	xmax = (int((countmax-1)/4)+1)*4

	histogram = [0 for x in range(xmax)]
	print count
	print countmax
	for i in range(0,len(count)):
		print str(i) +"," +str(count[i])
		histogram[count[i]] = histogram[count[i]] +1
	ymax = max(histogram)
	print histogram
	print ymax
	

	for i in range (0, xmax-1):
		x1 = int(480*i/xmax)
		x2 = int(480*(i+1)/xmax)
		y1 = 600-int(600*histogram[i]/ymax)
		y2 = 600-int(600*histogram[i+1]/ymax)
		plot.create_line(x1, y1, x2, y2, fill="blue", width =3)
		print str(i) +","+str(x1) +","+str(y1) +","+str(x2) +","+str(y2)
	
	

# create each Notebook tab in a Frame


DataCountLabel1 = Label(exp1, text = "Total Data Count")
DataCountLabel2 = Label(exp1, text ="0")

load = Button (exp1, text ="Load", command=loadata)
anal = Button (exp1, text ="Analysis", command= analysis_array)
save = Button (exp1, text ="Save Data", command=master.quit)


# Button to quit app on right

# start the define of sub module


HistrogramLabel.grid(column =0, row =0, columnspan =2)
his1.grid(column=0, row =1)
his2.grid(column=0, row =5)
his3.grid(column=0, row =9)
his4.grid(column=0, row =13)
his5.grid(column=0, row =17)
plot.grid(column= 1, row =1, rowspan =17)

DataCountLabel1.grid (column=2,  row=1)
DataCountLabel2.grid (column=2,  row=2, sticky =E)
SelectChannelLabel.grid(column=2, row =4)
chselect.grid(column=2, row =5)
SelectTimeLabel.grid(column =2,  row =6)
TimeSet.grid(column=2, row =7)

load.grid(column =2, columnspan =2, row =13)
anal.grid(column =2, columnspan =2, row = 15)
save.grid(column=2, columnspan =2, row =17)
nb.add(exp1, text="Photon Counting Statistic") # add tab to Notebook

# repeat for each tab
exp2 = Frame(master, name='exp2')
HistrogramLabel = Label (exp2, text ="Second Order Correlaton Function")
#plot = Canvas (exp2, width = 600, height = 480, bg ="white")
load = Button (exp2, text ="Load Data", command=master.quit)
save = Button (exp2, text ="Save Data", command=master.quit)



HistrogramLabel.grid(column =0, row =0, columnspan =2)
#plot.grid(column= 1, row =1, rowspan =3)
load.grid(column =2, row =2)
save.grid(column=2, row =3)




nb.add(exp2, text="Hanbury Brown_Twiss")





# start the app
if __name__ == "__main__":
    master.mainloop() # call master's Frame.mainloop() method.
    #root.destroy() # if mainloop quits, destroy window
# from Tkinter import *
# from ttk import *

# root = Tk()
# root.title("Quantum Optics Educational Experiment Set")
# master = Frame(root, name ="master")
# master.pack(fill=BOTH)
# root.protocol("WM_DELETE_WINDOW", master.quit)

# SelecExpLabel = Label(master, text ="Select Experiment")
# nb = Notebook(master, name='nb') # create Notebook in "master"
# nb.pack(fill=BOTH, padx=2, pady=3) # fill "master" but pad sides


# SelecExpLabel.grid(row=2,column=1)

# if __name__ == "__main__":
#     master.mainloop() # call master's Frame.mainloop() method.
#     #root.destroy() # if mainloop quits, destroy window