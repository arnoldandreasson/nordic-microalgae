#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Nordicmicroalgae. http://nordicmicroalgae.org/
# Copyright (c) 2011-2017 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import mysql.connector
import sys
import codecs
# import string
import json

def execute(file_name_sccap = '../data_import/external_facts_culture_collections_sccap.txt', 
#            file_encoding = 'utf16',
            file_encoding = 'cp1258',
            field_separator = '\t', 
            row_delimiter = '\r\n',
            db_host = 'localhost', 
            db_name = 'nordicmicroalgae', 
            db_user = 'root', 
            db_passwd = '',
            delete_db_content = False
            ):
    """ Imports facts prepared from external sources. """
    try:
        # Connect to db.
        db = mysql.connector.connect(host = db_host, db = db_name, 
                           user = db_user, passwd = db_passwd,
                           use_unicode = True, charset = 'utf8')
        cursor=db.cursor()
        # Remove all rows in table.
        if delete_db_content == True:
            cursor.execute(""" delete from taxa_external_facts """)
        
        # === Culture collections SCCAP === 
        # Dictionary used if more than one strain on one species.
        strainsforspecies = {} # Dictionary with html-coded strain list.
        print("")
        print("=== Culture collections SCCAP ===")
        # Open file for reading.
        infile = codecs.open(file_name_sccap, mode = 'r', encoding = file_encoding)    
        # Iterate over rows in file.
        for rowindex, row in enumerate(infile):
            if rowindex == 0: # First row is assumed to be the header row.
                # CUNR    GENUS    SPECIES    CLASS    COUNTRY    Foto    Availability
                pass
            else:
                row = list(map(str.strip, row.split(field_separator)))
                # row = list(map(unicode, row))
                # Get taxon_id from name.
                if row[2] == 'sp.':
                    speciesname = row[1]
                else:
                    speciesname = row[1] + ' ' + row[2]
                #
                cursor.execute("select id from taxa " + 
                                 "where name = %s", (speciesname,))
                result = cursor.fetchone()
                if result:
                    taxon_id = result[0]
                else:
                    print("Warning: Can't find taxon i taxa. Name: " + speciesname)
                    continue # Skip this taxon.
                # Get facts_json from db.
                cursor.execute("select facts_json from taxa_external_facts " + 
                               "where (taxon_id = %s) and (provider = %s) ", 
                               (str(taxon_id), str('Generated facts')))
                result = cursor.fetchone()
                if result:
                    # From string to dictionary.
                    factsdict = json.loads(result[0], encoding = 'utf-8')
                else:
                    # Add empty columns.
                    factsdict = {}
                # Update facts.
                # Common info
                htmltext = """
<strong>SCCAP</strong><br/>
The Scandinavian Culture Collection of Algae and Protozoa at the University of Copenhagen <br/>
More info at <a href="http://www.sccap.dk/">http://www.sccap.dk.</a> <br/>
Strains: """
                # Strains. If a species has more than one strain the older list will be overwritten when more are detected in the indata file.
                strainhtml = '<a href="http://www.sccap.dk/search/details.asp?Cunr=' + row[0] + '">' + row[0] + '</a>'
                if not speciesname in strainsforspecies:
                    strainsforspecies[speciesname] = []
                strainsforspecies[speciesname].append(strainhtml) 
                factsdict['Culture collections'] = htmltext + ', '.join(strainsforspecies[speciesname])
                
                # Convert facts to string.
                jsonstring = json.dumps(factsdict, # encoding = 'utf-8', 
                                     sort_keys=True, indent=4)
                # Check if db row exists. 
                cursor.execute("select count(*) from taxa_external_facts " + 
                               "where (taxon_id = %s) and (provider = %s) ", 
                               (str(taxon_id), str('Generated facts')))
                result = cursor.fetchone()
                if result[0] == 0: 
                    cursor.execute("insert into taxa_external_facts(taxon_id, provider, facts_json) " + 
                                   "values (%s, %s, %s)", 
                                   (str(taxon_id), str('Generated facts'), jsonstring))
                else:
                    cursor.execute("update taxa_external_facts set facts_json = %s " + 
                                   "where (taxon_id = %s) and (provider = %s) ", 
                                   (jsonstring, str(taxon_id), str('Generated facts')))
        
    #
    except (IOError, OSError):
        print("ERROR: Can't read text file.")
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


# Main.
if __name__ == '__main__':
    execute()

