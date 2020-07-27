
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
		print(f'{colored(msg, mColor):35}:  {colored(sts, sColor)}')
	else:
		print(colored(msg, mColor))

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