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
import connect_to_db
import sys
import codecs

def execute(file_name = '../data_export/taxa.txt', 
            file_encoding = 'utf16',  
            field_separator = '\t', 
            row_delimiter = '\r\n'): # For windows usage.
    """ Exports taxa table content. Format: Table with tab separated fields. """
    try:
        # Connect to db.
        db = connect_to_db.connect()
        cursor=db.cursor()
        cursortaxa=db.cursor()
        # Open file and write header.
        out = codecs.open(file_name, mode = 'w', encoding = file_encoding)
        # Header.
        outheader = ['Scientific name', 'Author', 'Rank', 'Parent name']
        # Print header row.
        out.write(field_separator.join(outheader) + row_delimiter)
        # Iterate over taxa. 
        cursortaxa.execute("select name, author, rank, parent_id from taxa order by name")
        for name, author, rank, parent_id in cursortaxa.fetchall():
            # Get parent name.
            parent_name = ''
            cursor.execute("select name from taxa where id = %s", parent_id)
            result = cursor.fetchone()
            if result:
                # From string to dictionary.
                parent_name = result[0]
            # Create row.
            row = [name, author, rank, parent_name]
            # Print row.
            out.write(field_separator.join(row) + row_delimiter)                
    except (IOError, OSError):
        print("ERROR: Can't write to text file." + file_name)
        print ("ERROR: Script will be terminated.")
        sys.exit(1)
    except mysql.Error, e:
        print ("ERROR: MySQL %d: %s" % (e.args[0], e.args[1]))
        print ("ERROR: Script will be terminated.")
        sys.exit(1)
    finally:
        if out: out.close()
        if cursor: cursor.close()
        if db: db.close()


# Main.
if __name__ == '__main__':
    execute()
