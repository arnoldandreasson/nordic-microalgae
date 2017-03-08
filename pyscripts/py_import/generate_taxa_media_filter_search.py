#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Nordicmicroalgae. http://nordicmicroalgae.org/
# Copyright (c) 2011-2017 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import mysql.connector
import sys
import json

def execute(db_host = 'localhost', 
            db_name = 'nordicmicroalgae', 
            db_user = 'root', 
            db_passwd = ''
            ):
    """ Automatically generated db table for filter-related media lookup. """
    db = None
    cursor = None
    try:
        # Connect to db.
        db = mysql.connector.connect(host = db_host, db = db_name, 
                           user = db_user, passwd = db_passwd,
                           use_unicode = True, charset = 'utf8')
        cursor=db.cursor()
        # Remove all rows in table taxa_media_filter_search.
        cursor.execute(""" delete from taxa_media_filter_search """) 
        #
        # Loop through taxon_media. 
        cursor.execute("select taxon_id, media_id, metadata_json from taxa_media")
        #
        hall_of_fame_dict = {}
        #
        for taxon_id, media_id, metadata_json in cursor.fetchall():
            # Unpack json.
            metadatadict = json.loads(metadata_json, encoding = 'utf-8')
            #
            # Add rows from 'Image galleries'.
            #
            if 'Image galleries' in metadatadict:
                for gallery in metadatadict['Image galleries']:
                    # Add row in taxa_media_filter_search.
                    cursor.execute("insert into taxa_media_filter_search(taxon_id, media_id, filter, value) " +
                                   "values (%s, %s, %s, %s)", 
                                   (taxon_id, media_id, 'Gallery', gallery))
            #
            # Add rows from 'Latest images'. Value is date-time.
            #
            if 'Date added' in metadatadict:
                datetime = metadatadict['Date added']
                cursor.execute("insert into taxa_media_filter_search(taxon_id, media_id, filter, value) " +
                               "values (%s, %s, %s, %s)", 
                               (taxon_id, media_id, 'Latest images', datetime))
            #
            # 'Hall of fame, part 1'. Add filter 'Artist' for value of photographer/artist.
            #
            if 'Photographer/artist' in metadatadict:
                photographer =  metadatadict['Photographer/artist']
                cursor.execute("insert into taxa_media_filter_search(taxon_id, media_id, filter, value) " +
                               "values (%s, %s, %s, %s)", 
                               (taxon_id, media_id, 'Artist', photographer))
            #
            # 'Hall of fame, part 2'. Count images for each photographer/artist.
            #
            if 'Photographer/artist' in metadatadict:
                photographer =  metadatadict['Photographer/artist']
                if photographer in hall_of_fame_dict:
                    hall_of_fame_dict[photographer] = hall_of_fame_dict[photographer] + 1
                else:
                    hall_of_fame_dict[photographer] = 1
        #
        # Add rows from 'Hall of fame'. Value is a key-value-pair "Photographer":"counter".
        #
        for key, value in hall_of_fame_dict.items():
            cursor.execute("insert into taxa_media_filter_search(taxon_id, media_id, filter, value) " +
                           "values (%s, %s, %s, %s)", 
                           (0, '', 'Hall of fame', key + ':' + str(value)))
    #
    except mysql.connector.Error as e:
        print("ERROR: MySQL %d: %s" % (e.args[0], e.args[1]))
        print("ERROR: Script will be terminated.")
        sys.exit(1)
    finally:
        if cursor: cursor.close()
        if db: db.close()


# To be used when this module is launched directly from the command line.
import getopt
def main():
    # Parse command line options.
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:d:u:p:", ["host=", "database=", "user=", "password="])
    except getopt.error as msg:
        print(msg)
        sys.exit(2)
    # Create dictionary with named arguments.
    params = {}
    for opt, arg in opts:
        if opt in ("-h", "--host"):
            params['db_host'] = arg
        elif opt in ("-d", "--database"):
            params['db_name'] = arg
        elif opt in ("-u", "--user"):
            params['db_user'] = arg
        elif opt in ("-p", "--password"):
            params['db_passwd'] = arg
    # Execute with parameter list.
    execute(**params) # The "two stars" prefix converts the dictionary into named arguments. 

if __name__ == "__main__":
    main()

