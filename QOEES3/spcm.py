import serial
import serial.tools.list_ports
import time

def BuildConnection(ser, errmsg):
	portlist = serial.tools.list_ports.comports()
	cp =0
	print "try reconnect"

	for a in portlist:
		if "0403:6001" in a[2]:
			cp = a[0]
	if cp ==0:
		errmsg.config(text="Can't find the COM Port for SPCM!", foreground="red")
		return 1 # define errorcode 1 for device open error
	else:
		ser = serial.Serial(cp)
		ser.baudrate = 115200
		ser.timeout = 0.5
		errmsg.config(text="Device Connected", foreground="black")
		return 0
def CheckFinestep (ser):
	askfine = list([3]) # ask finestep
	ser.write(askfine)
	finestep = ord(ser.read())
	return finestep
def LoadCount(ser, delaytime, askdc, sendreset, reset):
	if reset:
		ser.write(sendreset)
	time.sleep(delaytime)
	ser.write(askdc)
	dc =[]
	for i in xrange (0, 3):
		dc.append(ord(ser.read()))
		print str(dc[i])+", " +str(i)

	datacount = (dc[2]<<15)| (dc[1] <<(7)) | (dc[0] >>1)
	return datacount
def LoadData2(ser, askdc, askti, sendreset, idle):
	d4temp0 =0
	d4temp1 =0
	#f0c= open("f0c.tmp", "w")
	#f0f= open("f0f.tmp", "w")
	#f1c= open("f1c.tmp", "w")
	#f1f= open("f1f.tmp", "w")
	f0c= open("f0c.txt", "w")
	f0f= open("f0f.txt", "w")
	f1c= open("f1c.txt", "w")
	f1f= open("f1f.txt", "w")
	ser.write(askdc)
	dc =[]
	for i in xrange (0, 3):
		dc.append(ord(ser.read()))
		print str(dc[i])+", " +str(i)
	datacount = (dc[2]<<15)| (dc[1] <<(7)) | (dc[0] >>1)
	ser.write(askti)
	for i in xrange(0, datacount):
		d1 = ord(ser.read())
		d2 = ord(ser.read())
		d3 = ord(ser.read())
		d4 = ord(ser.read())
		ch = (d4 & 0x40) >>6
		d4 = d4 & 0x3F
		coarse =(d4  << 16) | (d3 << 8) | d2
		if ch == 0:
			f0c.write(str(coarse)+'\n')
		else:
			f1c.write(str(coarse)+'\n')
		
		# if ch == 0:
		# 	if (d4 > d4temp0 ) or ((d4 < d4temp0) and (d4 > 60)):
		# 		#f0c.write(chr(d2)+chr(d3)+chr(d4))
		# 		#f0f.write(chr(d1))
		# 		f0c.write(str(d2)+" "+str(d3)+" "+str(d4)+" ")
		# 		f0f.write(str(d1)+" ")
		# else:
		# 	if (d4 > d4temp1) or ((d4<d4temp1) and (d4 >60)):
		# 		f1c.write(str(d2)+" "+str(d3)+" "+str(d4)+" ")
		# 		f1f.write(str(d1)+" ")
		# 		#f1c.write(chr(d2)+chr(d3)+chr(d4))
		# 		#f1f.write(chr(d1))
	ser.write(idle)
	ser.write(sendreset)
	f0c.close()
	f0f.close()
	f1c.close()
	f1f.close()
def LoadData(ch0coarse, ch0fine, ch1coarse, ch1fine, ser, askdc, askti, sendreset, idle):
	#file3 = open("ch0.txt","w")
	d4temp0 =0
	d4temp1 =0
	ser.write(askdc)
	dc =[]

	for i in xrange (0, 3):
		dc.append(ord(ser.read()))
		print str(dc[i])+", " +str(i)
	datacount = (dc[2]<<15)| (dc[1] <<(7)) | (dc[0] >>1)
	ser.write(askti)

	for i in xrange(0, datacount):
		d1 = ord(ser.read())
		d2 = ord(ser.read())
		d3 = ord(ser.read())
		d4 = ord(ser.read())
		ch = (d4 & 0x40) >>6
		d4 = d4 & 0x3F
		coarse =(d4  << 16) | (d3 << 8) | d2
		
		if ch == 0:
			if (d4 > d4temp0 ) or ((d4 < d4temp0) and (d4 > 60)):
				ch0coarse.append(coarse)
				ch0fine.append(d1)
		else:
			if (d4 > d4temp1) or ((d4<d4temp1) and (d4 >60)):
				ch1coarse.append(coarse)
				ch1fine.append(d1)

	ser.write(idle)
	ser.write(sendreset)
