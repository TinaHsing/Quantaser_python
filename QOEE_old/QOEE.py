from Tkinter import *
from ttk import *
import time
import threading
import spcm




root = Tk() # creat a top-level window
master = Frame(root, name ='master')
master.pack(fill=BOTH)#fill both side of the paraent.

root.title("Quantum Optics Education Experiment")
root.protocol("WM_DELETE_WINDOW", master.quit)

nb = Notebook(master, name='nb') # create Notebook in "master"
nb.pack(fill=BOTH, padx=2, pady=3) 

exp0 = Frame(nb, name ='exp0')
nb.add(exp0, text ="Preparation")
exp1 = Frame(nb, name = 'epx1')
nb.add(exp1, text ="Photon Statics")
exp2 = Frame(nb, name  = 'exp2')
nb.add(exp2, text ="Hanbury Brown_Twiss")

#======start the pannel arrangement of exp0 =======
chname0 = StringVar(exp0)
key_runstop = IntVar(exp0)

def PhotonCount():
	global runindex
	runindex =1
	
	while runindex :
		pc =spcm.loadcount()
		Label0_PhotoCountOut.config(text =str(pc))
		


pc_thread = threading.Thread(target = PhotonCount)

def run_photoncount():
	global pc_thread
	print "thread start"
	pc_thread.start()


def stop_photoncount():
	global runindex
	runindex =0

Label0_PhotoCount = Label(exp0, text ="Photon Count", anchor ="center")
Label0_PhotoCountOut = Label(exp0, text ="0",font = ("Arial", 30), width=25, anchor="e")
#Label0_PhotoCountOut.config(foreground="green")
Label0_PhotoCountOut.config(background="red")
Label0_SelectCh = Label(exp0, text="Select Detector Channel")
ChOption0 = OptionMenu(exp0, chname0, "CH0", "CH0", "CH1")

runbutton0 = Button(exp0, text ="Run", command = run_photoncount)
stopbutton0 = Button(exp0, text ="Stop", command = stop_photoncount)

Label0_PhotoCount.grid(column =0, row =0)
Label0_PhotoCountOut.grid(column =0, row =2)
Label0_SelectCh.grid(column =1, row =0)
ChOption0.grid(column =1, row =1)
runbutton0.grid(column=1, row =2, sticky = W)
stopbutton0.grid(column=1, row=3, sticky = W)






#=======end the pannel arrangement of exp0 ========


#======start the pannel arrangement of exp1 =======

#=======end the pannel arrangement of exp1 ========


#======start the pannel arrangement of exp2 =======

#=======end the pannel arrangement of exp2 ========
master.mainloop()





