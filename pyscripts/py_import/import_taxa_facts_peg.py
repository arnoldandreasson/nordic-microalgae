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
import connect_to_db
import json
import plankton_toolbox.core.biology.taxa as taxa
import plankton_toolbox.core.biology.taxa_sources as taxa_sources

    
def execute(file_name = '../data_external/PEG_BVOL2010.json'):
    """ Imports facts related to size classes produced by HELCOMs Plankton Expert Group. """
    try:
        # Connect to db.
        db = connect_to_db.connect()
        cursor=db.cursor()
        # Remove all rows from table.
        cursor.execute(" delete from taxa_facts_peg ")
        cursor.close()
        cursor=db.cursor()
        # Read json file into PEG object.
        peg = taxa.Peg() 
        peg.clear()
        importer = taxa_sources.JsonFile(taxaObject = peg)
        importer.importTaxa(file = file_name)
        # Create lookup dictionary for Dyntaxa names.
        dyntaxanamedict = {}
        for taxon in peg.getTaxonList():
            if "Dyntaxa name" in taxon:
                dyntaxanamedict[taxon["Dyntaxa name"]] = taxon
        # Iterate over all rows in taxa table.
        cursor.execute("select id, name from taxa")
        for row in cursor.fetchall():
            id, name = row
            pegobject = dyntaxanamedict.get(name, None)
            # If PEG-object exists, insert into the taxa_facts_peg table.
            if pegobject:
                jsonstring = json.dumps(pegobject, encoding = 'utf-8', 
                                        sort_keys=True, indent=4)
                cursor.execute("insert into taxa_facts_peg(taxon_id, facts_json) values (%s, %s)", 
                               (unicode(id), unicode(jsonstring)))
    #
    except mysql.Error, e:
        print ("ERROR: MySQL %d: %s" % (e.args[0], e.args[1]))
        print ("ERROR: Script will be terminated.")
        sys.exit(1)
    finally:
        if cursor: cursor.close()
        if db: db.close()

    
# Main.
if __name__ == '__main__':
    execute()
    
