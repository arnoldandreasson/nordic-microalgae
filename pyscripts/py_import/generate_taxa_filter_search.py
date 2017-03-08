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
    """ Automatically generated db table for filter-related lookup. """
    db = None
    cursor = None
    try:
        # Connect to db.
        db = mysql.connector.connect(host = db_host, db = db_name, 
                           user = db_user, passwd = db_passwd,
                           use_unicode = True, charset = 'utf8')
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
            cursor.execute("select count(*) from taxa_media where taxon_id = %s", 
                           (taxon_id,) )
            result = cursor.fetchone()
            if result[0] > 0: 
                # Add row in taxa_filter_search.
                cursor.execute("insert into taxa_filter_search(taxon_id, filter, value) values (%s, %s, %s)", 
                               (taxon_id, 'Illustrated', 'True'))
            else: 
                # New filter added 2011-02-21. Name: "Not illustrated".
                cursor.execute("insert into taxa_filter_search(taxon_id, filter, value) values (%s, %s, %s)", 
                               (taxon_id, 'Not illustrated', 'True'))
            #
            # Check if HELCOM PEG. 
            #
            cursor.execute("select count(*) from taxa_helcom_peg where taxon_id = %s", 
                           (taxon_id,) )
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
            # Filters for GROUPS OF ORGANISMS
            #
            cursor.execute("select rank, classification from taxa_navigation where taxon_id = %s", 
                           (taxon_id,) )
            result = cursor.fetchone()
            if result:
                rank = result[0] 
                classification = result[1]
                # Only add filter if species or below in rank.
                if rank in ['Species', 'Subspecies', 'Variety', 'Form', 'Hybrid']:
                    # - GROUPS OF ORGANISMS: All.
                    # Add row in taxa_filter_search.
                    cursor.execute("insert into taxa_filter_search(taxon_id, filter, value) values (%s, %s, %s)", 
                                   (taxon_id, 'Group', 'All'))
                    
                    # - GROUPS OF ORGANISMS: Cyanobacteria.
                    #   (Cyanobacteria)
                    if 'Cyanobacteria' in classification:
                        cursor.execute("insert into taxa_filter_search(taxon_id, filter, value) values (%s, %s, %s)", 
                                       (taxon_id, 'Group', 'Cyanobacteria'))
                        
                    
                    # - GROUPS OF ORGANISMS: Diatoms.
                    #   (Bacillariophyta)
                    if 'Bacillariophyta' in classification:
                        cursor.execute("insert into taxa_filter_search(taxon_id, filter, value) values (%s, %s, %s)", 
                                       (taxon_id, 'Group', 'Diatoms'))
                    
                    # - GROUPS OF ORGANISMS: Dinoflagellates.
                    #   (Dinophyceae)
                    if 'Dinophyceae' in classification:
                        cursor.execute("insert into taxa_filter_search(taxon_id, filter, value) values (%s, %s, %s)", 
                                       (taxon_id, 'Group', 'Dinoflagellates'))
                    
                    # - GROUPS OF ORGANISMS: Other microalgae.
                    #   (Cryptophyceae + Haptophyta + Bolidophyceae + Chrysophyceae + Dictyochophyceae + 
                    #   Eustigmatophyceae + Pelagophyceae  + Raphidophyceae  + Synurophyceae  + Chlorophyta + 
                    #   Glaucophyta + Coleochaetophyceae + Klebsormidiophyceae + Mesostigmatophyceae + 
                    #   Zygnematophyceae + Euglenophyceae)
                    found = False
                    for taxon in ['Cryptophyceae', 'Haptophyta', 'Bolidophyceae', 'Chrysophyceae', 'Dictyochophyceae', 
                                  'Eustigmatophyceae', 'Pelagophyceae', 'Raphidophyceae', 'Synurophyceae', 'Chlorophyta',
                                  'Glaucophyta', 'Coleochaetophyceae', 'Klebsormidiophyceae', 'Mesostigmatophyceae',
                                  'Zygnematophyceae', 'Euglenophyceae']:
                        if taxon in classification:
                            found = True
                            break
                    if found:
                        cursor.execute("insert into taxa_filter_search(taxon_id, filter, value) values (%s, %s, %s)", 
                                       (taxon_id, 'Group', 'Other microalgae'))

                    # - GROUPS OF ORGANISMS: Ciliates.
                    #   (Ciliophora)
                    if 'Ciliophora' in classification:
                        cursor.execute("insert into taxa_filter_search(taxon_id, filter, value) values (%s, %s, %s)", 
                                       (taxon_id, 'Group', 'Ciliates'))
                    
                    # - GROUPS OF ORGANISMS: Other protozoa.
                    #   (Cryptophyta, ordines incertae sedis + Bicosoecophyceae + Bodonophyceae + 
                    #   Heterokontophyta, ordines incertae sedis + Cercozoa + Craspedophyceae + 
                    #   Ellobiopsea + Protozoa, classes incertae sedis)
                    found = False
                    for taxon in ['Cryptophyta, ordines incertae sedis', 'Bicosoecophyceae', 'Bodonophyceae',
                                  'Heterokontophyta, ordines incertae sedis', 'Cercozoa', 'Craspedophyceae',
                                  'Ellobiopsea', 'Protozoa, classes incertae sedis']:
                        if taxon in classification:
                            found = True
                            break
                    if found:
                        cursor.execute("insert into taxa_filter_search(taxon_id, filter, value) values (%s, %s, %s)", 
                                       (taxon_id, 'Group', 'Other protozoa'))
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

