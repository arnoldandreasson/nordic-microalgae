#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Nordicmicroalgae. http://nordicmicroalgae.org/
# Copyright (c) 2011-2017 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import mysql.connector
import sys
import json
import codecs

def execute(db_host = 'localhost', 
            db_name = 'nordicmicroalgae', 
            db_user = 'root', 
            db_passwd = '',
            file_name = '../data_download/taxa_facts.txt', 
            file_encoding = 'utf16',
            field_separator = '\t', 
            row_delimiter = '\r\n'):
    """ Exports facts managed by our own contributors. Format: Table with tab separated fields. """
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
        # Read header list from system settings (Facts: Headers).
        headers = None
        fieldtypes = {}
        cursor.execute("select settings_value from system_settings where settings_key = 'Facts'")
        result = cursor.fetchone()
        if result:
            # From string to dictionary.
            factssettingsdict = json.loads(result[0], encoding = 'utf-8')
            # Read headers.
            headers = factssettingsdict.get('Field list', None)
            if not headers:
                print("ERROR: No headers found. Terminates script.")
                return # Terminate script.
            # Read field types and store in dictionary.
            fieldtypedict = factssettingsdict.get('Field types', None)
            if not fieldtypedict:
                print("ERROR: No field types found. Terminates script.")
                return # Terminate script.
            else:
                for key, value in fieldtypedict.items():
                    fieldtypes[key] = value 
        else:
            print("ERROR: Can't read headers from system_settings. Terminates script.")
            return # Terminate script.
        # Open file and write header.
        out = codecs.open(file_name, mode = 'w', encoding = file_encoding)
        # Header.
        outheader = ['Taxon name', 'Rank', 'Classification']
        outheader.extend(headers)
        # Print header row.
        out.write(field_separator.join(outheader) + row_delimiter)
        # Iterate over taxa. 
        cursortaxa.execute("select id, name from taxa order by name")
        for taxon_id, taxon_name in cursortaxa.fetchall():
            # Create row.
            row = [taxon_name]
            # Add rank and classification string from the taxa_navigation table.
            cursor.execute("select rank, classification from taxa_navigation where taxon_id = %s", 
                           (taxon_id,) )
            result = cursor.fetchone()
            if result:
                row.append(result[0])
                row.append(result[1])
            else:
                row.append('') # Empty if missing.
                row.append('')
            # Get facts_json.
            cursor.execute("select facts_json from taxa_facts where taxon_id = %s", 
                           (taxon_id,) )
            result = cursor.fetchone()
            if result:
                # From string to dictionary.
                factsdict = json.loads(result[0], encoding = 'utf-8')
                # Add column values to row, if available.
                for headeritem in headers:
                    # Check field type and convert to string representation. 
                    if (headeritem in fieldtypes) and (fieldtypes[headeritem] == 'text'):  
                        row.append(factsdict.get(headeritem, ''))
                    elif (headeritem in fieldtypes) and (fieldtypes[headeritem] == 'text list'):  
                        row.append(';'.join(factsdict.get(headeritem, [])))
                    else:
                        print("ERROR: Can't handle field type for: " + headeritem + ". Terminates script.")
                        return # Terminate script.
            else:
                # Add empty columns.
                for headeritem in headers:
                    row.append('')
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
