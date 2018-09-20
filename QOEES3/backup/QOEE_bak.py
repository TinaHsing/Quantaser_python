from Tkinter import *
from ttk import *
import serial
import time
import threading
import spcm




root = Tk() # creat a top-level window
master = Frame(root, name ='master')
master.pack(fill=BOTH)#fill both side of the paraent.

root.title("Quantum Optics Education Experiment")
root.protocol("WM_DELETE_WINDOW", master.quit)

nb = Notebook(master, name='nb') # create Notebook in "master"
errmsg = Label(master, text ="ttt")
errmsg.pack() 
nb.pack(fill=BOTH, padx=2, pady=3)


exp0 = Frame(nb, name ='exp0')
nb.add(exp0, text ="Preparation")
exp1 = Frame(nb, name = 'epx1')
nb.add(exp1, text ="Photon Statics")
exp2 = Frame(nb, name  = 'exp2')
nb.add(exp2, text ="Hanbury Brown_Twiss")

# build connection with COM port
portlist = serial.tools.list_ports.comports()
cp =0
askdc = list([1]) # ask datacount
askti = list([2]) # ask time data
sendreset = list([4]) # send reset to spcm

for a in portlist:
	if "0403:6001" in a[2]:
		cp = a[0]
if cp ==0:
	errmsg.config(text ="Can't find COM port wiht SPCM module", foreground = "red")
else:
	ser = serial.Serial(cp)
	ser.baudrate = 115200
	ser.timeout = 0.5
	finestep = spcm.CheckFinestep(ser)
	finestep = float(finestep/1000)
	errmsg.config(text="Finestep:"+str("%1.4f" %finestep))
# =====global variable define and sub module for exp0=======
timeselect = StringVar(exp0)
key_runstop = IntVar(exp0)

def PhotonCount0():
	global ser
	global runindex0
	global exp0_thread
	runindex0 =1
	ts =timeselect.get()
	if ts == "0.2s" :
		delaytime = 0.2
	elif ts == "0.5s" :
		delaytime = 0.5
	else:
		delaytime =1

	while runindex0 :
		pc =spcm.LoadCount(ser, delaytime, askdc, sendreset, 1)
		Label0_PhotoCountOut.config(text =str(pc))
def Exp0photoncount():
	print "thread start"
	exp0_thread = threading.Thread(target = PhotonCount0)
	exp0_thread.setDaemon(True)
	exp0_thread.start()
def stop_photoncount():
	global runindex0
	runindex0 =0
#===== global variable and sub module define for =====exp1
chselect = StringVar(exp1)
ch0coarse =[]
#ch0coarse =[901, 3457, 8968, 13456, 27890, 56789, 92134, 145987, 881326, 952345, 1090987, 4692768, 6105347, 9087533]
ch1coarse =[]
ch0fine =[]
ch1fine =[]
histo_out=[]
def PhotonCount1():
	global ser
	global runindex1
	global sendreset
	global askdc
	global exp1_thread
	runindex1 =1
	#ser.write(sendreset)
	while runindex1 :
		pc =spcm.LoadCount(ser, 0.5, askdc, sendreset, 0) # update the photon count every 0.5s and do not reset
		Label1_CountOut.config(text =str(pc))
def Exp1PhotonCount():
	global exp1_thread
	exp1_thread = threading.Thread(target = PhotonCount1)
	exp1_thread.setDaemon(True)
	exp1_thread.start()
def LoadData():
	global ser
	global askdc, askti
	global ch0coarse, ch0fine, ch1coarse, ch1fine
	global runindex1
	runindex1 = 0
	exp1_thread.join()
	spcm.LoadData(ch0coarse, ch0fine, ch1coarse, ch1fine, ser, askdc, askti)
	#print ch0coarse
def Exp1LoadButton():
	global exp1_thread
	global exp1_thread2
	exp1_thread2 = threading.Thread(target = LoadData)
	exp1_thread2.setDaemon(True)
	exp1_thread2.start()
	errmsg.config(text ="Start Loading Data", foreground ="black")
def TimeAnalysis():
	global ch0coarse, ch1coarse
	global exp1_thread2
	file1 = open("ch0_out.txt","w")
	file2 = open("count.txt","w")
	countarray =[]
	yout =[]
	xout =[]
	xlabel =[]
	ylabel =[]
	timegetstr1 =timeset1.get()
	if timegetstr1 =="":
		errmsg.config (text ="Please input the analysis time interval", foreground ="red")
		return 0
	else : 
		int_timeset = int(timegetstr1)*100 #Timeset1 will get
		exp1_thread2.join()
		errmsg.config(text ="Load data finished, analysising", foreground ="black")
		if chselect.get() == "CH0":
			countarray = spcm.CoarseHistoAnalysis(ch0coarse, int_timeset)
		else:
			countarray = spcm.CoarseHistoAnalysis(ch1coarse, int_timeset)
		
		histo_out =spcm.PhotonCountHistogram(countarray)
	
	#histo_out = [0,30,80,1150, 643, 425, 90, 0]
	lenhis = len(histo_out)
	xarray =[i for i in xrange (0, lenhis)]
	spcm.PlotCalculation(histo_out, xarray, 480, 600, 100, yout, xout, xlabel, ylabel)
	Plot1.delete("all")
	Plot1.create_line(99, 0, 100,481, 700, 481, width = 1, fill="black")
	for i in xrange(0, lenhis):
		Plot1.create_rectangle(xout[i], 480, xout[i+1], yout[i], fill="blue")
	for i in xrange(0, 5):
		Plot1.create_text(120+i*140, 505, text =str(ylabel[i]))
		Plot1.create_text(50, 460-i*110, text = str(xlabel[i]))
	print yout
	print xout
	print xlabel
	print ylabel

	for i in xrange(0, len(ch0coarse)):
		file1.write(str(ch0coarse[i])+"\n")
	for i in xrange(0, len(countarray)):
		file2.write(str(countarray[i])+"\n")
	file1.close()
	file2.close()

