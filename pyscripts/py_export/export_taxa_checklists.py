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

def execute(db_host = 'localhost', 
            db_name = 'nordicmicroalgae', 
            db_user = 'root', 
            db_passwd = '',
            checklist_short_file_name = '../data_download/nordicmicroalgae_checklist_short.txt', 
            checklist_long_file_name = '../data_download/nordicmicroalgae_checklist.txt', 
            file_encoding = 'utf16',
            field_separator = '\t', 
            row_delimiter = '\r\n'):
    """ Exports facts managed by our own contributors. Format: Text file with tab separated fields. """
    db = None
    cursor = None
    out = None
    try:
        # Connect to db.
        db = mysql.connector.connect(host = db_host, db = db_name, 
                           user = db_user, passwd = db_passwd,
                           use_unicode = True, charset = 'utf8')
        cursor=db.cursor()
        cursortaxa=db.cursor()

        # Open file and write header.
        outshort = codecs.open(checklist_short_file_name, mode = 'w', encoding = file_encoding)
        outlong = codecs.open(checklist_long_file_name, mode = 'w', encoding = file_encoding)
        # Headers.
        outheadershort = ['Class', 'Taxon name', 'Author', 'Rank', 'Trophy', 'IOC-HAB', 'Dyntaxa id']
        outheaderlong = [
##                       'Class', 
                         'Taxon name', 'Author', 'Rank', 'Trophy', 'IOC-HAB', 'Dyntaxa id',
                         'Algaebase id', 'HELCOM-PEG name', 'Synonym names',
                         'Habitat', 'Geographic Area', 'Country', 
                         'Kingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species', 'Subspecies/Form/Variety',
                         'Taxonomic hierarchy']

        # Print header rows.
        outshort.write(field_separator.join(outheadershort) + row_delimiter)
        outlong.write(field_separator.join(outheaderlong) + row_delimiter)
        # Iterate over taxa. 
        cursortaxa.execute("select id, name, author, rank from taxa order by name")
        for taxon_id, scientificname, author, rank in cursortaxa.fetchall():
            # Only use species, and below.
            if rank in ['Species', 'Subspecies', 'Variety', 'Form', 'Hybrid']:
                taxonomicclass = ''
                #scientificname = ''
                #author = ''
                #rank = ''
                trophy = ''
                iochab = ''
                dyntaxaid = ''
                algaebaseid = ''
                helcompegname = ''
                synonymnames = ''
                habitat = ''
                geographicarea = ''
                country = ''
                taxonomichierarchy = ''
                #
                taxonomic_kingdom = '' # Kingdom
                taxonomic_phylum = '' # Phylum
                taxonomic_class = '' # Class (note: duplicated)
                taxonomic_order = '' # Order
                taxonomic_family = '' # Family
                taxonomic_genus = '' # Genus
                taxonomic_species = '' # Species
                taxonomic_subspecies = '' # Subspecies/Form/Variety

                # Get info from table taxa_facts.
                # - trophy
                # - habitat
                # - geographicarea
                # - country
                cursor.execute("select facts_json from taxa_facts " +
                               "where taxon_id = %s", 
                               (taxon_id,))
                result = cursor.fetchone()
                if result:
                    # From string to dictionary.
                    jsondict = json.loads(result[0], encoding = 'utf-8')
                    trophy = jsondict.get('Tropic type', '')
                    habitat = jsondict.get('Habitat', '')
                    geographicarea = jsondict.get('Geographic area', '')
                    country = jsondict.get('Country', '')
                
                # Get info from table taxa_external_facts.
                # - iochab
                # - dyntaxaid
                # - algaebaseid
                
                
                cursor.execute("select count(*) from taxa_external_links " +
                               "where (taxon_id = %s) and (provider = %s)", 
                               (taxon_id, 'IOC'))
                result = cursor.fetchone()
                if result[0] > 0:
                    iochab = 'X' 
                
                # Get Dyntaxa id.
                cursor.execute("select facts_json from taxa_external_facts " +
                               "where (taxon_id = %s) and (provider = %s)", 
                               (taxon_id, u'Dyntaxa'))
                result = cursor.fetchone()
                if result:
                    factsdict = json.loads(result[0], encoding = 'utf-8')
                    dyntaxaid = factsdict.get('Dyntaxa id', '')
                # Get Algaebase id.
                cursor.execute("select facts_json from taxa_external_facts " +
                               "where (taxon_id = %s) and (provider = %s)", 
                               (taxon_id, u'AlgaeBase'))
                result = cursor.fetchone()
                if result:
                    factsdict = json.loads(result[0], encoding = 'utf-8')
                    algaebaseid = factsdict.get('Algaebase id', '')
                
                
                # Get info from table taxa_facts_peg.
                # - helcompegname
                cursor.execute("select facts_json from taxa_helcom_peg " +
                               "where taxon_id = %s", 
                               (taxon_id,))
                result = cursor.fetchone()
                if result:
                    factsdict = json.loads(result[0], encoding = 'utf-8')
                    helcompegname = factsdict.get('Species', '') + ' ' + \
                                    factsdict.get('Author', '')
                
                # Get info from table taxa_synonyms.
                # - synonymnames
                cursor.execute("select synonym_name, synonym_author from taxa_synonyms " +
                               "where taxon_id = %s", 
                               (taxon_id,))
                synonyms = []
                for synonym_name, synonym_author in cursor.fetchall():
                    synonyms.append(synonym_name + ' ' + synonym_author)
                synonymnames = ', '.join(synonyms)

                # Get info from table taxa_navigation.
                # - taxonomichierarchy
                # - etc.
                cursor.execute("select classification from taxa_navigation " +
                               "where taxon_id = %s", 
                               (taxon_id,))
                result = cursor.fetchone()
                try:
                    if result:
                        hierarchy = result[0].split(';')
                        newhierarchy = []
                        for taxonandrank in hierarchy:
                            taxon, rank = taxonandrank.split(':')
                            # New columns.    
                            if rank == 'Kingdom':
                                taxonomic_kingdom = taxon
                            elif rank == 'Phylum':
                                taxonomic_phylum = taxon
                            elif rank == 'Class':
                                taxonomicclass = taxon
                                taxonomic_class = taxon
                            elif rank == 'Order':
                                taxonomic_order = taxon
                            elif rank == 'Family':
                                taxonomic_family = taxon
                            elif rank == 'Genus':
                                taxonomic_genus = taxon
                            elif rank == 'Species':
                                taxonomic_species = taxon
                            elif rank in ['Subspecies', 'Form', 'Variety']:
                                taxonomic_subspecies = taxon
                            # # Change order fromtaxon:rank to rank:taxon.
                            newhierarchy.append(rank + ': ' + taxon)
                    taxonomichierarchy = ', '.join(newhierarchy)
                except:
                    print('Error in taxonomy hierarchy:' + result[0])
                    taxonomichierarchy = ''
                #
                row =  [
                        taxonomicclass, 
                        scientificname, 
                        author, 
                        rank, 
                        trophy, 
                        iochab, 
                        dyntaxaid, 
                       ]
                outshort.write(field_separator.join(row) + row_delimiter)
                #
                row =   [
                        scientificname, 
                        author, 
                        rank, 
                        trophy, 
                        iochab, 
                        dyntaxaid,
                        # 
                        algaebaseid, 
                        helcompegname, 
                        synonymnames, 
                        habitat, 
                        geographicarea, 
                        country, 
                        taxonomic_kingdom,
                        taxonomic_phylum,
                        taxonomic_class,
                        taxonomic_order,
                        taxonomic_family,
                        taxonomic_genus,
                        taxonomic_species,
                        taxonomic_subspecies,
                        taxonomichierarchy
                            ]                
                outlong.write(field_separator.join(row) + row_delimiter)                
            
    except (IOError, OSError):
        print("ERROR: Can't write to text files." + checklist_short_file_name)
        print("ERROR: Script will be terminated.")
        sys.exit(1)
    except mysql.connector.Error as e:
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
