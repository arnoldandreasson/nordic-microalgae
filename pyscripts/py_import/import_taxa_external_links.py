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
import string
import codecs
import connect_to_db

def execute(provider = "AlgaeBase",
            link_type = "Taxon URL",
            url_template = "http://algaebase.org/search/species/detail/?species_id=<replace-id>",
            file_name = '../data_import/external_links_algaebase.txt', 
            file_encoding = 'utf16',
            field_separator = '\t', 
            row_delimiter = '\r\n', # For windows usage.
            db_host = 'localhost', 
            db_name = 'nordicmicroalgae', 
            db_user = 'root', 
            db_passwd = ''
            ):
    """ Imports data for links to external sources. """
    infile = None
    try:
        # Connect to db.
        db = connect_to_db.connect(db_host, db_name, db_user, db_passwd)
        cursor=db.cursor()
        # Open file for reading.
        infile = codecs.open(file_name, mode = 'r', encoding = file_encoding)    
        # Iterate over rows in file.
        for rowindex, row in enumerate(infile):
            if rowindex == 0: # First row is assumed to be the header row.
                # 'Scientific name', 'Synonym name', 'Synonym author', 'Info json'
                headers = map(string.strip, row.split(field_separator))
                headers = map(unicode, headers)
            else:
                row = map(string.strip, row.split(field_separator))
                row = map(unicode, row)
                # Get taxon_id from name.
                cursor.execute("select id from taxa " + 
                                 "where name = %s", (row[0]))
                result = cursor.fetchone()
                if result:
                    taxon_id = result[0]
                else:
                    print("Error: Can't find taxon i taxa. Name: " + row[0])
                    continue # Skip this taxon.
                
                # Insert row.
                externalid = row[1]
                value = url_template.replace('<replace-id>', externalid)
                try:
                    cursor.execute("insert into taxa_external_links(taxon_id, provider, type, value) values (%s, %s, %s, %s)", 
                                    (unicode(taxon_id), provider, link_type, value))
                except mysql.Error, e:
                    print("WARNING (taxa_external_links): MySQL %d: %s" % (e.args[0], e.args[1]))
    #
    except (IOError, OSError):
        print("ERROR: Can't read text file." + file_name)
        print("ERROR: Script will be terminated.")
        sys.exit(1)
    except mysql.Error, e:
        print("ERROR: MySQL %d: %s" % (e.args[0], e.args[1]))
        print("ERROR: Script will be terminated.")
        sys.exit(1)
    finally:
        if db: db.close()
        if cursor: cursor.close()
        if infile: infile.close() 


# Main.
if __name__ == '__main__':
    execute()

