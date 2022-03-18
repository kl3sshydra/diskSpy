#!/usr/bin/python3

# diskSpy by kl3sshydra
# https://github.com/kl3sshydra
# version 1.2

import os, shutil, json, datetime, threading
from tkinter import *

# test

# the name of the folder
# that will contain all of the saved data
saving_dir = "SAVED"

# main config variables
version = "1.2"
info = f"""\n\n\n\n
DiskSpy {version} by kl3sshydra
copyright under scemochilegge.inc™
you are not allowed to steal this code
"""
background = "black"
foreground = "red"
checkExtensions = True
checkFilenameContains = True
checkFiletextContains = True

# calculate window dimensions
# based on how many mountpoints it 
# will have to show
mountpoints = os.popen("lsblk").read()
lines_in_mountpoints = mountpoints.count('\n')
width = "700"
height = "455"
height = str((int(height)*lines_in_mountpoints)/8).split(".")[0]
width = str((int(width)*int(height))/455).split(".")[0]
windowsize = width+"x"+height

# load configuration file
configfile = open("config.json", "r")
configlists = json.loads(configfile.readline())
textcontains = configlists['textcontains']
filenamecontains = configlists['filenamecontains']
extensions = configlists['extensions']

# create the saved directory if it doesen't exists
if os.path.exists(saving_dir) == False:
	os.mkdir(saving_dir)


class diskspy:
	# function that determines
	# if a file is interesting or not
	def isInteresting(self, f):
		flag = False

		if (checkExtensions == True):
			for e in extensions:
				if (f.endswith(e)):
					flag = True

		elif (checkFilenameContains == True):
			for e in filenamecontains:
				if (e in f):
					flag = True

		elif (checkFiletextContains == True):
			f2 = open(f, 'rb')
			for e in textcontains:
				for line in f2.readlines():
					if (e in line):
						flag = True
			f2.close()

		return flag

	# thread for the realstart function
	def realstart(self, disco, t):
		if os.path.exists(disco) == False:
			diskspy.writelogs(t,"You selected an invalid mountpoint")
			exit()
		t.insert(END, "Please wait...")
		for (root, dirs, files) in os.walk(disco, topdown=True):
			for f in files:
				if diskspy.isInteresting(f):
					diskspy.writelogs(t,f)
					diskspy.writelogs(t,root)
					try:
						os.makedirs(saving_dir+root)
					except:
						pass
					try:
						shutil.copyfile(root+"/"+f, saving_dir+root+"/"+f)
					except:
						pass

	# function that starts the main process of
	# finding files
	def start(self, disco, t):
		threading.Thread(target=diskspy.realstart, args=(disco, t)).start()

	def writelogs(self, t, text):
		t.insert(END, text+"\n")
		t.see("end")

	def hello(self):
		print("hello")
		

	# main function for our program
	def main(self):
		finestra = Tk()
		finestra.geometry(windowsize)
		finestra.configure(bg=background)
		finestra.title("DiskSpy by kl3sshydra")

		label = Label(finestra, text="SELECT MOUNTPOINT ->   ", bg=background, fg=foreground)
		label.grid(column=0, row=1)

		mountpoint = Text(finestra, height=2, width=40, bg=background, fg=foreground)
		mountpoint.grid(column=1, row=1)

		# empty vertical space
		label = Label(finestra, bg=background, fg=foreground)
		label.grid(column=0, row=2)

		label = Label(finestra, text="MOUNTPOINT LIST:", bg=background, fg=foreground)
		label.grid(column=0, row=3)

		
		label = Label(finestra, text=mountpoints, bg=background, fg=foreground)
		label.grid(column=0, row=4)

		# empty vertical space
		label = Label(finestra, bg=background, fg=foreground)
		label.grid(column=0, row=5)

		label = Label(finestra, text="LOGS", bg=background, fg=foreground)
		label.grid(column=0, row=6)

		t = Text(finestra, width=40,  height=7, bg=background, fg=foreground, wrap = NONE)
		t.grid(column=0, row=7)

		startbutton = Button(finestra, text ="START", bg=background, fg=foreground, activebackground=background, activeforeground=foreground, height=2, width=20, command=lambda: diskspy.start(mountpoint.get("1.0",'end-1c'), t))
		startbutton.grid(column=1, row=3)
		
		label = Label(finestra, text=info, bg=background, fg=foreground)
		label.grid(column=1, row=7)

		diskspy.writelogs(t,"Started at "+str(datetime.datetime.now()))

		finestra.mainloop()

diskspy = diskspy()
diskspy.main()