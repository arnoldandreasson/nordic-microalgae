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
# import string
#import plankton_toolbox.core.biology.taxa as taxa
#import plankton_toolbox.core.biology.taxa_sources as taxa_sources

    
def execute(file_name = '../data_import/peg_bvol2013.json',
            translate_file_name = '../data_import/peg_to_dyntaxa.txt', 
            file_encoding = 'utf16',
            field_separator = '\t', 
            db_host = 'localhost', 
            db_name = 'nordicmicroalgae', 
            db_user = 'root', 
            db_passwd = ''
            ):
    """ Imports facts related to size classes produced by HELCOMs Plankton Expert Group. """
    db = None
    cursor = None
    try:
        # Connect to db.
        db = mysql.connector.connect(host = db_host, db = db_name, 
                           user = db_user, passwd = db_passwd,
                           use_unicode = True, charset = 'utf8')
        cursor=db.cursor()
        # Remove all rows from table.
        cursor.execute(" delete from taxa_helcom_peg ")
        cursor.close()
        cursor=db.cursor()
        # Read translation file and add to dictionary.
        translatedict = {}
        infile = codecs.open(translate_file_name, mode = 'r', encoding = file_encoding)    
        for rowindex, row in enumerate(infile):
            if rowindex == 0: # First row is assumed to be the header row.
                pass
            else:
                row = list(map(str.strip, row.split(field_separator)))
                # row = list(map(unicode, row))
                pegname = row[0]    
                dyntaxaname = row[1]
                translatedict[pegname] = dyntaxaname
        # Read json file into HELCOM PEG object.
        indata = codecs.open(file_name, mode = 'r', encoding = 'utf8')
        helcompeg = json.loads(indata.read(), encoding = 'utf8')
        indata.close()
        
        #
        for pegitem in helcompeg:
            #
            name = pegitem['Species']
            # Translate to dyntaxa.
            if name in translatedict:
                name = translatedict[name]
            # Get taxon_id from name.
            cursor.execute("select id from taxa " + 
                             "where name = %s", 
                             (name,))
            result = cursor.fetchone()
            if result:
                taxon_id = result[0]
                
                jsonstring = json.dumps(pegitem, # encoding = 'utf-8', 
                                        sort_keys=True, indent=4)
                cursor.execute("insert into taxa_helcom_peg(taxon_id, facts_json) values (%s, %s)", 
                               (str(taxon_id), str(jsonstring)))
            else:
                print("Warning: Import HELCOM PEG. Can't find taxon for: " + name)
                continue # Skip this taxon.
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
    
