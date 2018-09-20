import serial
import serial.tools.list_ports
import time
def loadcount():
	askdc = list([1]) # ask datacount
	sendreset = list([4]) # send reset to spcm
	portlist = serial.tools.list_ports.comports()
	cp =0

	for a in portlist:
		if "0403:6001" in a[2]:
			cp = a[0]
	if cp ==0:
		return -1 # define errorcode =-1 for device open error

	else:
		ser = serial.Serial(cp)
		ser.baudrate = 115200
		ser.timeout = 0.5
	ser.write(sendreset)
	time.sleep(0.5)
	ser.write(askdc)
	dc =[]
	for i in xrange (0, 3):
		dc.append(ord(ser.read()))
	datacount = (dc[2]<<15)| (dc[1] <<(7)) | (dc[0] >>1)

	return datacount





def loaddata(ch0coarse, ch0fine, ch1coarse, ch1fine, finestep):
	askdc = list([1]) # ask datacount
	askti = list([2]) # ask time 
	askstep = list([3]) # ask finestep
	sendreset = list([4]) # send reset to spcm
	
	portlist = serial.tools.list_ports.comports()
	cp =0
	
	
	data =[]
	for a in portlist:
		if "0403:6001" in a[2]:
			cp = a[0]
	if cp ==0:
		return 1 # define errorcode =1 for device open error

	else:
		ser = serial.Serial(cp)
		ser.baudrate = 115200
		ser.timeout = 0.5
	ser.write(askdc)

	for i in xrange (0, 3):
		dc.append(ord(ser.read()))
	datacount = (dc[2]<<15)| (dc[1] <<(7)) | (dc[0] >>1)

	finestep = 0.04
	ser.write(askti)

	for i in xrange(0, datacount):
		d1 = ord(ser.read())
		d2 = ord(ser.read())
		d3 = ord(ser.read())
		d4 = ord(ser.read())
		ch = (d4 & 0x40) >>6
		coarse =((d4 & 0x3F) << 16) | (d3 << 8) | d

		if ch == 0:
			ch0coarse.append(coarse)
			ch0fine.append(d1)
		else:
			ch1coarse.append(coarse)
			ch1fine.append(d1)
	return 0

def loadtest(ch0coarse, ch0fine, ch1coarse, ch1fine, finestep):
	ch0c =[350, 1234, 6572, 23456, 74484, 390655, 1396508, 2345, 7662, 32768, 4521, 95134 ]
	ch0f = [14, 35, 77, 92, 45, 36, 4, 254, 73, 12, 99, 76, 87]
	ch1c =[768, 1235, 6672, 23467, 72345, 199065, 239133, 3987654, 2345, 7662, 76672, 99989, 234797]
	ch1f = [34, 133, 68, 75, 34, 25, 5, 234, 44, 65, 75, 87, 91]
	for i in xrange (0, len(ch0c)):
		ch0coarse.append(ch0c[i])
		ch0fine.append(ch0f[i])

	for i in xrange(0, len(ch1c)):
		ch1coarse.append(ch1c[i])
		ch1fine.append(ch1f[i])
	finestep = 0.04





def CalculateTime(timearray, coarsearray, finearray, finestep):
	n1 = len(coarsearray)
	n2 = len(finearray)
	resetindex =0
	coarsetemp =0
	coarsestep =10
	if n1 !=n2:
		return 2
	
	for i in xrange (0, n1):
		if coarsearray[i] < coarsetemp:
			resetindex = resetindex+0x400000
		
		coarse = coarsearray[i] +resetindex
		time = coarse* coarsestep +  finearray[i]*finestep
		timearray.append(time)
		coarsetemp = coarsearray[i]
	return 0





def Histogram(analysisarray, binarray): #this will return countarray
	n1 = len(analysisarray)
	j =0
	countarray =[]
	countemp =0
	for i in xrange (0, n1):
		if analysisarray[i] < binarray [j]:
			countemp = countemp +1
		else:
			countarray[j] = countemp
			j = j+1
			countemp =0
	return countarray

#def PlotHisto(corrdarray, xcorrd, ycorrd, xpixel, ypixel, xarray, yarray):










