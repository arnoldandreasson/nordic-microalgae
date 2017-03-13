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
  
def execute(db_host = 'localhost', 
            db_name = 'nordicmicroalgae', 
            db_user = 'root', 
            db_passwd = '',
            delete_db_content = False,
            file_name = '../data_import/media.txt', 
            file_encoding = 'utf16',
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
        # Remove all rows in tables.
        if delete_db_content == True:
            cursor.execute(""" delete from taxa_media """) 
            cursor.execute(""" delete from taxa_media_list """) 
        # Open file for reading.
        infile = codecs.open(file_name, mode = 'r', encoding = file_encoding)    
        # Iterate over rows in file.
        for rowindex, row in enumerate(infile):
            if rowindex == 0: # First row is assumed to be the header row.
                # Header: 'Scientific name', 'Media id', 'Media type', 'User name', 'Sort order', 
                #         'Location', 'Latitude DD', 'Longitude DD', 'Media format', 'Date', 
                #         'Dateadded', 'Title', 'Description', 'Creator', 'Publisher', 'Contributor', 'Rights'
                header = list(map(str.strip, row.split(field_separator)))
                # header = list(map(unicode, header))
                pass
            else:
                row = list(map(str.strip, row.split(field_separator)))
                # row = list(map(unicode, row))
                #
                scientificname = row[0] # Scientific name
                mediaid = row[1] # Media id
                mediatype = row[2] # Media type
                username = row[3] # 'User name
                # Create metadata.
                metadata = {}
                for columnindex, headeritem in enumerate(header):
#                    if not (headeritem in ['Scientific name', 'Media id', 'Media type', 'User name', 'Sort order']):
                    if not (headeritem in ['Scientific name', 'Media id', 'Sort order']):
                        if row[columnindex]:
                            metadata[headeritem] = row[columnindex]
                # Convert facts to string.
                jsonstring = json.dumps(metadata, # encoding = 'utf-8', 
                                        sort_keys=True, indent=4)
                
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

                # Check if db row exists. 
                cursor.execute("select count(*) from taxa_media where taxon_id = %s and media_id = %s and media_type = %s", 
                               (taxon_id, row[1], row[2]))
                result = cursor.fetchone()
                if result[0] == 0: 
                    cursor.execute("insert into taxa_media(taxon_id, media_id, media_type, user_name, metadata_json) values (%s, %s, %s, %s, %s)", 
                                   (str(taxon_id), mediaid, mediatype, username, jsonstring))
                else:
                    cursor.execute("update taxa_media set metadata_json = %s where taxon_id = %s and media_id = %s and media_type = %s"
                                   (jsonstring, str(taxon_id), mediaid, mediatype))
        #
        # Put media in media list
        # Restart infile.
        infile.seek(0)
        # 
        taxondict = {} # Key: taxonid, value: name-list.
        #
        for rowindex, row in enumerate(infile):
            if rowindex == 0: # First row is assumed to be the header row.
                # Header: 'Scientific name', 'Media id', 'Media type', 'User name', 'Sort order', 
                #         'Location', 'Latitude DD', 'Longitude DD', 'Media format', 'Media type', 'Date', 
                #         'Dateadded', 'Title', 'Description', 'Creator', 'Publisher', 'Contributor', 'Rights'
                header = list(map(str.strip, row.split(field_separator)))
                # header = list(map(unicode, header))
                pass
            else:
                row = list(map(str.strip, row.split(field_separator)))
                # row = list(map(unicode, row))
                #
                scientificname = row[0] # Scientific name
                mediaid = row[1] # Media id
                sortorder = row[4] # Media type
                # Get taxon_id from name.
                cursor.execute("select id from taxa " + 
                                 "where name = %s", 
                                 (scientificname,) )
                result = cursor.fetchone()
                taxonid = None
                if result:
                    taxonid = result[0]
                else:
                    print("Warning: Can't find taxon i taxa. Name: " + scientificname)
                    continue # Skip this taxon.
                # 
                if taxonid in taxondict:
                    if sortorder == '0':
                        taxondict[taxonid] = [mediaid] + taxondict[taxonid] # Add at beginning.
                    else:
                        taxondict[taxonid].append(mediaid) # Append at end.
                else:
                    taxondict[taxonid] = [mediaid] # This was the first one.
        #
        for taxonid in taxondict:
            cursor.execute("insert into taxa_media_list(taxon_id, media_list) values (%s, %s)", 
               (str(taxonid), ';'.join(taxondict[taxonid])))
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


# Main.
if __name__ == '__main__':
    execute()

