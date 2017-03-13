#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Nordicmicroalgae. http://nordicmicroalgae.org/
# Copyright (c) 2011-2017 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import mysql.connector
import sys
# import string
import codecs

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
            db_passwd = '',
            delete_db_content = False
            ):
    """ Imports data for links to external sources. """
    infile = None
    try:
        # Connect to db.
        db = mysql.connector.connect(host = db_host, db = db_name, 
                           user = db_user, passwd = db_passwd,
                           use_unicode = True, charset = 'utf8')
        cursor=db.cursor()
        # Remove all rows in table.
        if delete_db_content == True:
            cursor.execute(""" delete from taxa_external_links """) 
        # Open file for reading.
        infile = codecs.open(file_name, mode = 'r', encoding = file_encoding)    
        # Iterate over rows in file.
        for rowindex, row in enumerate(infile):
            if rowindex == 0: # First row is assumed to be the header row.
                # 'Scientific name', 'Synonym name', 'Synonym author', 'Info json'
                headers = list(map(str.strip, row.split(field_separator)))
                # headers = list(map(unicode, headers))
            else:
                row = list(map(str.strip, row.split(field_separator)))
                # row = list(map(unicode, row))
                # Get taxon_id from name.
                cursor.execute("select id from taxa " + 
                                 "where name = %s", (row[0],) )
                result = cursor.fetchone()
                if result:
                    taxon_id = result[0]
                else:
                    print("Warning: Can't find taxon i taxa. Name: " + row[0])
                    continue # Skip this taxon.
                
                # Insert row.
                externalid = row[1]
                value = url_template.replace('<replace-id>', externalid)
                try:
                    cursor.execute("insert into taxa_external_links(taxon_id, provider, type, value) values (%s, %s, %s, %s)", 
                                    (str(taxon_id), provider, link_type, value))
                except mysql.connector.Error as e:
                    print("WARNING (taxa_external_links): MySQL %d: %s" % (e.args[0], e.args[1]))
    #
    except (IOError, OSError):
        print("ERROR: Can't read text file." + file_name)
        print("ERROR: Script will be terminated.")
        sys.exit(1)
    except mysql.connector.Error as e:
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

