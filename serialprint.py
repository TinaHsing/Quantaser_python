import Serial
import datetime
ser = ser = serial.Serial('COM6', 9600, timeout=1)
thefile = open('serialsave4.txt', 'w')
i =0
while True:
    line = ser.readline()
    thefile.write(line)
    print(line)
    i=i+1
    if i == 2000:
        i=0
        text = str(datetime.datetime.now().time())
        thefile.write(text)


