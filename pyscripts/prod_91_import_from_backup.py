#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Nordicmicroalgae. http://nordicmicroalgae.org/
# Copyright (c) 2011-2017 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import nordicmicroalgae_settings as settings

#import mysql.connector
import mysql.connector
import sys
import os
import json
import codecs
# import string

def execute(db_host = settings.MYSQL_HOST, 
            db_name = settings.MYSQL_DATABASE, 
            db_user = settings.MYSQL_USER, 
            db_passwd = settings.MYSQL_PASSWORD, 
            taxa_facts_file_name = 'data_backup/OLD_Backup/taxa_facts_backup.txt', 
            taxa_media_file_name = 'data_backup/OLD_Backup/taxa_media_backup.txt', 
            taxa_media_list_file_name = 'data_backup/OLD_Backup/taxa_media_list_backup.txt', 
            change_history_file_name = 'data_backup/OLD_Backup/change_history_backup.txt', 
#             taxa_facts_file_name = 'data_backup/backup_taxa_facts.txt', 
#             taxa_media_file_name = 'data_backup/backup_taxa_media.txt', 
#             taxa_media_list_file_name = 'data_backup/backup_taxa_media_list.txt', 
#             change_history_file_name = 'data_backup/backup_change_history.txt', 
            file_encoding = 'utf16',
            field_separator = '\t', 
            row_delimiter = '\r\n',
            **more_options):
    """ 
    Imports data to database from backup file. Backup must be done by running 
    'export_to_backup.py'. 
    Use this import after a database rebuild. Taxa must be loaded before.
    """
    
    # Check that backup files exists before deleting db content.
    if not os.path.isfile(taxa_facts_file_name):
        print("Import from backap terminated. Can't find file: " + taxa_facts_file_name)
        return
    if not os.path.isfile(taxa_media_file_name):
        print("Import from backap terminated. Can't find file: " + taxa_media_file_name)
        return
    if not os.path.isfile(taxa_media_list_file_name):
        print("Import from backap terminated. Can't find file: " + taxa_media_list_file_name)
        return
    if not os.path.isfile(change_history_file_name):
        print("Import from backap terminated. Can't find file: " + change_history_file_name)
        return
        
    try:
        # Connect to db.
        db = mysql.connector.connect(host = db_host, db = db_name, 
                           user = db_user, passwd = db_passwd,
                           use_unicode = True, charset = 'utf8')
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
                headers = list(map(str.strip, row.split(field_separator)))
                # headers = list(map(unicode, headers))
            else:
                row = list(map(str.strip, row.split(field_separator)))
                # row = list(map(unicode, row))
                if row[0] in taxonnametoid:
                    taxon_id = taxonnametoid[row[0]]
                    facts_json = row[1]
                    # Repack json and add pretty print (by setting indent=4).
                    factsdict = json.loads(facts_json, encoding = 'utf-8')
                    facts_json = json.dumps(factsdict, # encoding = 'utf-8', 
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
        metadata_json = ''
        #
        for rowindex, row in enumerate(infile):
            if rowindex == 0: # First row is assumed to be the header row.
                headers = list(map(str.strip, row.split(field_separator)))
                # headers = list(map(unicode, headers))
            else:
                row = list(map(str.strip, row.split(field_separator)))
                # row = list(map(unicode, row))
                if row[0] in taxonnametoid:
                    taxon_id = taxonnametoid[row[0]]
                    media_id = row[1]
                    media_type = row[2]
                    user_name = row[3]
                    metadata_json = row[4]
                    # Repack json and add pretty print (by setting indent=4).
                    factsdict = json.loads(metadata_json, encoding = 'utf-8')
                    metadata_json = json.dumps(factsdict, # encoding = 'utf-8', 
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
                headers = list(map(str.strip, row.split(field_separator)))
                # headers = list(map(unicode, headers))
            else:
                row = list(map(str.strip, row.split(field_separator)))
                # row = list(map(unicode, row))
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
                headers = list(map(str.strip, row.split(field_separator)))
                # headers = list(map(unicode, headers))
            else:
                row = list(map(str.strip, row.split(field_separator)))
                # row = list(map(unicode, row))
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
#                 # Repack json and add pretty print (by setting indent=4).
#                 factsdict = json.loads(metadata_json, encoding = 'utf-8')
#                 metadata_json = json.dumps(factsdict, # encoding = 'utf-8', 
#                                      sort_keys = True, indent = 4)
                # Write to database.
                cursor.execute("insert into change_history(taxon_id, current_taxon_name, user_name, description, timestamp) values (%s, %s, %s, %s, %s)", 
                               (taxon_id, current_taxon_name, user_name, description, timestamp))
        #    
        # Log import from backup to change_history.
        description = 'Import_from_backup.py: Tables are loaded from backup files.'    
        cursor.execute("insert into change_history(taxon_id, current_taxon_name, user_name, description, timestamp) values (%s, %s, %s, %s, now())", 
                       (str(0), '', 'db-admin', description))
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

