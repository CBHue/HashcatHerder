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

DIR_CONFIG = {

	# Hashcat Binary location
	#'hashcat' : '/opt/hashcat-5.0.0/hashcat64.bin',
	'hashcat' : '/opt/hashcat-5.1.0/hashcat64.bin',
	#'hashcat' : '/opt/hashcat/hashcat',

	# John script location
	'john' : '/opt/JohnTheRipper/run/john',

	# Script Working Directories
	'workingDir' : '/opt/hashERLoopER/working/log/', 
	'dataDIR'	 : '/opt/hashERLoopER/working/db/',
	'DBFILE'	 : '/opt/hashERLoopER/working/db/hashMaster.db',

	# Wordlist Directories
	'MainDir'	 	: '/mnt/NoName/PList/',
	'pListDir'	 	: '/mnt/NoName/PList/wordlist/',
	'potDir'	 	: '/mnt/NoName/PList/potfile/',
	'rDir'	 	 	: '/mnt/NoName/PList/rules/',
	'RuleOnlyDir'	: '/mnt/NoName/PList/rules/ALL/'

}
