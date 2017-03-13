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

def execute(provider_dyntaxa_id = "Dyntaxa",
            file_name_dyntaxa_id = '../data_import/taxa_dyntaxa.txt', 
            provider_algaebase_id = "AlgaeBase",
            file_name_algaebase_id = '../data_import/external_links_algaebase.txt', 
            provider_omnidia_codes = "SLU",
            file_name_omnidia_codes = '../data_import/external_facts_omnidia_codes.txt', 
            provider_rebecca_codes = "NIVA",
            file_name_rebecca_codes = '../data_import/external_facts_rebecca_codes.txt', 
            provider_ioc_hab = "IOC",
            file_name_ioc_hab = '../data_import/external_facts_ioc_hab.txt', 
            file_encoding = 'utf16',
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
        
        # === Dyntaxa id === 
        print("")
        print("=== Dyntaxa id ===")
        # Open file for reading.
        infile = codecs.open(file_name_dyntaxa_id, mode = 'r', encoding = file_encoding)    
        # Iterate over rows in file.
        for rowindex, row in enumerate(infile):
            if rowindex == 0: # First row is assumed to be the header row.
                headers = list(map(str.strip, row.split(field_separator)))
                # headers = list(map(unicode, headers))
            else:
                row = list(map(str.strip, row.split(field_separator)))
                # row = list(map(unicode, row))
                # Get taxon_id from name.
                cursor.execute("select id from taxa " + 
                                 "where name = %s", (row[0],) )
                result = cursor.fetchone()
                if result:
                    taxon_id = result[0]
                else:
                    print("Warning: Can't find taxon i taxa. Name: " + row[0])
                    continue # Skip this taxon.
                # Get facts_json from db.
                cursor.execute("select facts_json from taxa_external_facts " + 
                               "where (taxon_id = %s) and (provider = %s) ", 
                               (str(taxon_id), str(provider_dyntaxa_id)))
                result = cursor.fetchone()
                if result:
                    # From string to dictionary.
                    factsdict = json.loads(result[0], encoding = 'utf-8')
                    # Add column values to row, if available.
                    for headeritem in headers:
                        row.append(factsdict.get(headeritem, ''))
                else:
                    # Add empty columns.
                    factsdict = {}
                # Update facts.
                for colindex, headeritem in enumerate(headers):
                    if headeritem == 'Dyntaxa id':
                        factsdict[headeritem] = row[colindex]
                # Convert facts to string.
                jsonstring = json.dumps(factsdict, # encoding = 'utf-8', 
                                     sort_keys=True, indent=4)
                # Check if db row exists. 
                cursor.execute("select count(*) from taxa_external_facts " + 
                               "where (taxon_id = %s) and (provider = %s) ", 
                               (str(taxon_id), str(provider_dyntaxa_id)))
                result = cursor.fetchone()
                if result[0] == 0: 
                    cursor.execute("insert into taxa_external_facts(taxon_id, provider, facts_json) " + 
                                   "values (%s, %s, %s)", 
                                   (str(taxon_id), str(provider_dyntaxa_id), jsonstring))
                else:
                    cursor.execute("update taxa_external_facts set facts_json = %s " + 
                                   "where (taxon_id = %s) and (provider = %s) ", 
                                   (jsonstring, str(taxon_id), str(provider_dyntaxa_id)))
        
        # === AlgaeBase_id === 
        print("")
        print("=== AlgaeBase_id ===")
        # Open file for reading.
        infile = codecs.open(file_name_algaebase_id, mode = 'r', encoding = file_encoding)    
        # Iterate over rows in file.
        for rowindex, row in enumerate(infile):
            if rowindex == 0: # First row is assumed to be the header row.
                headers = list(map(str.strip, row.split(field_separator)))
                # headers = list(map(unicode, headers))
            else:
                row = list(map(str.strip, row.split(field_separator)))
                # row = list(map(unicode, row))
                # Get taxon_id from name.
                cursor.execute("select id from taxa " + 
                                 "where name = %s", (row[0],) )
                result = cursor.fetchone()
                if result:
                    taxon_id = result[0]
                else:
                    print("Warning: Can't find taxon i taxa. Name: " + row[0])
                    continue # Skip this taxon.
                # Get facts_json from db.
                cursor.execute("select facts_json from taxa_external_facts " + 
                               "where (taxon_id = %s) and (provider = %s) ", 
                               (str(taxon_id), str(provider_algaebase_id)))
                result = cursor.fetchone()
                if result:
                    # From string to dictionary.
                    factsdict = json.loads(result[0], encoding = 'utf-8')
                    # Add column values to row, if available.
                    for headeritem in headers:
                        row.append(factsdict.get(headeritem, ''))
                else:
                    # Add empty columns.
                    factsdict = {}
                # Update facts.
                for colindex, headeritem in enumerate(headers):
                    if headeritem == 'Algaebase id':
                        factsdict[headeritem] = row[colindex]
                # Convert facts to string.
                jsonstring = json.dumps(factsdict, # encoding = 'utf-8', 
                                     sort_keys=True, indent=4)
                # Check if db row exists. 
                cursor.execute("select count(*) from taxa_external_facts " + 
                               "where (taxon_id = %s) and (provider = %s) ", 
                               (str(taxon_id), str(provider_algaebase_id)))
                result = cursor.fetchone()
                if result[0] == 0: 
                    cursor.execute("insert into taxa_external_facts(taxon_id, provider, facts_json) " + 
                                   "values (%s, %s, %s)", 
                                   (str(taxon_id), str(provider_algaebase_id), jsonstring))
                else:
                    cursor.execute("update taxa_external_facts set facts_json = %s " + 
                                   "where (taxon_id = %s) and (provider = %s) ", 
                                   (jsonstring, str(taxon_id), str(provider_algaebase_id)))
        
        # === OMNIDIA codes ===          
        # Note: This code is used in "External identities", see generate_taxa_facts_external_identities.py.        
        print("")
        print("=== OMNIDIA codes ===")
        # Open file for reading.
        infile = codecs.open(file_name_omnidia_codes, mode = 'r', encoding = file_encoding)    
        # Iterate over rows in file.
        for rowindex, row in enumerate(infile):
            if rowindex == 0: # First row is assumed to be the header row.
                headers = list(map(str.strip, row.split(field_separator)))
                # headers = list(map(unicode, headers))
            else:
                row = list(map(str.strip, row.split(field_separator)))
                # row = list(map(unicode, row))
                # Get taxon_id from name.
                cursor.execute("select id from taxa " + 
                                 "where name = %s", (row[0],) )
                result = cursor.fetchone()
                if result:
                    taxon_id = result[0]
                else:
                    print("Warning: Can't find taxon i taxa. Name: " + row[0])
                    continue # Skip this taxon.
                # Get facts_json from db.
                cursor.execute("select facts_json from taxa_external_facts " + 
                               "where (taxon_id = %s) and (provider = %s) ", 
                               (str(taxon_id), str(provider_omnidia_codes)))
                result = cursor.fetchone()
                if result:
                    # From string to dictionary.
                    factsdict = json.loads(result[0], encoding = 'utf-8')
                    # Add column values to row, if available.
                    for headeritem in headers:
                        row.append(factsdict.get(headeritem, ''))
                else:
                    # Add empty columns.
                    factsdict = {}
                # Update facts.
                for colindex, headeritem in enumerate(headers):
                    if not headeritem in ['Scientific name']:
                        factsdict[headeritem] = row[colindex]
# Note: Description is moved to "External identities", see generate_taxa_facts_external_identities.py.
#                        if headeritem == "OMNIDIA code":
#                            # Add extra info if omidia code.
#                            omnidia = row[colindex]
#                            infostring = str(omnidia) + """<br/>Used by many freshwater diatomists. See <a href="http://omnidia.free.fr/omnidia_english.htm"> <i>http://omnidia.free.fr/omnidia_english.htm</i>.</a>and <a href="http://www.norbaf.net"> <i>http://www.norbaf.net</i>.</a>"""
#                            factsdict[headeritem] = infostring
#                        else:
#                            # Store other as key/value.
#                            factsdict[headeritem] = row[colindex]
                # Convert facts to string.
                jsonstring = json.dumps(factsdict, # encoding = 'utf-8', 
                                     sort_keys=True, indent=4)
                # Check if db row exists. 
                cursor.execute("select count(*) from taxa_external_facts " + 
                               "where (taxon_id = %s) and (provider = %s) ", 
                               (str(taxon_id), str(provider_omnidia_codes)))
                result = cursor.fetchone()
                if result[0] == 0: 
                    cursor.execute("insert into taxa_external_facts(taxon_id, provider, facts_json) " + 
                                   "values (%s, %s, %s)", 
                                   (str(taxon_id), str(provider_omnidia_codes), jsonstring))
                else:
                    cursor.execute("update taxa_external_facts set facts_json = %s " + 
                                   "where (taxon_id = %s) and (provider = %s) ", 
                                   (jsonstring, str(taxon_id), str(provider_omnidia_codes)))






        # === REBECCA codes ===         
        # Note: This code is used in "External identities", see generate_taxa_facts_external_identities.py.        
        print("")
        print("=== REBECCA codes ===")
        # Open file for reading.
        infile = codecs.open(file_name_rebecca_codes, mode = 'r', encoding = file_encoding)    
        # Iterate over rows in file.
        for rowindex, row in enumerate(infile):
            if rowindex == 0: # First row is assumed to be the header row.
                headers = list(map(str.strip, row.split(field_separator)))
                # headers = list(map(unicode, headers))
            else:
                row = list(map(str.strip, row.split(field_separator)))
                # row = list(map(unicode, row))
                # Get taxon_id from name.
                cursor.execute("select id from taxa " + 
                                 "where name = %s", (row[1],) ) # 1 = AcceptedTaxon
                result = cursor.fetchone()
                if result:
                    taxon_id = result[0]
                else:
                    print("Warning: Can't find taxon i taxa. Name: " + row[1]) # 1 = AcceptedTaxon
                    continue # Skip this taxon.
                # Get facts_json from db.
                cursor.execute("select facts_json from taxa_external_facts " + 
                               "where (taxon_id = %s) and (provider = %s) ", 
                               (str(taxon_id), str(provider_rebecca_codes)))
                result = cursor.fetchone()
                if result:
                    # From string to dictionary.
                    factsdict = json.loads(result[0], encoding = 'utf-8')
                    # Add column values to row, if available.
                    for headeritem in headers:
                        row.append(factsdict.get(headeritem, ''))
                else:
                    # Add empty columns.
                    factsdict = {}
                # Update facts.
                factsdict[u'REBECCA code'] = row[0] # 0 = RebeccaID
                # Convert facts to string.
                jsonstring = json.dumps(factsdict, # encoding = 'utf-8', 
                                     sort_keys=True, indent=4)
                # Check if db row exists. 
                cursor.execute("select count(*) from taxa_external_facts " + 
                               "where (taxon_id = %s) and (provider = %s) ", 
                               (str(taxon_id), str(provider_rebecca_codes)))
                result = cursor.fetchone()
                if result[0] == 0: 
                    cursor.execute("insert into taxa_external_facts(taxon_id, provider, facts_json) " + 
                                   "values (%s, %s, %s)", 
                                   (str(taxon_id), str(provider_rebecca_codes), jsonstring))
                else:
                    cursor.execute("update taxa_external_facts set facts_json = %s " + 
                                   "where (taxon_id = %s) and (provider = %s) ", 
                                   (jsonstring, str(taxon_id), str(provider_rebecca_codes)))







        # === IOC-HAB === 
        print("")
        print("=== IOC-HAB ===")
        # Open file for reading.
        infile = codecs.open(file_name_ioc_hab, mode = 'r', encoding = file_encoding)    
        # Iterate over rows in file.
        for rowindex, row in enumerate(infile):
            if rowindex == 0: # First row is assumed to be the header row.
                headers = list(map(str.strip, row.split(field_separator)))
                # headers = list(map(unicode, headers)))
            else:
                row = list(map(str.strip, row.split(field_separator)))
                # row = list(map(unicode, row)))
                # Get taxon_id from name.
                cursor.execute("select id from taxa " + 
                                 "where name = %s", (row[0],) )
                result = cursor.fetchone()
                if result:
                    taxon_id = result[0]
                else:
                    print("Warning: Can't find taxon i taxa. Name: " + row[0])
                    continue # Skip this taxon.
                # Get facts_json from db.
                cursor.execute("select facts_json from taxa_external_facts " + 
                               "where (taxon_id = %s) and (provider = %s) ", 
                               (str(taxon_id), str(provider_ioc_hab)))
                result = cursor.fetchone()
                if result:
                    # From string to dictionary.
                    factsdict = json.loads(result[0], encoding = 'utf-8')
                    # Add column values to row, if available.
                    for headeritem in headers:
                        row.append(factsdict.get(headeritem, ''))
                else:
                    # Add empty columns.
                    factsdict = {}
                # Update facts.
                for colindex, headeritem in enumerate(headers):
                    if not headeritem in ['Scientific name']:
                        factsdict[headeritem] = row[colindex]
                # Convert facts to string.
                jsonstring = json.dumps(factsdict, # encoding = 'utf-8', 
                                     sort_keys=True, indent=4)
                # Check if db row exists. 
                cursor.execute("select count(*) from taxa_external_facts " + 
                               "where (taxon_id = %s) and (provider = %s) ", 
                               (str(taxon_id), str(provider_ioc_hab)))
                result = cursor.fetchone()
                if result[0] == 0: 
                    cursor.execute("insert into taxa_external_facts(taxon_id, provider, facts_json) " + 
                                   "values (%s, %s, %s)", 
                                   (str(taxon_id), str(provider_ioc_hab), jsonstring))
                else:
                    cursor.execute("update taxa_external_facts set facts_json = %s " + 
                                   "where (taxon_id = %s) and (provider = %s) ", 
                                   (jsonstring, str(taxon_id), str(provider_ioc_hab)))
        
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

