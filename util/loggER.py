
from colorama import init, Fore, Back, Style
from termcolor import colored

'''
Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
Style: DIM, NORMAL, BRIGHT, RESET_ALL
'''

init(autoreset=True)
colours = ["BLACK", "RED", "GREEN", "YELLOW", "BLUE", "MAGENTA", "CYAN", "WHITE"];

def screen(msg, mColor="", sts="", sColor=""):

	# Do we have colors?
	if mColor:
		if mColor.upper() in colours:
			mColor = mColor.lower()
	else:
		mColor = "white"

	if sColor:
		if sColor.upper() in colours:
			sColor = sColor.lower()
	else:
		sColor = "white"
		
	# Do we have a status to print?
	if (sts):
		print(f'{colored(msg, mColor):45}:  {colored(sts, sColor)}')
	else:
		print(colored(msg, mColor))

def printB(out): print("\033[90m{}\033[00m" .format("[-] " + out))
def printR(out): print("\033[91m{}\033[00m" .format("[!] " + out)) 
def printG(out): print("\033[92m{}\033[00m" .format("[+] " + out)) 
def printY(out): print("\033[93m{}\033[00m" .format("[~] " + out)) 
def printB(out): print("\033[94m{}\033[00m" .format("[-] " + out))  
def printP(out): print("\033[95m{}\033[00m" .format("[-] " + out))  
def printC(out): print("\033[96m{}\033[00m" .format("[-] " + out))
def printW(out): print("[$] " + out)

def logTXT(out,oF):
	with open(oF, 'a', newline='') as oHandle:
		for x in out:
			oHandle.write('{0:20}: {1}'.format("[*] " + x, out[x]))
			oHandle.write('\n')
		if len(out) > 0:
			oHandle.write("\n\n")
	oHandle.close()

def logCSV(out,oF):
	import csv
	with open(oF, 'a', newline='') as csvF:
		fieldnames = out.keys()
		writer = csv.DictWriter(csvF, fieldnames=fieldnames)
		if os.stat(oF).st_size == 0:
			writer.writeheader()
		writer.writerow(out)
	csvF.close()
