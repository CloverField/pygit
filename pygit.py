#!/usr/bin/python
import os, sys, subprocess
from colors import bc

def checkForConfig():
	return os.path.isfile(os.path.dirname(os.path.realpath(__file__))+"/config.txt")

def readFromConfig():
	if checkForConfig():
		for line in open(os.path.dirname(os.path.realpath(__file__))+"/config.txt"):
			line2 = line.replace('\n', '')
			changeDirectory(line2)
			git("pull")

	else:
		print("The config file was not found. \nNow creating a new config file.")
		try:
			cfile = open(os.getcwd()+"/config.txt",'a')
			cfile.close()
		except:
			print('Unable to create the file. \nPlease check your permissions.')
			return 1
	return 0

def git(*args):
	return subprocess.check_call(['git'] + list(args))

# write string s to target t (file, stdout, etc)
def p(s,t):
	t.write(s)
	t.flush()
def pout(s):
	p(s,sys.stdout)
def perr(s):
	p(bc.red + s + bc.endc, sys.stderr)

# repo operations
def f_show():
	for r in repos:
		print(bc.green + r + bc.endc)
def f_add():
	global repos
	
	pout('Type the location of the repository to add:\n')
	pout('> ')
	path = os.path.abspath(sys.stdin.readline().strip()) # expand . and ~, etc

	if os.path.isfile(path):
		perr('Error 1. The specified path is a file, not a directory.\n')
		return 1
	elif not os.path.isdir(path):
		perr('Error 2. The specified path does not exist.\n')
		return 2
	cwd = os.getcwd() # record current dir to return to later
	os.chdir(path) # cd to git dir (NOTE: may fail without perms)
	p = subprocess.Popen(['git','status'],
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE).communicate()
	os.chdir(cwd) # return to dir

	if p[1].find('fatal:') == 0: # invalid repo
		perr('Error 3: "%s"\n' % (p[1].strip(),))
		return 3
	else: # valid repo
		if path in repos:
			perr('Error 4. The specified path is already in the repo list.\n')
			return 4
		repos.append(path)
	return 0

def f_del(): pass
def f_pull(): pass
def f_push(): pass

# save 'repos' to config file
def saveconf():
	f = open(confpath, 'w')
	f.write(_magic + '\n')
	for r in repos:
		f.write(r + '\n')
	f.close()

def menu():
	funcs = [f_show, f_add, f_del, f_pull, f_push, saveconf, None]
	try:
		while True:
			pout('GitPyManager v1.0\n')
			pout(' [0] Show repositories\n')
			pout(' [1] Add repository\n')
			#pout(' [2] Remove repository\n')
			#pout(' [3] Pull repositories\n')
			#pout(' [4] Push repositories\n')
			pout(' [5] Save changes\n')
			pout(' [6] Exit\n')
			pout('> ')
		
			ch = sys.stdin.readline()
			if ch == '' or ch.strip() == '6': return # EOI / exit
			try:
				funcs[int(ch)]() # call function ptr
			except: pass # ignore invalid menu choices
	except:
		pass
	finally: # always save when done, or on sigint / exit
		saveconf()
	
_magic = '# gitpymgr. DO NOT MODIFY THIS LINE!'
confpath = os.path.expanduser('~') + '/.gitpymgr.conf'
repos = [0]
def main():
	global repos

	# create config file if it doesnt exist
	if not os.path.isfile(confpath):
		f = open(confpath, 'w')
		f.write(_magic)
		f.close()

	# read and veirfy config file
	repos = open(confpath).readlines()
	for i in range(0,len(repos)): repos[i] = repos[i].strip() # cleanup
	if len(repos) < 1 or repos[0] != _magic:
		perr('%s header is empty or corrupt! Please fix, or move %s to another location.' % (confpath,confpath,))
		return 1

	# remove header
	del repos[0]

	# if no parameters were specified, load interactive CLI
	if len(sys.argv) == 1: menu()

	return 0

if __name__ == '__main__': main()
