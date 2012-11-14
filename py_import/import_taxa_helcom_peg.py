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
#import plankton_toolbox.core.biology.taxa as taxa
#import plankton_toolbox.core.biology.taxa_sources as taxa_sources

    
def execute(file_name = '../data_import/peg_bvol2011.json',
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
        db = mysql.connect(host = db_host, db = db_name, 
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
                row = map(string.strip, row.split(field_separator))
                row = map(unicode, row)
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
                             "where name = %s", (name))
            result = cursor.fetchone()
            if result:
                taxon_id = result[0]
                
                jsonstring = json.dumps(pegitem, encoding = 'utf-8', 
                                        sort_keys=True, indent=4)
                cursor.execute("insert into taxa_helcom_peg(taxon_id, facts_json) values (%s, %s)", 
                               (unicode(taxon_id), unicode(jsonstring)))
            else:
                print("Error: Import HELCOM PEG. Can't find taxon for: " + name)
                continue # Skip this taxon.
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
    
