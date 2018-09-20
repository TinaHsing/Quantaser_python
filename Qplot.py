from Tkinter import *
import math

master = Tk()
master.title("Quantaser Plot")
canvas_width = 600
canvas_height = 600
divx = canvas_width/10
divy =  canvas_height/10
plot = Canvas(master, width= canvas_width, height = canvas_height, bg ="white")


#### create grid ######
for x in xrange(0,9):
	plot.create_line(0, (x+1)*divy, canvas_width, (x+1)*divy, fill ="gray", width =1)
	plot.create_line((x+1)*divx, 0, (x+1)*divx, canvas_height,fill ="gray", width =1)

# create triangle wave
plot.create_line(0, 475, 100, 550, 300, 400, 500, 550, 600, 475, fill = "red", width = 3)




plot.pack()
master.mainloop()