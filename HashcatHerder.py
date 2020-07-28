#!/usr/bin/env python3

'''
 
 	HashcatHerder

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''

import os
import sys
import time
import shlex
import locale
import subprocess
from argparse import ArgumentParser
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# Custom Modules
import util.dbWork as dbWork
import util.config as config
import util.banner as banner
from util.helper import *
import util.loggER as logOUT

# Configurations #
hashcat 	= config.DIR_CONFIG['hashcat']
john 		= config.DIR_CONFIG['john']
workingDir	= config.DIR_CONFIG['workingDir'] 
MainDir		= config.DIR_CONFIG['MainDir']
wordlistDir	= config.DIR_CONFIG['wordlistDir']
potDir		= config.DIR_CONFIG['potDir']
rulesDir 	= config.DIR_CONFIG['rulesDir']
hcMaskDir 	= config.DIR_CONFIG['hcMaskDir']
hybridDir 	= config.DIR_CONFIG['hybridDir']
RuleOnlyDir	= config.DIR_CONFIG['RuleOnlyDir']
dataDIR 	= config.DIR_CONFIG['dataDIR']
DBFILE 		= config.DIR_CONFIG['DBFILE']

def muxER(command):
	result =[]
	result = subprocess.Popen(command, shell=True,stdout=subprocess.PIPE).communicate()[0].decode('utf-8').strip()
	return result

def realTimeMuxER(command):
	p = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
	while True:
		output = p.stdout.readline().decode()
		if output == '' and p.poll() is not None:
			break
		if output:
			print(output.strip())
	rc = p.poll()


def john():
	cmd = "sudo" + john + " " + hFile + " --wordlist=" + pFile
	cmd = "sudo /opt/JohnTheRipper/run/john ./SunMD5_unshadowed.txt --wordlist=/mnt/NoName/PList/10k-most-common.txt"

def hashCAT(hType, hFile, wordList, option):
	'''
	hType 		: Hash Type
	hFile 		: Hash File
	wordList 	: wordList 
	option 		: "Rules, Rules+, Mask, WordList"

	'''
	iSize = curentLines(hFile)
	if "Rules" in option:
		# Rules+ loops over multiple smaller rule files. 
		if option == "Rules+":
			Dir = RuleOnlyDir
		else:
			# Rules only will run a super one rule that may take a while due to the size. But will not duplicate checks
			Dir = rulesDir
		cmd = "ls " + "-Sr " + Dir + " | grep \".rule\""
		result = muxER(cmd)
		rList = result.split('\n')
		totalRules = len(rList)
		counter = 1
		for r in rList:
			rules = Dir + r
			logOUT.screen("[~] Rule File", "yellow", '%s %s out of %s' % (r, counter, totalRules), "cyan")
			logOUT.screen("[~] Wordlist", "yellow", wordList, "cyan")
			print('')
			cmd = "%s --rules %s --potfile-path %s -o %s -a 0 -m %s %s %s" % (hashcat,rules,potFile,oFile,hType,hFile,wordList)
			#print(cmd)
			realTimeMuxER(cmd)
			counter += 1

			# lets check to see if were done
			nSize = curentLines(hFile)
			iSize = crackCheck(iSize, nSize)

			if nSize == "0":
				logOUT.screen("[!] No more work to do", "red")
				fin(iSize)

	if option == "Mask":
		Dir = hcMaskDir
		cmd = "ls " + "-Sr " + Dir + " | grep \".hcmask\""
		result = muxER(cmd)
		fList = result.split('\n')
		total = len(fList)
		counter = 1
		for f in fList:
			file = Dir + f
			logOUT.screen("[~] Mask Right", "yellow", '%s %s out of %s' % (f, counter, total), "cyan")
			logOUT.screen("[~] Wordlist", "yellow", wordList, "cyan")

			cmd = "%s --potfile-path %s -o %s -a 6 -m %s %s %s %s" % (hashcat, potFile, oFile, hType, hFile, wordList, file)
			#print(cmd)
			realTimeMuxER(cmd)

			logOUT.screen("[~] Mask Left", "yellow", '%s %s out of %s' % (f, counter, total), "cyan")
			logOUT.screen("[~] Wordlist", "yellow", wordList, "cyan")
			print('')
			cmd = "%s --potfile-path %s -o %s -a 7 -m %s %s %s %s" % (hashcat, potFile, oFile, hType, hFile, file, wordList)
			#print(cmd)
			realTimeMuxER(cmd)	
			
			counter += 1

			# lets check to see if were done
			nSize = curentLines(hFile)
			iSize = crackCheck(iSize, nSize)

			if nSize == "0":
				logOUT.screen("[!] No more work to do", "red")
				fin(iSize)

	if option == "Hybrid":
		hyb = '?a?a?a?a?a?a?a'

		logOUT.screen("[~] Mask Right", "yellow", hyb, "cyan")
		logOUT.screen("[~] Wordlist", "yellow", wordList, "cyan")
		print('')
		cmd = "%s --potfile-path %s -o %s -a 6 -m %s %s %s %s -i" % (hashcat, potFile, oFile, hType, hFile, wordList, hyb)
		#print(cmd)
		realTimeMuxER(cmd)

		logOUT.screen("[~] Mask Left", "yellow", hyb, "cyan")
		logOUT.screen("[~] Wordlist", "yellow", wordList, "cyan")
		print('')
		cmd = "%s --potfile-path %s -o %s -a 7 -m %s %s %s %s -i" % (hashcat, potFile, oFile, hType, hFile, hyb, wordList)
		#print(cmd)
		realTimeMuxER(cmd)	

	if option == "Brute":
		brute = wordList
		logOUT.screen("[~] Brute", "yellow", brute, "cyan")
		print('')
		cmd = "%s --potfile-path %s -o %s -a 3 -m %s %s %s" % (hashcat, potFile, oFile, hType, hFile, brute)
		#printP(cmd)
		realTimeMuxER(cmd)

	if option == "WordList":
		cmd = "%s --potfile-path %s -o %s -a 0 -m %s %s %s" % (hashcat, potFile, oFile, hType, hFile, wordList)
		#print(cmd)
		realTimeMuxER(cmd)


def loggER(message):
	cmd = "echo \"" + message + "\" >> " + oFile 
	muxER(cmd)

def crackCheck(iSize,nSize):
	global startTime
	dbWork.endT(startTime)
	logOUT.screen("[~] Log File", "yellow", oFile, "cyan")
	logOUT.screen("[~] Starting hash file size", "yellow", locale.format_string("%d", int(iSize), grouping=True), "cyan")
	logOUT.screen("[~] Current hash file size ", "yellow", locale.format_string("%d", int(nSize), grouping=True), "cyan")

	if int(nSize) < int(iSize):
		cracked = int( float(iSize)-float(nSize) )
		logOUT.screen("Cracked " + locale.format_string("%d", int(cracked), grouping=True) + " hash(es) out of " + locale.format_string("%d", int(iSize), grouping=True), "green")
		print('')
		
		loggER(locale.format_string("%d", int(cracked), grouping=True) + " hash(es) cracked out of "+ locale.format_string("%d", int(iSize), grouping=True))
		loggER("")
		return nSize

	else:
		logOUT.screen("[~] Nothing cracked this round ...", "red","\U0001F607")
		print('')
		return iSize

def loopList(Dir,iSize,option,mod=""):
	'''
	Dir 	: String: Directory to get wordlist
	iSize 	: String: initial file size 
	option 	: Type of test - Rules, Rules+, Wordlist, Mask

	The idea here is pull the text files (Wordlists) from the passed in directory
	these txt files are the word lists we will use for this hashcat round
	'''
	cmd = "ls " + "-Sr " + Dir + " | grep \".txt\""

	# You can only check the amount of logs you want ... [tail -5 | head -5]
	if mod:
		cmd = "ls " + "-Sr " + Dir + " | grep \".txt\" | tail -" + str(mod)

	result = muxER(cmd)
	pList = result.split('\n')

	counter = 1
	str_list = list(filter(None, pList))
	totalWordLists = len(str_list)

	for f in pList:
		fext = os.path.splitext(f)[1]
		if fext == '.txt':
			wordList = Dir + f
			
			loggER(wordList)
			loggER("-------------------------------")
			
			logOUT.screen("[~] Attack", "red", option, "cyan")
			logOUT.screen("[~] File", "red", '%s %s out of %s' % (f, counter, totalWordLists), "cyan")

			print('')
			# hash type , Working hash file, working Pot File, Type of test
			hashCAT(hType,wFile,wordList,option)
			counter += 1
		
			# lets check to see if were done
			nSize = curentLines(hFile)
			iSize = crackCheck(iSize, nSize)

			if nSize == "0":
				logOUT.screen("[!] No more work to do", "red")
				fin(iSize)

		else:
			counter += 1
			continue

def curentLines(file):
	# Get starting wc of hFile
	cmd = "wc " + file
	result = muxER(cmd)
	lineCount = result.split(None, 1)[0]
	return lineCount

def checkPot():
	# Check if a pot dir was configured
	if os.path.isdir(potDir):
		logOUT.screen("[-] POT Check", "magenta", potDir, "cyan")
		print('')

		cmd = "ls -Sr " + potDir
		result = muxER(cmd)
		pList = result.split('\n')
		str_list = list(filter(None, pList))
		totalWordLists = len(str_list)
		counter = 0
		hashfile = hFile
		
		for f in pList:	
			potfile = potDir + f
			
			if os.path.isfile(potfile):
				counter += 1
				outFile = wFile + "-" + str(counter)
				cmd = "%s -m %s --potfile-path %s --left %s >> %s" % (hashcat, hType, potfile, hashfile, outFile)

				logOUT.screen(cmd, "magenta")
				realTimeMuxER(cmd)
				# reset hashfile to use output from above command
				hashfile = outFile

		# once were done set the outfile to wFile
		cmd = "mv %s %s" % (outFile, wFile)
		realTimeMuxER(cmd)
		# Then delete the working files
		cmd = "rm %s-*" % wFile
		realTimeMuxER(cmd)

	# if there is not pot directory just check the normal pot file
	else:
		cmd = "%s -m %s --left %s >> %s" % (hashcat, hType, hFile, wFile)
		logOUT.screen(cmd, "magenta")
		realTimeMuxER(cmd)

	# if none of the above worked then just back up the hash file and move on
	if not os.path.isfile(wFile):
		cmd = "cp " + hFile + " " + wFile
		realTimeMuxER(cmd)

def workCheck(c,iSize):
	nSize = curentLines(wFile)
	if int(nSize) == 0:
		# No more work to do
		fin(iSize)
	else:
		logOUT.screen("[+] Work to do?", "yellow"  , "True", "green")

def fin(iSize):

	currentSize = curentLines(wFile)
	loggER("")
	loggER("****************************************************")
	loggER(time.strftime("%m/%d/%Y %H:%M:%S", time.gmtime()) + ": " + locale.format_string("%d", int(currentSize), grouping=True) + " hash(es) not cracked")
	loggER("")

	print('')
	logOUT.screen("[!] Fin", "red")
	logOUT.screen("[+] Starting Hashes Count", "yellow"  , locale.format_string("%d", int(iSize), grouping=True), "green")
	logOUT.screen("[+] Ending Hashes Count", "yellow"  , locale.format_string("%d", int(currentSize), grouping=True), "green")
	logOUT.screen("[+] Remaining Hashes are located in", "yellow"  , wFile, "cyan")
	logOUT.screen("[+] Complete Log File located in", "yellow"  , oFile, "cyan")
	print('')

	# Copy log file to current hash path
	hashDir = os.path.dirname(hFile)
	cmd = "cp " + oFile + " " + hashDir
	realTimeMuxER(cmd)
	
	# add any cracked hashes to the DB
	if os.path.isfile(potFile):
		dbWork.db_readFile(c, potFile)
	
	dbWork.endT(startTime)
	dbWork.db_close(c)

	if args.notify:
		USER = os.getlogin()
		media = os.path.abspath(os.path.dirname(sys.argv[0])) + "/media/"
		if currentSize < iSize:
			# Notify listeners we cracked something
			cmd = "sudo -u " + USER + " vlc --intf dummy --no-loop --play-and-exit " + media + "Yes.mp3 2> /dev/null"
		else:
			# Notify users we failed ...
			cmd = "sudo -u " + USER + " vlc --intf dummy --no-loop --play-and-exit " + media + "No.mp3 2> /dev/null"
		muxER(cmd)

	sys.exit(1)

def brutus():
	logOUT.screen("[+] Brute Lower", "yellow"  , str(lowER), "cyan")
	logOUT.screen("[+] Brute Upper", "yellow"  , str(uppER), "cyan")
	if lowER == '+':
		#we need to incrementing
		charset = '?a' * uppER
		charset = '--increment ' + charset
		hashCAT(hType,wFile,charset,"Brute")
	else:
		for b in range(lowER, uppER + 1):
			charset = '?a' * b


# Main #
def main():

	def notify():
		# Check if VLC is installed
		logOUT.screen("[+] Notify", "yellow"  , "True", "cyan")
		logOUT.screen("[+] Rules" , "yellow"  , rulesDir, "cyan")

	def rules():
		workCheck(c,initialSize)
		logOUT.screen("[+] Rules" , "yellow"  , rulesDir, "cyan")
		loopList(hybridDir, workingSize, "Rules")
		dbWork.endT(startTime)

	def wordlist():
		workCheck(c,initialSize)
		logOUT.screen("[+] Wordlist" , "yellow"  , wordlistDir, "cyan")
		if args.wordlist != 99999:
			loopList(wordlistDir, workingSize, "WordList", args.wordlist)
		else:
			loopList(wordlistDir, workingSize, "WordList")
		dbWork.endT(startTime)
		
	def rulesplus():
		workCheck(c,initialSize)
		logOUT.screen("[+] Rules+" , "yellow"  , RuleOnlyDir, "cyan")
		loopList(RuleOnlyDir, workingSize, "Rules+")
		dbWork.endT(startTime)	

	def mask():
		workCheck(c,initialSize)
		logOUT.screen("[+] Hybrid Mask" , "yellow"  , '?a?a?a?a?a?a?a')
		loopList(hybridDir, workingSize, "Hybrid")
		dbWork.endT(startTime)

	def hybrid():
		workCheck(c,initialSize)
		logOUT.screen("[+] Hybrid Mask" , "yellow"  , hybridDir, "cyan")
		loopList(hybridDir, workingSize, "Mask")
		dbWork.endT(startTime)

	def brute(lowER,uppER):
		logOUT.screen("[+] Brute Lower", "yellow"  , str(lowER), "cyan")
		logOUT.screen("[+] Brute Upper", "yellow"  , str(uppER), "cyan")

		if lowER == '+':
			#we need to incrementing
			charset = '?a' * int(uppER)
			charset = '--increment ' + charset
			hashCAT(hType,wFile,charset,"Brute")
		else:
			uppER = int(uppER)
			lowER = int(lowER)
			for b in range(lowER, uppER + 1):
				charset = '?a' * b
				hashCAT(hType,wFile,charset,"Brute")

	def all():
		logOUT.screen("[+] Running ALL checks","","wordList, Rules, RulesPlus, Mask, Hybrid, Brute[5,9]")
		wordlist()
		rules()
		rulesplus()
		mask()
		hybrid()
		brute(5,9)

	# This is a rough estimate assuming no deletions ...
	dbWork.db_getHashCount(c)

	logOUT.screen("[~] Start File", "yellow"  , hFile, "cyan")
	initialSize = curentLines(hFile)
	logOUT.screen("[~] Start Count", "yellow"  , int(initialSize), "green")
	logOUT.screen("[~] Mode", "yellow"  , hType, "cyan")
	logOUT.screen("[~] Hash File", "yellow"  , wFile, "cyan")
	logOUT.screen("[~] Log File", "yellow"  , oFile, "cyan")
	logOUT.screen("[~] Pot File", "yellow"  , potFile, "cyan")

	# Check the potfile ... Think this is faster than checking a larger pot in everyloop
	#checkPot() 

	# check DB insted of potfile ... 
	dbWork.db_checkFile(c, hFile, wFile, oFile)
	dbWork.endT(startTime)

	workingSize = curentLines(wFile)

	logOUT.screen("[+] New Count", "green"  , str(workingSize), "green")

	loggER("")
	loggER(time.strftime("%m/%d/%Y %H:%M:%S", time.gmtime()) + ": " + locale.format_string("%d", int(workingSize), grouping=True) + " hash(es) to crack")
	loggER("****************************************************")
	loggER("")

	# We are going to process the options as they are pased in ... 
	for arguments in sys.argv:
		check = str(arguments).lower()
		check = check[2:]

		# Skip Notify until the end
		if check == 'notify':
			continue

		# If this is a argument, run function
		if check in vars(args):
			fU = locals()[check]
			if check == 'brute':
				a,b = args.brute.split(',',1)
				fU(a,b)
			else:
				fU()

	# Notify if needed
	if args.notify:
		notify()

	# If we got here we couldnt crack everything and ran out of things to try ....
	logOUT.screen("")
	logOUT.screen("[!] We ran out of work ...", "red"  , "\u001b[31m\u001b[31;1m\U0001F634\033[00m", "cyan")

	fin(initialSize)

if __name__ == "__main__":
	
	if sys.version_info <= (3, 0):
		logOUT.screen("[!] This script requires Python 3.x", "red")
		sys.exit(1)

	banner.banner()
	banner.title()

	# Root Check
	if os.geteuid() != 0:
		logOUT.screen("[!] You need to have root privileges to run this script.", "red")
		logOUT.screen("[!] Please try again, this time using 'sudo'. Exiting.")
		sys.exit(1)

	parser = ArgumentParser()
	# Tool options
	parser.add_argument("--mode",  		 dest="hType",	help="Hashcat Mode", 				metavar="13100")
	parser.add_argument("-f", "--hfile", dest="hFile",										metavar="Hash.FILE")
	parser.add_argument("--addOn",	 	 dest="addOn",	help="Add on Hashcat options", 		metavar="\"--remove -w 4\"")
	parser.add_argument("-p", "--pFile", dest="pFile",	help="Alternate potfile", 			metavar="pot.file")
	parser.add_argument("--dbcheck",	 dest="hash",	help="Check DB for cracked hash", 	metavar="'5f4dcc3b5aa765d61d8327deb882cf99' or './hash.file'", )
	parser.add_argument("--notify","--Notify",			dest="notify",		action="store_true", 	help="Use VLC to notfy were done ...")

	#  - [ Attack Modes ] -
	#  0 | Straight
	#  1 | Combination
	#  3 | Brute-force
	#  6 | Hybrid Wordlist + Mask
	#  7 | Hybrid Mask + Wordlist

	parser.add_argument("--rules","--Rules",			dest="rules",		action="store_true", 	help="One Rule to Rule them all")
	parser.add_argument("--wordlist","--Wordlist",		dest="wordlist", 	default=99999,	action="store", 	nargs='?',	type=int, help="Wordlist Only")
	parser.add_argument("--rulesPlus","--RulesPlus",	dest="rulesplus",	action="store_true", 	help="Extended Rules")
	parser.add_argument("--brute","--Brute", 		 	dest="brute",		help="Ex: 2,3 - Brute Loop '?a?a' [2] to '?a?a?a' [3] Ex: +,3 incrementing '?a' to '?a?a?a' [3]", metavar='[+|any number],[any number]')
	parser.add_argument("--mask","--Mask", 		 		dest="mask",		action="store_true", 	help="Mask Attack ex: '?a?a?a?a?a?a?a'")
	parser.add_argument("--hybrid","--Hybrid",			dest="hybrid",	 	action="store_true", 	help="Hybrid Attack")
	parser.add_argument("--All","--all",				dest="all", 		action="store_true", 	help="All Attacks")

	args = parser.parse_args()

	# Connect to the DB
	c = dbWork.db_connect(DBFILE)

	# if you only want to check for a hash do it now
	if args.hash:

		if os.path.isfile(args.hash):
			hFile = args.hash
			# create a unique identifier date + master
			ts = time.strftime("%m%d%Y_%H_%M_%S", time.gmtime())
			wFile 	= workingDir + os.path.basename(hFile) + "_" + ts
			oFile 	= workingDir + os.path.basename(hFile) + "_" + ts + ".log"
			dbWork.db_checkFile(c, args.hash, wFile, oFile)
			wCount = curentLines(wFile)
			oCount = str(int(curentLines(oFile)) - 2) # header count = 2

			logOUT.screen("[+] Cracked", "green"  , oCount + " " + oFile)
			logOUT.screen("[!] Not Cracked", "red", wCount + " " + wFile)

			exit()

		logOUT.screen("[+] Checking for", "yellow", args.hash )		

		r = dbWork.db_search(c, args.hash)
		if type(r) is str:
			logOUT.screen("[!] Hash not cracked yet", "red")
			# Hash is already cracked
		else:
			password = ', ,'.join([str(i[0]) for i in r]) + "\n"
			logOUT.screen("[!] Hash Cracked", "green", str(password))
		exit()	

	if (args.hFile is None) or (args.hType is None):
		parser.print_help()
		exit()

	if args.hFile is not None:
		if os.path.isfile(args.hFile):
			hFile = args.hFile
		else:
			logOUT.screen("[!] File Not Found", "red", args.hFile)
			exit()
		
		# create a unique identifier date + master
		ts = time.strftime("%m%d%Y_%H_%M_%S", time.gmtime())
		wFile 	= workingDir + os.path.basename(hFile) + "_" + ts
		oFile 	= workingDir + os.path.basename(hFile) + "_" + ts + ".log"
		potFile = workingDir + os.path.basename(hFile) + "_" + ts + ".pot"

	if args.hType is not None:
		hType = args.hType

	if args.pFile is not None:
		pFile = args.pFile
		logOUT.screen(pFile, "yellow")

	if args.brute is not None:
		# we need to get the upper and lower limits
		lowER,uppER = args.brute.split(',',1)

		# Validate the upper limit first ... it should always be a non 0 number
		try:
			uppER = int(uppER)
		except ValueError:
			logOUT.screen("[!] Upper limit must be an int larger than the lower limit", "red")
			exit()

		# Validate the lower limit.
		if lowER == "+":
			# we dont need to verify ... we will increment
			logOUT.screen("[!] increment", "yellow")
		
		else:
			try:
				lowER = int(lowER)
			except ValueError:
				logOUT.screen("[!] Lower limit must be an int lower than the upper limit", "red")
				exit()
			# Now lets check to make sure upper is not lower than lower
			if lowER > uppER:
				logOUT.screen("[!] The lower limit [" + str(lowER) + "] must to be lower than the upper [" + str(uppER) + "] limit", "red")
				exit()

	if args.addOn:
		hashcat += " " + args.addOn + " "

	# Set the Global timekeeper
	startTime = dbWork.start()

	main()
