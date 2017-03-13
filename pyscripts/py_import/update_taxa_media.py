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
import json
  
def execute(db_host, db_name, db_user, db_passwd, file_name, 
#            file_encoding = 'utf16',
#            file_encoding = 'utf8',
            file_encoding = 'cp1252',
            field_separator = '\t', 
            row_delimiter = '\r\n'):
    """ Imports content to the main taxa table. """
    db = None
    cursor = None
    try:
        # Connect to db.
        db = mysql.connector.connect(host = db_host, db = db_name, 
                           user = db_user, passwd = db_passwd,
                           use_unicode = True, charset = 'utf8')
        cursor = db.cursor()

        # Read header list from system settings (Facts: Headers).
        fieldtypes = {}
        cursor.execute("select settings_value from system_settings where settings_key = 'Media'")
        result = cursor.fetchone()
        if result:
            # From string to dictionary.
            factssettingsdict = json.loads(result[0], encoding = 'utf-8')
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
        
        
        # Open file for reading.
        infile = codecs.open(file_name, mode = 'r', encoding = file_encoding)    
        # Iterate over rows in file.
        for rowindex, row in enumerate(infile):
            if rowindex == 0: # First row is assumed to be the header row.
                headers = list(map(cleanup_string, row.split(field_separator)))
#                headers = list(map(str.strip, row.split(field_separator)))
#                headers = list(map(unicode, headers))
            else:
                row = list(map(cleanup_string, row.split(field_separator)))
#                row = list(map(str.strip, row.split(field_separator)))
#                # row = list(map(unicode, row))
                #
                if len(row) < 3:
                    continue
                
                scientificname = row[0] # Scientific name
                mediaid = row[1] # Media id
#                mediatype = row[2] # Media type
#                username = row[3] # 'User name
                # Get taxon_id from name.
                cursor.execute("select id from taxa " + 
                                 "where name = %s", 
                                 (scientificname,) )
                result = cursor.fetchone()
                if result:
                    taxon_id = result[0]
                else:
                    print("Warning: Can't find taxon in taxa. Name: " + scientificname)
                    continue # Skip this taxon.




                # Get metadata from db.
                cursor.execute("select metadata_json from taxa_media where taxon_id = %s and media_id = %s", 
                               (taxon_id, mediaid))
                result = cursor.fetchone()
                if result:
                    # From string to dictionary.
                    metadatadict = json.loads(result[0], encoding = 'utf-8')
                    # Add column values to row, if available.
                    for headeritem in headers:
                        row.append(metadatadict.get(headeritem, ''))
                else:
                    # Add empty columns.
                    metadatadict = {}
                # Update facts.
                for colindex, headeritem in enumerate(headers):
                    if not headeritem in ['Taxon name', 'Scientific name', 'Media id']:
                        if row[colindex] == 'NULL':
                            # Remove items marked as NULL.
                            if headeritem in metadatadict:
                                del metadatadict[headeritem]
                        elif len(row[colindex]) > 0:
                            # Only change value if row item contains text.
                            if (headeritem in fieldtypes) and (fieldtypes[headeritem] == 'text list'):
                                #
                                """ """ 
                                textlist = []
                                for text in row[colindex].split(';'):
                                    textlist.append(text)
                                metadatadict[headeritem] = textlist
                            else:
                                metadatadict[headeritem] = row[colindex]
                
                # Convert metadata to string.
                jsonstring = json.dumps(metadatadict, # encoding = 'utf-8', 
                                        sort_keys=True, indent=4)
                # Update metadata. 
                cursor.execute("update taxa_media set metadata_json = %s where taxon_id = %s and media_id = %s", 
                               (jsonstring, str(taxon_id), mediaid))
        #
        infile.close()
    #
    except mysql.connector.Error as e:
        print("ERROR: MySQL %d: %s" % (e.args[0], e.args[1]))
        print("ERROR: Script will be terminated.")
        sys.exit(1)
    finally:
        if db: db.close()
        if cursor: cursor.close()

def cleanup_string(value):
    """ 
    Removes white characters at beginning and end of string. Convert to unicode.
    Citation characters eventually added by Excel are also removed. 
    """
    return str(value.strip().strip('"'))
    

if __name__ == "__main__":
    execute()

