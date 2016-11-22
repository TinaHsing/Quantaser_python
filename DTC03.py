
from Tkinter import *
import time
import tkFileDialog
import visa
from visa import constants
import math
import os

canvas_width = 600
canvas_height = 400
entry_width = 80
default_ymax = 27.0
default_ymin = 23.0
yvalue2 = default_ymin+3*((default_ymax-default_ymin)/4)
yvalue3 = default_ymin+((default_ymax-default_ymin)/2)
yvalue4 = default_ymin+((default_ymax-default_ymin)/4)
master = Tk()
var = IntVar()
sf = IntVar()
enstatus =1
master.title("DTC03 Testing")



x1 =0
z=[]
yplot1 =0
boolupdate = 0
w = Canvas(master, width=canvas_width,height=canvas_height, bg= "black")
def runvisa():
	global taking
	global x1
	global y1
	global canvas_width
	global canvas_height
	global z
	global default_ymin
	global default_ymax
	global boolupdate
	global enstatus
	global sf
	taking =1
	str_rem ='SYST:REM'
	str_measv ='MEAS:VOLT:DC?'
	str_measr ='MEAS:RES?'

	w.delete("all")
	totaltime = int(maxtime.get())
	dt=float(steptime.get())
	if (dt>0.5):
		dt = dt-0.5
	else:
		dt =0
	plotxrange = int(totaltime/(dt+0.5))

	
	resourcename ='ASRL'
	resourcename+=comport.get()
	resourcename+='::INSTR'
	print(resourcename)
	rm = visa.ResourceManager()
	dmm = rm.open_resource(resourcename)

	if(instname.get() =="HP34401A"):
		dmm.stop_bits=constants.StopBits.two
	
	else:
		#dmm.stop_bits=constants.StopBits.one
		str_rem =':'+str_rem
		str_measr=':'+str_measr
		str_measv =':'+str_measv
	dmm.write("*CLS")
	dmm.write(str_rem)

		
	
	if(sf.get()==1):
		fps = filepath.get()
		snn=sn.get()
		fps+= snn
		fps+='.txt'
		thefile = open(fps, 'w')
		thefile.write("Model:DTC03 S/N:"+snn+'\n')
		thefile.write("Date:"+time.strftime("%c")+'\n')
		if(var.get()==1):
			thefile.write("time"+'\t'+"volt"+'\t'+"temp"+'\n')
		else:
			thefile.write("time"+'\t'+"res"+'\t'+"temp"+'\n')

	yplot1 =0
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
			yplot1=0
			boolupdate =0
			return		
		if(var.get() == 1):

			y=dmm.query(str_measv)
			y=1

			tempact =(1/(math.log((float(y))/2.0)/3988+0.003354))-273.15
			
		else :
			y=dmm.query(str_measr)
			y=1
			tempact =1/ (math.log(float(y)/10000)/3988+0.003354)-273.15

		z.append(tempact)
		yplot = canvas_height-(tempact-default_ymin)*(canvas_height)/(default_ymax-default_ymin)
		x = index*canvas_width/plotxrange


		if ((index > 0) & (yplot>=0) & (yplot <= canvas_height) &(yplot1 >=0) & (yplot <=canvas_height)):
			w.create_line(x1, yplot1, x, yplot, fill = "yellow", width =3)
		x1 = x
		yplot1 = yplot

		if(sf.get()==1):
			thefile.write("%3.4f" %float(y)+'\t'+"%3.4f" %tempact +'\n')
			
		if(boolupdate):
			w.delete("all")
			for i in range(0, index):
				x = i*canvas_width/plotxrange
				yplot= canvas_height-(z[i]-default_ymin)*(canvas_height)/(default_ymax-default_ymin)

				if ((i > 0) & (yplot>=0) & (yplot <= canvas_height) &(yplot1 >= 0) & (yplot <= canvas_height)):
					w.create_line(x1, yplot1, x, yplot, fill = "yellow", width =3)
				x1 = x
				yplot1 = yplot
			w.update()
			boolupdate =0
		w.update()
		tact.config(text = str("%3.4f" %tempact))

		time.sleep(dt)
	z=[]
	thefile.close
	taking =0

