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
import config
from dbWork import db_init

# Be sure to update your config.py to reflect your desired directory structure
DIRs = ['workingDir', 'dataDIR' , 'MainDir', 'wordlistDir', 'potDir', 'rulesDir', 'hcMaskDir', 'hybridDir', 'RuleOnlyDir']

# Make directory structure needed.
for dirS in DIRs:
    globals()[dirS] = config.DIR_CONFIG[dirS]
    d = (globals()[dirS])
    print ("Making Directory: "+ d)
    os.makedirs(d, exist_ok=True)

# create the DB
DBFILE      = config.DIR_CONFIG['DBFILE']
db_init(DBFILE)