def CoarseHistoAnalysis(coarsearray, time_inteval):
	n1 = len(coarsearray)
	j = 0
	countarray =[0]
	countemp =0
	adderindex = 0
	coarsetemp =0
	for i in xrange (0, n1):
		if coarsearray[i] < coarsetemp :
			adderindex = adderindex +1
		coarsetemp = coarsearray[i]
		coarsearray[i] = coarsearray[i] + 0x400000*adderindex

		if coarsearray[i] < time_inteval*(j+1):
			countemp = countemp +1		
		
		else:
			while coarsearray[i] > time_inteval*(j+1):
				countarray.append(countemp)
				j=j+1
				countemp =0
			countemp =1
		#print "i:"+str(i) + ", j:"+str(j) + ", coarsearray:"+str(coarsearray[i])+", countarray:" +str(countarray[j])+", countemp:" +str(countemp)
		
	return countarray
def CoarseHistoAnalysis2(ch, time_inteval):
	j = 0
	countemp =0
	adderindex = 0
	coarsetemp =0
	countarray =[]
	ftemp = open ("outfile.txt", "w")

	if ch:
		fc = open("f1c.tmp","r")
	else:
		fc = open("f0c.tmp", "r")
	chrinput =fc.read(1)
	while chrinput !='':
		d2 = ord(chrinput)
		chrinput =fc.read(1)
		d3 = ord(chrinput)
		chrinput =fc.read(1)
		d4 = ord(chrinput)
		chrinput = fc.read(1)
		coarse =(d4  << 16) | (d3 << 8) | d2
		ftemp.write(str(d4)+"," +str(coarse)+",")
		print coarse
		if coarse < coarsetemp:
			adderindex = adderindex+1
		coarsetemp = coarse
		coarse = coarse +0x400000*adderindex
		ftemp.write(str(coarse)+"\n")

		if coarse < time_inteval*(j+1):
			countemp = countemp +1		
		else:
			while coarse> time_inteval*(j+1):
				countarray.append(countemp)
				j=j+1
				countemp =0
			countemp =1
		#print "i:"+str(i) + ", j:"+str(j) + ", coarsearray:"+str(coarsearray[i])+", countarray:" +str(countarray[j])+", countemp:" +str(countemp)	
	fc.close()
	ftemp.close()
	return countarray

def PhotonCountHistogram(countarray):
	n1 = len(countarray)
	countmax = max(countarray)
	if countmax < 4:
		countmax =4
	histo_out = [0 for i in range(countmax+1)]
	for i in xrange(0, n1):
		histo_out[countarray[i]] = histo_out[countarray[i]]+1
	return histo_out
def PlotCalculation(yarray, xarray, ycordmax, xcordmax, xoffset, yout, xout, ylabel, xlabel):
	n1 = len(yarray)
	ymax = max(yarray)
	xmax = max(xarray)
	ymin = 0
	xmin = 0
	dyl = int((ymax-ymin)/4)+1
	dxl = int((xmax-xmin)/4)+1


	for i in xrange (0,5):
		ylabel.append(ymin +dyl*i)
		xlabel.append(xmin +dxl*i)

	dy = float(ycordmax)/(ylabel[4]-ymin)
	dx = float(xcordmax)/(xlabel[4]-xmin)
	xout.append(xoffset)
	for i in xrange (0, n1):
		y = ycordmax-(yarray[i]-ymin)*dy
		x = (xarray[i]-xmin+1)*dx + xoffset
		yout.append(y)
		xout.append(x)










