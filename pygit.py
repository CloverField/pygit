import os
import sys
import subprocess

def checkForConfig():
	return os.path.isfile(os.getcwd()+"/config.txt")

def readFromConfig():
	if checkForConfig():
		for line in open(os.getcwd()+"/config.txt"):
			line2 = line.replace('\n', '')
			changeDirectory(line2)
			git("pull")

	else:
		print("The config file was not found. \nNow creating a new config file.")
		try:
			file = open(os.getcwd()+"/config.txt",'a')
			file.close()
		except:
			print('Unable to create the file. \nPlease check your permissions.')
			sys.exit(0)

def changeDirectory(path):
	return os.chdir(path)

def git(*args):
	return subprocess.check_call(['git'] + list(args))

def main():
	return(readFromConfig())

main()