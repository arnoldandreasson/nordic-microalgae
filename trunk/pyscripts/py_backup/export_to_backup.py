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

def execute(db_host = 'localhost', 
            db_name = 'nordicmicroalgae', 
            db_user = 'root', 
            db_passwd = '',
            taxa_facts_file_name = '../data_backup/taxa_facts_backup.txt', 
            taxa_media_file_name = '../data_backup/taxa_media_backup.txt', 
            taxa_media_list_file_name = '../data_backup/taxa_media_list_backup.txt', 
            change_history_file_name = '../data_backup/change_history_backup.txt', 
            file_encoding = 'utf16',
            field_separator = '\t', 
            row_delimiter = '\r\n'):
    """ 
    Exports database tables to text files for backup. Json data is not unpacked. 
    Internal keys for taxon_id are not exported, they are replaced by taxon names. 
    Tables generated from external sources are not exported.
    Run this export before rebuilding the database. Run 'import_from_backup.py' when
    taxa and data from external sources are loaded.    
    """
    db = None
    cursor = None
    out = None
    try:
        # Connect to db.
        db = mysql.connect(host = db_host, db = db_name, 
                           user = db_user, passwd = db_passwd,
                           use_unicode = True, charset = 'utf8')
        cursor=db.cursor()        
        # Create dictionary for translations from taxon_id to taxon_name.
        taxonidtoname = {}
        cursor.execute("select id, name from taxa")
        for taxon_id, taxon_name in cursor.fetchall():
            taxonidtoname[taxon_id] = taxon_name
        #    
        # TAXA FACTS.    
        # Open file and write header.
        out = codecs.open(taxa_facts_file_name, mode = 'w', encoding = file_encoding)
        # Create and print header row.
        outheader = ['Taxon name', 'Facts json']
        out.write(field_separator.join(outheader) + row_delimiter)
        # Loop through rows.
        cursor.execute("select taxon_id, facts_json from taxa_facts")
        for taxon_id, facts_json in cursor.fetchall():
            if taxon_id in taxonidtoname:
                taxonname = taxonidtoname[taxon_id] 
                # Repack json and remove pretty print (by setting indent=None).
                factsdict = json.loads(facts_json, encoding = 'utf-8')
                facts_json = json.dumps(factsdict, encoding = 'utf-8', 
                                     sort_keys = True, indent = None)
                # Print row.
                out.write(taxonname + field_separator + facts_json + row_delimiter)
            else:
                print("To backup, table taxa_facts: Can't find taxon id in table taxa. Id: " + unicode(taxon_id))               
        #
        out.close()



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
        # Open file and write header.
        out = codecs.open(taxa_media_file_name, mode = 'w', encoding = file_encoding)
        # Create and print header row.
        outheader = ['Taxon name', 'Media id', 'Media type', 'User name', 'Media json']
        out.write(field_separator.join(outheader) + row_delimiter)
        # Loop through rows.
        cursor.execute("select taxon_id, media_id, media_type, user_name, metadata_json from taxa_media")
        for taxon_id, media_id, media_type, user_name, metadata_json in cursor.fetchall():
            if taxon_id in taxonidtoname:
                taxonname = taxonidtoname[taxon_id] 
                # Repack json and remove pretty print (by setting indent=None).
                factsdict = json.loads(metadata_json, encoding = 'utf-8')
                metadata_json = json.dumps(factsdict, encoding = 'utf-8', 
                                     sort_keys = True, indent = None)
                # Print row.
                out.write(taxonname + field_separator + 
                          media_id + field_separator + 
                          media_type + field_separator + 
                          user_name + field_separator + 
                          metadata_json + row_delimiter)
            else:
                print("To backup, table taxa_media: Can't find taxon id in table taxa. Id: " + unicode(taxon_id))
        #    
        # TAXA MEDIA LIST.    
        # Open file and write header.
        out = codecs.open(taxa_media_list_file_name, mode = 'w', encoding = file_encoding)
        # Create and print header row.
        outheader = ['Taxon name', 'Media list']
        out.write(field_separator.join(outheader) + row_delimiter)
        # Loop through rows.
        cursor.execute("select taxon_id, media_list from taxa_media_list")
        for taxon_id, media_list in cursor.fetchall():
            if taxon_id in taxonidtoname:
                taxonname = taxonidtoname[taxon_id] 
                # Print row.
                out.write(taxonname + field_separator + 
                          media_list + row_delimiter)
            else:
                print("To backup, table taxa_media_list: Can't find taxon id in table taxa. Id: " + unicode(taxon_id))
        #    
        # CHANGE HISTORY.    
        # Open file and write header.
        out = codecs.open(change_history_file_name, mode = 'w', encoding = file_encoding)
        # Create and print header row.
        outheader = ['Taxon name', 'Current taxon name', 'User name', 'Description', 'Timestamp']
        out.write(field_separator.join(outheader) + row_delimiter)
        # Loop through rows.
        cursor.execute("select taxon_id, current_taxon_name, user_name, description, timestamp from change_history")
        for taxon_id, current_taxon_name, user_name, description, timestamp in cursor.fetchall():
            if taxon_id in taxonidtoname:
                taxonname = taxonidtoname[taxon_id]
            else:
                # Taxon missing. The row should be saved, but not connected to a valid taxon. 
                taxonname = '' 
            # Print row.
            out.write(taxonname + field_separator + 
                      current_taxon_name + field_separator + 
                      user_name + field_separator + 
                      description + field_separator + 
                      unicode(timestamp) + row_delimiter)
    #
    except (IOError, OSError):
        print("ERROR: Can't write to text file.")
        print("ERROR: Script will be terminated.")
#        print(sys.exc_info())
        sys.exit(1)
    except mysql.Error, e:
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
