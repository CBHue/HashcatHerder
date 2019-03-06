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
import sqlite3
from datetime import datetime 
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

def printR(out): print("\033[91m{}\033[00m" .format("[!] " + out)) 
def printP(out): print("\033[95m{}\033[00m" .format("[*] " + out)) 

def db_init(DBFILE):
	conn = sqlite3.connect(DBFILE)
	c = conn.cursor()
	c.execute( '''CREATE TABLE IF NOT EXISTS "hashes" (
		"hash" text PRIMARY KEY,
		"password" text
	)''') 

	# Test the connection
	db_connect(DBFILE)

def db_connect(DBFILE):
	try:
		# set the database connectiont to autocommit w/ isolation level
		conn = sqlite3.connect(DBFILE, check_same_thread=False)
		conn.text_factory = str
		conn.isolation_level = None
		return conn

	except Exception:
		printR("Could not connect to database")
		raise SystemExit

def db_close(conn):
	conn.close()

def db_search(c, hash):
	hash = hash.strip()
	cursor = c.cursor()
	query = "SELECT password FROM hashes WHERE hash = '%s'" % hash
	cursor.execute(query)
	r = cursor.fetchall()
	cursor.close()
	if r:
		return r
	else:
		return hash

def db_getHashCount(conn):
	printP("Checking DB for Hash count")
	conn.execute('pragma journal_mode=wal')
	c = conn.cursor()
	c.execute('SELECT count(*) from hashes') 
	r = c.fetchall()
	c.close()
	count = ', ,'.join([str(i[0]) for i in r])
	printP("Hash Count  : " + locale.format("%d", int(count), grouping=True))

def db_checkFile(c, hashFile, workingFile, LogFile):
	if hashFile:
		printP("Checking if Hashes are in DB")
		with open(workingFile, mode = 'a', encoding='utf-8') as wFile:
			with open(LogFile, mode = 'a', encoding='utf-8') as oFile:
				oFile.write("Hashes in DB\n")
				oFile.write("***************************************************\n")
				with open(hashFile, "r",encoding='utf-8', errors='ignore') as HashReader:
					for hash in HashReader:
						hash = hash.strip()
						r = db_search(c, hash)
						# Hash not in DB
						if type(r) is str:
							wFile.write(hash + "\n")
						# Hash is already cracked
						else:
							password = hash + ":" + ', ,'.join([str(i[0]) for i in r]) + "\n"
							oFile.write(str(password))
						wFile.flush()
						oFile.flush()
		wFile.close()
		oFile.close()
	else:
		printR("Issues with the hashFile ...")		

def db_readFile(conn, fileName):
	if fileName:
		printP("Adding potFile to DB: " + fileName)
		try:
			c = conn.cursor()
			c.execute("BEGIN")
			with open(fileName, "r",encoding='utf-8', errors='ignore') as HashReader:
				for row in HashReader:
					sL,sR=row.split(':', 1)
					c.execute("INSERT OR IGNORE INTO hashes VALUES (?,?)", [sL.strip(),sR.strip()])
			conn.commit()

		except IOError:
			printR("Could not read file:"), fileName
	else:
		printR("Issues with " + fileName + " ...")

def db_configure(dataDIR):
	try: 
	    os.makedirs(dataDIR)
	except OSError:
	    if not os.path.isdir(dataDIR):
	        raise

def start():
	t = datetime.now()
	printP("Starting Time " + str(t))
	return t

def endT(t):
	tE = datetime.now() - t 
	printP('Elapsed Time (hh:mm:ss.ms) {}'.format(tE))
