
from Tkinter import *
import time
import tkFileDialog
import visa
from visa import constants
import math
import os

canvas_width = 800
canvas_height = 300
entry_width = 80
default_ymax = 27.0
default_ymin = 23.0
default_ambmax = 27.0
default_ambmin = 23.0
yvalue2 = default_ymin+3*((default_ymax-default_ymin)/4)
yvalue3 = default_ymin+((default_ymax-default_ymin)/2)
yvalue4 = default_ymin+((default_ymax-default_ymin)/4)

ambvalue2 = default_ambmin+3*((default_ambmax-default_ambmin)/4)
ambvalue3 = default_ambmin+((default_ambmax-default_ambmin)/2)
ambvalue4 = default_ambmin+((default_ambmax-default_ambmin)/4)
master = Tk()
var = IntVar()
sf = IntVar()
enstatus =1
master.title("DTC03 Testing")

rm = visa.ResourceManager()
dmm = rm.open_resource('ASRL9::INSTR')
dmm.stop_bits=constants.StopBits.two
dmm.write("*CLS")
dmm.write("SYST:REM")

x1 =0
z=[]
z2=[]

boolupdate = 0

w = Canvas(master, width=canvas_width,height=canvas_height, bg= "black")
w2 = Canvas(master, width = canvas_width, height = canvas_height, bg="black")
def runvisa():
	global x1
	global y1
	global canvas_width
	global canvas_height
	global z
	global z2
	global default_ymin
	global default_ymax
	global default_ambmax
	global default_ambmin
	global boolupdate
	global enstatus
	global sf
	w.delete("all")
	totaltime = int(maxtime.get())
	dt=float(steptime.get())
	if (dt>0.5):
		dt = dt-0.5
	else:
		dt =0
	plotxrange = int(totaltime/(dt+0.5))
	
	if(sf.get()==1):
		fps = filepath.get()
		snn=sn.get()
		fps+= snn
		fps+='.txt'
		thefile = open(fps, 'w')
		thefile.write("Model:DTC03 S/N:"+snn+'\n')
		thefile.write("Date:"+time.strftime("%c")+'\n')
		if(var.get()==1):
			thefile.write("time"+'\t'+"volt"+'\t'+"Tact"+'\t'+"Tamb"+'\n')
		else:
			thefile.write("time"+'\t'+"res"+'\t'+"Tact"+'\t'+"Tamb"+'\n')

	yplot1 =0
	tplot1=0
	tstart = time.time()

	for index in range(0, plotxrange):

		if(sf.get()==1):
			tread = (time.time()-tstart)
			if(tread <0.01):
				tread =0
			thefile.write(str("%3.4f" %tread)+'\t')

		if(enstatus ==0):
			enstatus =1
			x1=0
			z=[]
			z2=[]
			yplot1=0
			boolupdate =0
			return		
		if(var.get() == 1):

			y=dmm.query("MEAS:VOLT:DC?")	
			#y=1.9
			tempact =(1/(math.log((float(y))/2.0)/3988+0.003354))-273.15
		else :
			y=dmm.query("MEAS:RES?")
			#y=10000
			tempact =1/ (math.log(float(y)/10000)/3988+0.003354)-273.15

		time.sleep(dt)
		tamb = dmm.query("MEAS:CURR:DC?")	
		#tamb=0.000298
		tempamb = float(tamb)*1000000-273.15
		#tempamb =tamb
		z.append(tempact)
		z2.append(tempamb)
		yplot = canvas_height-(tempact-default_ymin)*(canvas_height)/(default_ymax-default_ymin)
		tplot = canvas_height-(tempamb-default_ambmin)*(canvas_height)/(default_ambmax-default_ambmin)
		x = index*canvas_width/plotxrange


		if ((index > 0) & (yplot>=0) & (yplot <= canvas_height) &(yplot1 >=0) & (yplot <=canvas_height)):
			w.create_line(x1, yplot1, x, yplot, fill = "yellow", width =3)
		
		if ((index > 0) & (tplot>=0) & (tplot <= canvas_height) &(tplot1 >=0) & (tplot <=canvas_height)):
			w2.create_line(x1, tplot1, x, tplot, fill = "yellow", width =3)
		x1 = x
		yplot1 = yplot
		tplot1 = tplot
		if(sf.get()==1):
			thefile.write("%3.4f" %float(y)+'\t'+"%3.4f" %tempact +'\t'+"%3.4f" %tempamb +'\n')
			
		if(boolupdate):
			w.delete("all")
			w2.delete("all")
			for i in range(0, index):
				x = i*canvas_width/plotxrange
				yplot= canvas_height-(z[i]-default_ymin)*(canvas_height)/(default_ymax-default_ymin)
				tplot = canvas_height-(z[i]-default_ambmin)*(canvas_height)/(default_ambmax-default_ambmin)
				
				if ((i > 0) & (yplot>=0) & (yplot <= canvas_height) &(yplot1 >= 0) & (yplot <= canvas_height)):
					w.create_line(x1, yplot1, x, yplot, fill = "yellow", width =3)
				
				if ((index > 0) & (tplot>=0) & (tplot <= canvas_height) &(tplot1 >=0) & (tplot <=canvas_height)):
					w2.create_line(x1, tplot1, x, tplot, fill = "yellow", width =3)

				x1 = x
				yplot1 = yplot
				tplot1 = tplot
			w.update()
			w2.update()
			boolupdate =0
		w.update()
		w2.update()
		tact.config(text = "Tact:"+str("%3.4f" %tempact))
		tambe.config(text = "Tamb:"+str("%3.4f" %tempamb))

		
	z=[]
	thefile.close

