#!/usr/bin/python3

# diskSpy by kl3sshydra
# https://github.com/kl3sshydra
# version 1.1[beta]

import os, shutil

# the name of the folder
# that will contain all of the saved data
saving_dir = "SAVED"

# main config variables
checkExtensions = False
checkFilenameContains = True
checkFiletextContains = False


# customizable lists

filetextContains_list = [
	"password",
	"product",
	"info",
	"creden",
	"login",
	"email",
	"posta",
]

filenameContains_list = [
	"password",
	"product",
	"info",
	"creden",
	"login",
	"email",
	"posta",
]

possible_extensions = [
	"txt",
	"ppt",
	"pptx",
	"doc",
	"docx",
	#"ldb",
	"pdf",
	"odt", 
	#"log",
	"zip"
	#"html",
	#"htm",
]


# create the saved directory if it doesen't exists
if os.path.exists(saving_dir) == False:
	os.mkdir(saving_dir)

# function that determines
# if a file is interesting or not
def isInteresting(f):
	flag = False

	if (checkExtensions == True):
		for e in possible_extensions:
			if (f.endswith(e)):
				flag = True

	elif (checkFilenameContains == True):
		for e in filenameContains_list:
			if (e in f):
				flag = True

	elif (checkFiletextContains == True):
		f2 = open(f, 'rb')
		for e in filetextContains_list:
			for line in f2.readlines():
				if (e in line):
					flag = True
		f2.close()

	return flag

# main function for our program
def main():
	os.system("clear && lsblk")
	disco = input("-----------------------\nMountpoint: ")
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

main()