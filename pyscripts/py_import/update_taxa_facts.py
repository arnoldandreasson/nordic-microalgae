#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Nordicmicroalgae. http://nordicmicroalgae.org/
# Copyright (c) 2011-2017 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import mysql.connector
import sys
import codecs
# import string
import json

def execute(db_host, db_name, db_user, db_passwd, file_name, 
#            file_encoding = 'utf16',
            file_encoding = 'cp1252',
            field_separator = '\t', 
            row_delimiter = '\r\n'
            ):
    """ Updates facts with changes made to text file. """
    try:
        # Connect to db.
        db = mysql.connector.connect(host = db_host, db = db_name, 
                           user = db_user, passwd = db_passwd,
                           use_unicode = True, charset = 'utf8')
        cursor=db.cursor()
        # Open file for reading.
        infile = codecs.open(file_name, mode = 'r', encoding = file_encoding)    
        # Iterate over rows in file.
        for rowindex, row in enumerate(infile):
            if rowindex == 0: # First row is assumed to be the header row.
                headers = list(map(str.strip, row.split(field_separator)))
                # headers = list(map(unicode, headers))
            else:
                row = list(map(str.strip, row.split(field_separator)))
                # row = list(map(unicode, row))
                # Get taxon_id from name.
                cursor.execute("select id from taxa " + 
                                 "where name = %s", 
                                 (row[0],) )
                result = cursor.fetchone()
                if result:
                    taxon_id = result[0]
                else:
                    print("Warning: Can't find taxon i taxa. Name: " + row[0])
                    continue # Skip this taxon.
                # Get facts_json from db.
                cursor.execute("select facts_json from taxa_facts where taxon_id = %s", taxon_id)
                result = cursor.fetchone()
                if result:
                    # From string to dictionary.
                    factsdict = json.loads(result[0], encoding = 'utf-8')
                    # Add column values to row, if available.
                    for headeritem in headers:
                        row.append(factsdict.get(headeritem, ''))
                else:
                    # Add empty columns.
                    factsdict = {}
                # Update facts.
                for colindex, headeritem in enumerate(headers):
                    if not headeritem in ['Taxon name', 'Rank', 'Classification']:
                        if row[colindex] == 'NULL':
                            # Remove items marked as NULL.
                            del factsdict[headeritem]
                        elif len(row[colindex]) > 0:
                            # Only change value if row item contains text.
                            factsdict[headeritem] = row[colindex]
                # Convert facts to string.
                jsonstring = json.dumps(factsdict, # encoding = 'utf-8', 
                                     sort_keys=True, indent=4)
                # Check if db row exists. 
                cursor.execute("select count(*) from taxa_facts where taxon_id = %s", 
                               (taxon_id,) )
                result = cursor.fetchone()
                if result[0] == 0: 
                    cursor.execute("insert into taxa_facts(taxon_id, facts_json) values (%s, %s)", 
                                   (str(taxon_id), jsonstring))
                else:
                    cursor.execute("update taxa_facts set facts_json = %s where taxon_id = %s", 
                                   (jsonstring, str(taxon_id)))
        #
        infile.close()
    #
    except (IOError, OSError):
        print("ERROR: Can't read text file." + infile)
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


if __name__ == "__main__":
    execute()

