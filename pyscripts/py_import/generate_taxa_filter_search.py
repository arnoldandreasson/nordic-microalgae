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
import string

def execute(db_host = 'localhost', 
            db_name = 'nordicmicroalgae', 
            db_user = 'root', 
            db_passwd = '',
            ):
    """ Automatically generated db table for filter-related lookup. """
    db = None
    cursor = None
    try:
        # Connect to db.
        db = connect_to_db.connect(db_host, db_name, db_user, db_passwd)
        cursor=db.cursor()
        # Remove all rows in table taxa_filter_search.
        cursor.execute(""" delete from taxa_filter_search """) 
        #
        # Loop through all taxa.
        cursor.execute("select id, name from taxa")
        for taxon_id, taxon_name in cursor.fetchall():
            #
            # Check if illustrated. 
            #
            cursor.execute("select count(*) from taxa_media where taxon_id = %s", taxon_id)
            result = cursor.fetchone()
            if result[0] > 0: 
                # Add row in taxa_filter_search.
                cursor.execute("insert into taxa_filter_search(taxon_id, filter, value) values (%s, %s, %s)", 
                               (taxon_id, 'Illustrated', 'True'))
            #
            # Check if HELCOM PEG. 
            #
            cursor.execute("select count(*) from taxa_helcom_peg where taxon_id = %s", taxon_id)
            result = cursor.fetchone()
            if result[0] > 0: 
                # Add row in taxa_filter_search.
                cursor.execute("insert into taxa_filter_search(taxon_id, filter, value) values (%s, %s, %s)", 
                               (taxon_id, 'HELCOM PEG', 'True'))
            #
            # Check if Harmful. 
            #
            cursor.execute("select count(*) from taxa_external_facts where (taxon_id = %s) and (provider = %s)", 
                           (taxon_id, 'IOC'))
            result = cursor.fetchone()
            if result[0] > 0: 
                # Add row in taxa_filter_search.
                cursor.execute("insert into taxa_filter_search(taxon_id, filter, value) values (%s, %s, %s)", 
                               (taxon_id, 'Harmful', 'True'))
        #
        # Loop through taxon_facts. 
        cursor.execute("select taxon_id, facts_json from taxa_facts")
        for taxon_id, facts_json in cursor.fetchall():
                # Unpack json.
                factsdict = json.loads(facts_json, encoding = 'utf-8')
                #
                # Add rows from Facts.Country.
                #
                if 'Country' in factsdict:
                    for item in factsdict['Country']:
                        # Add row in taxa_filter_search.
                        cursor.execute("insert into taxa_filter_search(taxon_id, filter, value) values (%s, %s, %s)", 
                                       (taxon_id, 'Country', item))
                #
                # Add rows from Facts.Geographic area.
                #
                if 'Geographic area' in factsdict:
                    for item in factsdict['Geographic area']:
                        # Add row in taxa_filter_search.
                        cursor.execute("insert into taxa_filter_search(taxon_id, filter, value) values (%s, %s, %s)", 
                                       (taxon_id, 'Geographic area', item))
                #
                # Add rows from Facts.Habitat
                #
                if 'Habitat' in factsdict:
                    for item in factsdict['Habitat']:
                        # Add row in taxa_filter_search.
                        cursor.execute("insert into taxa_filter_search(taxon_id, filter, value) values (%s, %s, %s)", 
                                       (taxon_id, 'Habitat', item))
                #
                # Add rows from Facts.Trophic type
                #
                if 'Trophic type' in factsdict:
                    for item in factsdict['Trophic type']:
                        # Add row in taxa_filter_search.
                        cursor.execute("insert into taxa_filter_search(taxon_id, filter, value) values (%s, %s, %s)", 
                                       (taxon_id, 'Trophic type', item))
    #
    except mysql.Error, e:
        print("ERROR: MySQL %d: %s" % (e.args[0], e.args[1]))
        print("ERROR: Script will be terminated.")
        sys.exit(1)
    finally:
        if cursor: cursor.close()
        if db: db.close()


# Main.
if __name__ == '__main__':
    execute()