def updatey():
	global default_ymax
	global default_ymin
	global boolupdate
	global taking

	tempmax = float(ymax.get())
	tempmin = float(ymin.get())
	if(tempmin < tempmax):
		default_ymax=float(ymax.get())
		default_ymin=float(ymin.get())
		yvalue2 = default_ymin+3*((default_ymax-default_ymin)/4)
		yvalue3 = default_ymin+((default_ymax-default_ymin)/2)
		yvalue4 = default_ymin+((default_ymax-default_ymin)/4)

		texty2.config(text = str(yvalue2))
		texty3.config(text = str(yvalue3))
		texty4.config(text = str(yvalue4))
		boolupdate =1
	if (taking==0):
		w.delete("all")
		for i in range(0, index):
			x = i*canvas_width/plotxrange
			yplot= canvas_height-(z[i]-default_ymin)*(canvas_height)/(default_ymax-default_ymin)

			if ((i > 0) & (yplot>=0) & (yplot <= canvas_height) &(yplot1 >= 0) & (yplot <= canvas_height)):
				w.create_line(x1, yplot1, x, yplot, fill = "yellow", width =3)
			x1 = x
			yplot1 = yplot
		w.update()

def stopbutton():
	global enstatus
	enstatus =0



		
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
tact_l = Label(master, text = "Tact:")
tact = Label(master, text = "%3.4f" %(25), bg="black", fg="yellow", font=("Arial",18))
sn_l = Label(master, text="S/N:")
comport_l = Label(master, text ="ASRL")

filepath = Entry(master)
comport = Entry(master, width = 6)

instname = StringVar(master)
instname.set("HP34401A")
instsele = OptionMenu(master, instname, "HP34401A", "Keithley2000")
instsele.config(width =15)
ymax = Entry(master, width = 6, justify='right')
ymin = Entry(master, width = 6, justify='right')
maxtime = Entry(master, width = 15)
steptime = Entry(master, width =15)
sn = Entry(master, width= 15)
measureV = Radiobutton(master, text = "measure voltage", variable = var, value =1)
measureR = Radiobutton(master, text = "measure resistor", variable = var, value =2)

filepath_l.grid(row=0, column =0, sticky =W)
filepath.grid(row =0, column = 1, columnspan =3, sticky = EW)
sn_l.grid(row =0, column =4, sticky =E)
sn.grid(row=0, column =5, sticky =W)
instsele.grid(row=0, column=6)

savef.grid(row = 1, column =0)
maxt_l.grid(row =1, column =1,  sticky =E)
maxtime.grid(row=1, column =2, sticky =W)
measureV.grid(row = 1, column =3)
tact_l.grid(row=1, column =4)
tact.grid(row=1, column =5, sticky = EW)
runbutton.grid(row=1, column=6)




updatebutton.grid(row=2, column=0)
step_l.grid(row=2, column=1, sticky=E)
steptime.grid(row=2, column =2, sticky =W)
measureR.grid(row = 2, column =3)
comport_l.grid(row=2, column =4, sticky = E)
comport.grid(row=2, column=5, sticky =W)
stopbutton.grid(row =2, column=6)


ymax.grid(row =3, column=0, sticky =NE)
texty2.grid(row=4,column =0, sticky= NE)
texty3.grid(row=5,column =0, sticky =E)
texty4.grid(row=6,column =0, sticky= SE)
ymin.grid(row =7, column=0, sticky= SE)

w.grid(row=3 ,column=1, rowspan =5,columnspan=6)
ymax.insert(0, str(default_ymax))
ymin.insert(0, str(default_ymin))

filepath.insert(0,os.getcwd()+'\\' )


master.mainloop()
