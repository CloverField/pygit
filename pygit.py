import os
import sys

def checkForConfig():
	return os.path.isfile(os.getcwd()+"/config.txt")

def readFromConfig():
	if checkForConfig():
		return("Config file found.")
	else:
		print("The config file was not found. \nNow creating a new config file.")
		try:
			file = open(os.getcwd()+"/config.txt",'a')
			file.close()
		except:
			print('Unable to create the file. \nPlease check your permissions.')
			sys.exit(0)

def main():
	print(readFromConfig())

main()