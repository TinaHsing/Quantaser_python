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

exp0 = Frame(nb, name = 'exp0')
nb.add(exp0, text ="Preparation")


exp1 = Frame(nb, name='exp1')
SelectTimeLabel =Label(exp1, text="Set the analysis time interval(ns)")
TimeSet = Entry (exp1)
SelectChannelLabel = Label(exp1, text = "Select the analysis channel")
channelname = StringVar(exp1)
TotaltimeLabel = Label(exp1, text = "Total time (ns)")
Totaltimeout = Label(exp1, text ="0")
#channelname.set("CH0")
chselect = OptionMenu(exp1, channelname, "CH1" , "CH0" , "CH1")
chselect.config(width =15)

HistrogramLabel = Label (exp1, text ="Photon Counting Histrogram")
his1 = Label(exp1, text ="4")
his2 = Label(exp1, text ="3")
his3 = Label(exp1, text ="2")
his4 = Label(exp1, text ="1")
his5 = Label(exp1, text ="0")
pn1 = Label(exp1, text ="0")
pn2 = Label (exp1, text ="1")
pn3 = Label (exp1, text ="2")
pn4 = Label (exp1, text ="3")
pn5 = Label (exp1, text ="4")
plot = Canvas (exp1, width = 600, height = 480, bg ="white")
#plot.create_line(0,30, 30, 60, fill = "blue", width =3)

def loaddata():
	datacount=0
	finearray0 =[]
	finearray1 =[]
	coarsearray1 =[]
	coarsearray0 =[]
	global analyfine 
	global analycoarse 
	global lengthcoarse
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
	datacount = ((d3 << 16)|(d2 << 8) | d1) >>1
	DataCountLabel2.config(text = str(datacount))

	#print "d1:" + str(d1) + ", d2:" +str(d2) +", d3:" +str(d3) + ", datacount: " +str(datacount)
	ser.write(askti)
	for x in xrange(0, datacount):
		d1 = ord(ser.read())
		d2 = ord(ser.read())
		d3 = ord(ser.read())
		d4 = ord(ser.read())
		ch = (d4 & 0x40) >>6
		coarse =((d4 & 0x3F) << 16) | (d3 << 8) | d2 
		if ch:
			coarsearray1.append (coarse)
			finearray1.append(d1)
		else:
			coarsearray0.append ( coarse)
			finearray0.append(d1)

		print "ch:" + str(ch) + ", coarse:" +str(coarse) +", fine: " +str(d1)

	if channelname.get() == "CH0":
		analycoarse = coarsearray0
		analyfine = finearray0
	else:
		analycoarse = coarsearray1
		analyfine = finearray1

	lengthcoarse = len (analycoarse)


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
		analyfine = finearray1

	lengthcoarse = len (analycoarse)
	lengthfine = len(analyfine)

	if lengthcoarse == 0:
		DataCountLabel2.config(text ="Data load Error!")
		return
	if lengthcoarse != lengthfine:
		DataCountLabel2.config(text ="Data number Error!")
		return
	DataCountLabel2.config (text=str(lengthcoarse))

#def historgram():

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
	
	timearray =[]
	timemax =0;
	reset_index =0
	for i in xrange (0, lengthcoarse):
		if analycoarse [i] > analycoarse [i-1]:
			reset_index = reset_index+0x400000
		coarse = analycoarse [i] +reset_index 
		timearray.append(float(coarse)*coarsestep - float(analyfine[i])*finestep)
	Totaltimeout.config(text=str(max(timearray)))

	i = 0
	j = 1
	count =[]
	counttemp =0

	print lengthcoarse
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
	dx = (int((countmax-1)/4)+1)
	xmax = dx*4


	histo = [0 for x in range(xmax)]
	print count
	print countmax
	for i in range(0,len(count)):
		print str(i) +"," +str(count[i])
		histo[count[i]] = histo[count[i]] +1
	dy = int (max(histo)/4) +1
	ymax = 4*dy
	his1.config(text = str(ymax))
	his2.config(text = str(3*dy))
	his3.config(text = str(2*dy))
	his4.config(text = str(dy))
	
	x0 = 0
	for i in range (0, xmax-1):
		x = int(480*(i+1)/xmax)
		y = 600-int(600*histo[i]/ymax)
		if y >= 597:
			y = 597
		plot.create_rectangle(x0, 600, x, y, fill="blue")
		
		print str(i) +","+str(x0) +","+str(y) +","+str(x)
		x0 =x
	

# create each Notebook tab in a Frame


DataCountLabel1 = Label(exp1, text = "Total Data Count")
DataCountLabel2 = Label(exp1, text ="0")

load = Button (exp1, text ="Load", command=loaddata)
anal = Button (exp1, text ="Analysis", command= analysis_array)
save = Button (exp1, text ="Save Data", command=master.quit)


# Button to quit app on right

# start the define of sub module


HistrogramLabel.grid(column =0, row =0, columnspan =6)
his1.grid(column=0, row =1)
his2.grid(column=0, row =5)
his3.grid(column=0, row =9)
his4.grid(column=0, row =13)
his5.grid(column=0, row =17)
plot.grid(column= 1, columnspan = 5, row =1, rowspan =17)

DataCountLabel1.grid (column=6,  row=1)
DataCountLabel2.grid (column=6,  row=2, sticky =E)
SelectChannelLabel.grid(column=6, row =4)
chselect.grid(column=6, row =5)
TotaltimeLabel.grid(column =6, row =6)
Totaltimeout.grid(column =6, row =7, sticky =E)
SelectTimeLabel.grid(column =6,  row =8)
TimeSet.grid(column=6, row =9)

load.grid(column =6,  row =13)
anal.grid(column =6,  row = 15)
save.grid(column=6, row =17)
pn1.grid(column =1, row =18, sticky =W)
pn2.grid(column =2, row =18, sticky =W)
pn3.grid(column =3, row =18)
pn4.grid(column =4, row =18,sticky =E)
pn5.grid(column =5, row =18,sticky =E)

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