def LoadandPlot():
	global runindex1
	global ser
	global askdc
	global askti
	global chselect
	global timeset1
	global Plot1

	datacountoffset =0
	ser.write(sendreset)
	ch0coarse =[]
	ch0fine =[]
	ch1coarse =[]
	ch1fine =[]
	countarray=[]
	histo_out =[]
	xlabel =[]
	ylabel =[]
	xarray =[]
	yarray =[]
	runindex1 =1
	int_timeset = int(timeset1.get())*100 #Timeset1 will get
	if chselect.get() == "CH0" :
		ch =0
	else:
		ch =1

	spcm.LoadData(ch0coarse, ch0fine, ch1coarse, ch1fine, ser, askdc, askti)
	if ch:
		countarray =spcm.CoarseHistoAnalysis(ch1coarse, int_timeset)
	else:
		countarray =spcm.CoarseHistoAnalysis(ch0coarse, int_timeset)
	maxpc = max(countarray)
	histo_out =spcm.PhotonCountHistogram(countarray)
	pcarray = [i for i in range (0, maxpc+1)]
	
	
	spcm.PlotCalculation(histo_out, pcarray, yarray, xarray, xlabel, ylabel)
	Plot1.create_line(99, 0, 100,481, 700, 481, width = 1, fill="black")

	for i in xrange (0, maxpc):
		Plot1.create_retectangle(xarray[i], 0, xarray[i+1], yarray[i], fill = "blue")

	for i in xrange (0, 5):
		Plot.create_text()





	





	




#======start the pannel arrangement of exp0 =======



Label0_PhotoCount = Label(exp0, text ="Photon Count", anchor ="center")
Label0_PhotoCountOut = Label(exp0, text ="0",font = ("Arial", 30), width=40, anchor="e")

Label0_SelectTime = Label(exp0, text="Select Detection Time interval")
TimeOption0 = OptionMenu(exp0, timeselect, "0.5s", "0.2s", "0.5s", "1s")

runbutton0 = Button(exp0, text ="Run", command = Exp0photoncount)
stopbutton0 = Button(exp0, text ="Stop", command = stop_photoncount)

Label0_PhotoCount.grid(column =0, row =0)
Label0_PhotoCountOut.grid(column =0, row =2)
Label0_SelectTime.grid(column =1, row =0)
TimeOption0.grid(column =1, row =1,sticky = W)
runbutton0.grid(column=1, row =2, sticky = W)
stopbutton0.grid(column=1, row=3, sticky = W)


#======start the pannel arrangement of exp1 =======

Label1_title = Label(exp1, text ="Photon Count Histogram", anchor ="center")
Plot1 = Canvas(exp1, height =530, width = 700, bg ="white")
Label1_Count = Label(exp1, text ="Total Photon Counts")
Label1_CountOut = Label(exp1, text ="0", anchor ="e")
Label1_SelectCh = Label(exp1, text ="Select the APD Channel")
ChOption1 = OptionMenu(exp1, chselect, "CH0", "CH0", "CH1")
Label1_timeset = Label(exp1, text="Input analysis time interval(us)")
timeset1 = Entry(exp1)
Runbutton1 = Button(exp1, text ="RUN", command = Exp1PhotonCount)
Loadbutton1 = Button(exp1, text ="Load", command = Exp1LoadButton)
Anabutton1 = Button(exp1, text ="Analysis", command = TimeAnalysis)
savebutton1 = Button(exp1, text = "Save data", command = master.quit)




Label1_title.grid (column =0, row =0)
Plot1.grid(column =0, row =1, rowspan= 8)
Label1_Count.grid(column =1, row =0)
Label1_CountOut.grid(column =1, row = 1)
Label1_SelectCh.grid(column =1, row =2)
ChOption1.grid(column = 1, row =3)
Label1_timeset.grid(column =1, row=4)
timeset1.grid(column =1, row =5)
Runbutton1.grid(column =1, row =6)
Loadbutton1.grid(column =1, row =7)
Anabutton1.grid(column =1, row =8)
savebutton1.grid(column=1, row =9)





#=======end the pannel arrangement of exp1 ========


#======start the pannel arrangement of exp2 =======

#=======end the pannel arrangement of exp2 ========
master.mainloop()





