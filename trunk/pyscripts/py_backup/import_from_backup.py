#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Project: Nordic Microalgae. http://nordicmicroalgae.org/
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2011 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License as follows:
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import MySQLdb as mysql
import sys
import codecs
import string
import connect_to_db

def execute(file_name = '../data_backup/taxa_facts_backup.txt', 
            file_encoding = 'utf16',
            field_separator = '\t', 
            row_delimiter = '\r\n'): # For windows usage.
    """ 
    Imports data to database from backup file. 
    Use this import after a database rebuild. Taxa must be loaded before.
    """
    try:
        # Connect to db.
        db = connect_to_db.connect()
        cursor=db.cursor()
        # Remove all rows in table.
        cursor.execute(""" delete from taxa_facts """) 
        # Create dictionary for translations from taxon_name to taxon_id.
        taxonnametoid = {}
        cursor.execute("select id, name from taxa")
        for taxon_id, taxon_name in cursor.fetchall():
            taxonnametoid[taxon_name] = taxon_id
        # Open file for reading.
        infile = codecs.open(file_name, mode = 'r', encoding = file_encoding)    
        # Iterate over rows in file.
        for rowindex, row in enumerate(infile):
            if rowindex == 0: # First row is assumed to be the header row.
                headers = map(string.strip, row.split(field_separator))
                headers = map(unicode, headers)
            else:
                row = map(string.strip, row.split(field_separator))
                row = map(unicode, row)
                if row[0] in taxonnametoid:
                    taxon_id = taxonnametoid[row[0]]
                    facts_json = row[1]
                    cursor.execute("insert into taxa_facts(taxon_id, facts_json) values (%s, %s)", 
                                   (taxon_id, facts_json))
                else:
                    print("Can't find taxon name in table taxa. Name: " + row[0])
    #
    except (IOError, OSError):
        print("ERROR: Can't read text file." + infile)
        print("ERROR: Script will be terminated.")
        sys.exit(1)
    except mysql.Error, e:
        print("ERROR: MySQL %d: %s" % (e.args[0], e.args[1]))
        print("ERROR: Script will be terminated.")
        sys.exit(1)
    finally:
        if infile: infile.close() 
        if cursor: cursor.close()
        if db: db.close()


# Main.
if __name__ == '__main__':
    execute()
