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
import json
import codecs
import string
import connect_to_db

def execute(taxa_facts_file_name = '../data_backup/taxa_facts_backup.txt', 
            taxa_media_file_name = '../data_backup/taxa_media_backup.txt', 
            taxa_media_list_file_name = '../data_backup/taxa_media_list_backup.txt', 
            change_history_file_name = '../data_backup/change_history_backup.txt', 
            file_encoding = 'utf16',
            field_separator = '\t', 
            row_delimiter = '\r\n'): # For windows usage.
    """ 
    Imports data to database from backup file. Backup must be done by running 
    'export_to_backup.py'. 
    Use this import after a database rebuild. Taxa must be loaded before.
    """
    try:
        # Connect to db.
        db = connect_to_db.connect()
        cursor=db.cursor()
        # Remove all rows in table taxa_facts.
        cursor.execute(""" delete from taxa_facts """) 
        # Remove all rows in table taxa_media.
        cursor.execute(""" delete from taxa_media """) 
        # Remove all rows in table taxa_media_list.
        cursor.execute(""" delete from taxa_media_list """) 
        # Remove all rows in table change_history.
        cursor.execute(""" delete from change_history """) 
        # Create dictionary for translations from taxon_name to taxon_id.
        taxonnametoid = {}
        cursor.execute("select id, name from taxa")
        for taxon_id, taxon_name in cursor.fetchall():
            taxonnametoid[taxon_name] = taxon_id
        #    
        # TAXA FACTS.    
        # Open file for reading.
        infile = codecs.open(taxa_facts_file_name, mode = 'r', encoding = file_encoding)    
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
                    # Repack json and add pretty print (by setting indent=4).
                    factsdict = json.loads(facts_json, encoding = 'utf-8')
                    facts_json = json.dumps(factsdict, encoding = 'utf-8', 
                                         sort_keys = True, indent = 4)
                    # Write to database.
                    cursor.execute("insert into taxa_facts(taxon_id, facts_json) values (%s, %s)", 
                                   (taxon_id, facts_json))
                else:
                    print("From backup, table taxa_facts: Can't find taxon name in table taxa. Name: " + row[0])



        #    
        # TAXA SYNONYMS.    
        # Open file and write header.
        #create table taxa_synonyms (
        #taxon_id           int unsigned not null, -- FK.
        #synonym_name       varchar(128) not null default '',
        #synonym_author     varchar(256) not null default '',
        #info_json          text not null default '',

        
        
        #    
        # TAXA MEDIA.    
        # Open file for reading.
        infile = codecs.open(taxa_media_file_name, mode = 'r', encoding = file_encoding)    
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
                    media_id = row[1]
                    media_type = row[2]
                    user_name = row[3]
                    metadata_json = row[4]
                    # Repack json and add pretty print (by setting indent=4).
                    factsdict = json.loads(metadata_json, encoding = 'utf-8')
                    metadata_json = json.dumps(factsdict, encoding = 'utf-8', 
                                         sort_keys = True, indent = 4)
                    # Write to database.
                    cursor.execute("insert into taxa_media(taxon_id, media_id, media_type, user_name, metadata_json) values (%s, %s, %s, %s, %s)", 
                                   (taxon_id, media_id, media_type, user_name, metadata_json))
                else:
                    print("From backup, table taxa_media: Can't find taxon name in table taxa. Name: " + row[0])
        #    
        # TAXA MEDIA LIST.    
        # Open file for reading.
        infile = codecs.open(taxa_media_list_file_name, mode = 'r', encoding = file_encoding)    
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
                    media_list = row[1]
                    # Write to database.
                    cursor.execute("insert into taxa_media_list(taxon_id, media_list) values (%s, %s)", 
                                   (taxon_id,media_list))
                else:
                    print("From backup, table taxa_media_list: Can't find taxon name in table taxa. Name: " + row[0])
        #    
        # CHANGE HISTORY.    
        # Open file for reading.
        infile = codecs.open(change_history_file_name, mode = 'r', encoding = file_encoding)    
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
                else:
                    # This taxon is not available any longer. The change history row should be stored,
                    # but not connected to a valid taxon. 
                    taxon_id = 0
                current_taxon_name = row[1]
                user_name = row[2]
                description = row[3]
                timestamp = row[4]
                # Repack json and add pretty print (by setting indent=4).
                factsdict = json.loads(metadata_json, encoding = 'utf-8')
                metadata_json = json.dumps(factsdict, encoding = 'utf-8', 
                                     sort_keys = True, indent = 4)
                # Write to database.
                cursor.execute("insert into change_history(taxon_id, current_taxon_name, user_name, description, timestamp) values (%s, %s, %s, %s, %s)", 
                               (taxon_id, current_taxon_name, user_name, description, timestamp))
        #    
        # Log import from backup to change_history.
        description = 'Import_from_backup.py: Tables are loaded from backup files.'    
        cursor.execute("insert into change_history(taxon_id, current_taxon_name, user_name, description, timestamp) values (%s, %s, %s, %s, now())", 
                       (unicode(0), '', 'db-admin', description))
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
