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
import json
import connect_to_db
  
def execute(db_host = 'localhost', 
            db_name = 'nordicmicroalgae', 
            db_user = 'root', 
            db_passwd = '',
            file_name = '../data_import/taxa_media.txt', 
            file_encoding = 'utf16',
            field_separator = '\t', 
            row_delimiter = '\r\n'):
    """ Imports content to the main taxa table. """
    db = None
    cursor = None
    try:
        # Connect to db.
        db = connect_to_db.connect(db_host, db_name, db_user, db_passwd)
        cursor = db.cursor()
        # Remove all rows in tables.
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
                header = map(string.strip, row.split(field_separator))
                header = map(unicode, header)
                pass
            else:
                row = map(string.strip, row.split(field_separator))
                row = map(unicode, row)
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
                jsonstring = json.dumps(metadata, encoding = 'utf-8', 
                                        sort_keys=True, indent=4)
                
                # Get taxon_id from name.
                cursor.execute("select id from taxa " + 
                                 "where name = %s", (scientificname))
                result = cursor.fetchone()
                if result:
                    taxon_id = result[0]
                else:
                    print("Error: Can't find taxon in taxa. Name: " + scientificname)
                    continue # Skip this taxon.

                # Check if db row exists. 
                cursor.execute("select count(*) from taxa_media where taxon_id = %s and media_id = %s and media_type = %s", 
                               (taxon_id, row[1], row[2]))
                result = cursor.fetchone()
                if result[0] == 0: 
                    cursor.execute("insert into taxa_media(taxon_id, media_id, media_type, user_name, metadata_json) values (%s, %s, %s, %s, %s)", 
                                   (unicode(taxon_id), mediaid, mediatype, username, jsonstring))
                else:
                    cursor.execute("update taxa_media set metadata_json = %s where taxon_id = %s and media_id = %s and media_type = %s"
                                   (jsonstring, unicode(taxon_id), mediaid, mediatype))
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
                header = map(string.strip, row.split(field_separator))
                header = map(unicode, header)
                pass
            else:
                row = map(string.strip, row.split(field_separator))
                row = map(unicode, row)
                #
                scientificname = row[0] # Scientific name
                mediaid = row[1] # Media id
                sortorder = row[4] # Media type
                # Get taxon_id from name.
                cursor.execute("select id from taxa " + 
                                 "where name = %s", (scientificname))
                result = cursor.fetchone()
                taxonid = None
                if result:
                    taxonid = result[0]
                else:
                    print("Error: Can't find taxon i taxa. Name: " + scientificname)
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
               (unicode(taxonid), ';'.join(taxondict[taxonid])))
        #
        infile.close()
    #
    except mysql.Error, e:
        print("ERROR: MySQL %d: %s" % (e.args[0], e.args[1]))
        print("ERROR: Script will be terminated.")
        sys.exit(1)
    finally:
        if db: db.close()
        if cursor: cursor.close()


# Main.
if __name__ == '__main__':
    execute()

