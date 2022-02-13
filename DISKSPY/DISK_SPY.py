#!/usr/bin/python3
import os, shutil
saving_dir = "SAVED"
interesting_extensions = ["txt", "ldb", "pdf", "odt", "log", "zip"]

if os.path.exists(saving_dir) == False:
	os.mkdir(saving_dir)

def isInteresting(f):
	flag = False
	for e in interesting_extensions:
		if (f.endswith(e)):
			flag = True
				
	return flag



os.system("clear && lsblk")
disco = input("-----------------------\nSelect a mountpoint: ")
if os.path.exists(disco) == False:
	print("Invalid path.")
	exit()
print("Please wait...")
for (root, dirs, files) in os.walk(disco, topdown=True):
	for f in files:
		if isInteresting(f):
			print(f)
			print(root)
			try:
				os.makedirs(saving_dir+root)
			except:
				pass
			try:
				shutil.copyfile(root+"/"+f, saving_dir+root+"/"+f)
			except:
				pass
