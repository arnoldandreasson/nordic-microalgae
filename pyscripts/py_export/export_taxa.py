#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Nordicmicroalgae. http://nordicmicroalgae.org/
# Copyright (c) 2011-2017 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import mysql.connector
import sys
import codecs

def execute(db_host = 'localhost', 
            db_name = 'nordicmicroalgae', 
            db_user = 'root', 
            db_passwd = '',
            file_name = '../data_download/taxa.txt', 
            file_encoding = 'utf16',  
            field_separator = '\t', 
            row_delimiter = '\r\n'): # For windows usage.
    """ Exports taxa table content. Format: Table with tab separated fields. """
    db = None
    cursor = None
    out = None
    try:
        # Connect to db.
        db = mysql.connector.connect(host = db_host, db = db_name, 
                           user = db_user, passwd = db_passwd,
                           use_unicode = True, charset = 'utf8')
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
            cursor.execute("select name from taxa where id = %s", 
                           (parent_id,) )
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
        print("ERROR: Script will be terminated.")
        sys.exit(1)
    except mysql.connector.Error as e:
        print("ERROR: MySQL %d: %s" % (e.args[0], e.args[1]))
        print("ERROR: Script will be terminated.")
        sys.exit(1)
    finally:
        if db: db.close()
        if cursor: cursor.close()
        if out: out.close()


# Main.
if __name__ == '__main__':
    execute()