def updatey():
	global default_ymax
	global default_ymin
	global default_ambmax
	global default_ambmin
	global boolupdate

	tempmax = float(ymax.get())
	tempmin = float(ymin.get())
	tempambmax = float(tmax.get())
	tempambmin = float(tmin.get())
	if(tempmin < tempmax):
		default_ymax=float(ymax.get())
		default_ymin=float(ymin.get())
		yvalue2 = default_ymin+3*((default_ymax-default_ymin)/4)
		yvalue3 = default_ymin+((default_ymax-default_ymin)/2)
		yvalue4 = default_ymin+((default_ymax-default_ymin)/4)

		texty2.config(text = str(yvalue2))
		texty3.config(text = str(yvalue3))
		texty4.config(text = str(yvalue4))
	if(tempambmin < tempambmax):
		default_ambmax=float(tmax.get())
		default_ambmin=float(tmin.get())
		ambvalue2 = default_ambmin+3*((default_ambmax-default_ambmin)/4)
		ambvalue3 = default_ambmin+((default_ambmax-default_ambmin)/2)
		ambvalue4 = default_ambmin+((default_ambmax-default_ambmin)/4)

		textt2.config(text = str(ambvalue2))
		textt3.config(text = str(ambvalue3))
		textt4.config(text = str(ambvalue4))



def stopbutton():
	global enstatus
	enstatus =0


def paste(self, event):
	text = self.selection_get(selection='CLIPBOARD')
	self.insert('insert', text)



		
runbutton = Button(master, text ="Run", command = runvisa)
stopbutton = Button(master, text = "Stop", command = stopbutton)
updatebutton = Button(master, text ="Update", command = updatey)

filepath_l =Label(master, text= "File path:")
savef = Checkbutton(master, text = "Save File", variable =sf, onvalue =1, offvalue = 0)

maxt_l = Label(master, text = "Max time(s)")
step_l = Label(master, text = "Time step (s)")

texty2 = Label(master, text = str(yvalue2))
texty3 = Label(master, text = str(yvalue3))
texty4 = Label(master, text = str(yvalue4))

textt2 = Label(master, text = str(ambvalue2))
textt3 = Label(master, text = str(ambvalue3))
textt4 = Label(master, text = str(ambvalue4))

tambe = Label(master, text ="Tamb:"+"%3.1f" %(25), bg="black", fg="yellow", font=("Arial",16))
tact = Label(master, text = "Tact:"+"%3.4f" %(25), bg="black", fg="yellow", font=("Arial",16))
sn_l = Label(master, text="S/N:")

filepath = Entry(master, width = 50)
ymax = Entry(master, width = 6)
ymin = Entry(master, width = 6)
tmax = Entry(master, width = 6)
tmin = Entry(master, width = 6)
maxtime = Entry(master, width = 15)
steptime = Entry(master, width =15)
sn = Entry(master, width= 15)
measureV = Radiobutton(master, text = "measure voltage", variable = var, value =1)
measureR = Radiobutton(master, text = "measure resistor", variable = var, value =2)

filepath_l.grid(row=0, column =0, sticky =W)
filepath.grid(row =0, column = 1, columnspan =2, sticky = EW)
sn_l.grid(row =0, column =3, sticky =E)
sn.grid(row=0, column =4, sticky =W)
savef.grid(row = 0, column =5)

maxt_l.grid(row =1, column =1,  sticky =E)
maxtime.grid(row=1, column =2, sticky =W)
measureV.grid(row = 1, column =3)
tambe.grid(row=1, column =4, sticky = EW)
runbutton.grid(row=1, column=5)
updatebutton.grid(row=2, column=0)
step_l.grid(row=2, column=1, sticky=E)
steptime.grid(row=2, column =2, sticky =W)
measureR.grid(row = 2, column =3)
tact.grid(row=2, column =4, sticky = EW)
stopbutton.grid(row =2, column=5)
ymax.grid(row =3, column=0, sticky =N)
texty2.grid(row=4,column =0, sticky= N)
texty3.grid(row=5,column =0)
texty4.grid(row=6,column =0, sticky= S)
ymin.grid(row =7, column=0, sticky= S)
w.grid(row=3 ,column=1, rowspan =5,columnspan=5)
tmax.grid(row =8, column=0, sticky =N)
textt2.grid(row=9,column =0, sticky= N)
textt3.grid(row=10,column =0)
textt4.grid(row=11,column =0, sticky= S)
tmin.grid(row =12, column=0, sticky= S)
w2.grid(row=8 ,column=1, rowspan =5,columnspan=5)
ymax.insert(0, str(default_ymax))
ymin.insert(0, str(default_ymin))
tmax.insert(0, str(default_ambmax))
tmin.insert(0, str(default_ambmin))

filepath.insert(0,os.getcwd()+'\\' )


master.mainloop()
