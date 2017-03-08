#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Nordicmicroalgae. http://nordicmicroalgae.org/
# Copyright (c) 2011-2017 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import sys
# import string
import codecs
import json
  
def execute(algaebase_file_name = '../data_external/algaebase_species_20120306.txt', 
            ###algaebase_file_name = '../data_external/algaebase_species_20090318.txt', 
            taxa_file_name = '../data_prepared/taxa_dyntaxa.txt', 
            out_external_links_file_name = '../data_prepared/external_links_algaebase.txt', 
            out_synonyms_file_name = '../data_prepared/synonyms_algaebase.txt', 
            infile_encoding = 'utf16',
            outfile_encoding = 'utf16',
            field_separator = '\t', 
            row_delimiter = '\r\n'):
    """ Prepare import file to be used for external links. """    
    #
    try:       
        #
        ab_nametoid_dict = {} # Key: name, value: algaebase id.
        ab_idtoname_dict = {} # Key: algaebase id, value: name.
        ab_synonymnametoid_dict = {} # Key: name, value: algaebase id.
        #
        # Open Algaebase species file for reading.
        algaebasefile = codecs.open(algaebase_file_name, mode = 'r', encoding = infile_encoding)
        # Iterate over rows in file.
        for rowindex, row in enumerate(algaebasefile):
            if rowindex == 0: # First row is assumed to be the header row.
                # Header OLD: Genus    genus_id    id    Accepted_name_serial    Species    Subspecies    Variety    Forma    Current_flag 
                # Header NEW: species.id    genus.Genus    species.Species    species.Subspecies    species.Variety    species.Forma    taxon_authority.taxon_authority    taxon_authority.authority_year    species.Current_flag    species.Record_status    species.Accepted_name_serial    species.genus_id    species.key_Habitat    species.Type_locality
                pass
            else:
                row = list(map(str.strip, row.split(field_separator)))
                # row = list(map(unicode, row))
                 
#               # OLD: 
#                # 0: Genus    
#                # 1: genus_id    
#                # 2: id    
#                # 3: Accepted_name_serial    
#                # 4: Species    
#                # 5: Subspecies    
#                # 6: Variety    
#                # 7: Forma    
#                # 8: Current_flag
#                id = row[2]
#                idforsynonyms = row[3]
#                genus = row[0]
#                species = row[4]
#                subspecies = row[5]
#                variety = row[6]
#                forma = row[7]
#                currentflag = row[8]

                # NEW: 
                # 0: species.id    
                # 1: genus.Genus    
                # 2: species.Species    
                # 3: species.Subspecies    
                # 4: species.Variety    
                # 5: species.Forma    
                # 6: taxon_authority.taxon_authority    
                # 7: taxon_authority.authority_year    
                # 8: species.Current_flag    
                # 9: species.Record_status    
                # 10: species.Accepted_name_serial    
                # 11: species.genus_id    
                # 12: species.key_Habitat    
                # 13: species.Type_locality
                #
                if len(row) < 10:
                    continue
                #
                id = row[0]
                idforsynonyms = row[10] 
                genus = row[1]
                species = row[2]
                subspecies = row[3]
                variety = row[4]
                forma = row[5]
                currentflag = row[8]
                #
                if currentflag in ['U', 'P', 'D']: # U: uncertain taxonomically, P: not checked, D: deprecated.
                    continue
                #
                if currentflag == '': # 
                    print("Current flag is empty: " + id + 
                          " name: " + genus + " " + species + " ssp. " + subspecies + " var. " + variety + " f. " + forma)
                    continue
                #
                name = genus + ' ' + species
                if len(forma) > 0:
                    name = name + ' f. ' + forma
                elif len(variety) > 0:
                    name = name + ' var. ' + variety
                elif len(subspecies) > 0:
                    name = name + ' ssp. ' + subspecies
                #
                #
                if currentflag in ['C', 'c', 'S', 's']: # C: Valid or current, S: Synonym.
                    ab_nametoid_dict[name] = id
                    ab_idtoname_dict[id] = name
                else:
                    print("Error in current flag: " + currentflag)
                
                if currentflag in ['S', 's']: # S: Synonym.
                    ab_synonymnametoid_dict[name] = idforsynonyms
        #
        # Open taxa file.
        infile = codecs.open(taxa_file_name, mode = 'r', encoding = infile_encoding)    
        #
        # Create outdatafiles.
        outlinks = codecs.open(out_external_links_file_name, mode = 'w', encoding = outfile_encoding)
        outsynonyms = codecs.open(out_synonyms_file_name, mode = 'w', encoding = outfile_encoding)
        # Header, define and print.
        outheader = ['Scientific name', 'Algaebase id']
        outlinks.write(field_separator.join(outheader) + row_delimiter)
        outheader = ['Scientific name', 'Synonym name', 'Synonym author', 'Info json']
        outsynonyms.write(field_separator.join(outheader) + row_delimiter)
        # Iterate over rows in file.
        matchcounter = 0
        nomatchcounter = 0
        synonymcounter = 0
        synonymerrorscounter = 0
        highertaxacounter = 0
        
        print(u'Start:')
        
        for rowindex, row in enumerate(infile):
            if rowindex == 0: # First row is assumed to be the header row.
                # Header: Scientific name    Author    Rank    Parent name
                pass
            else:
                row = list(map(str.strip, row.split(field_separator)))
                # row = list(map(unicode, row))
                #
                scientificname = row[0] # ScientificName
                rank = row[2] # Rank
                #
                
                if rank in ['Species', 'Subspecies', 'Variety', 'Form', 'Hybrid']:
                    if scientificname in ab_nametoid_dict:
                        matchcounter += 1
                        algaebaseid = ab_nametoid_dict[scientificname]
                        #
                        # Create and print row.
                        outrow = [scientificname, algaebaseid]
                        outlinks.write(field_separator.join(outrow) + row_delimiter)                
                    else:
                        nomatchcounter += 1
                        print('No match: ' + scientificname)

                    if scientificname in ab_synonymnametoid_dict:
                        try:
                            synonymcounter += 1  
                            algaebaseid = ab_synonymnametoid_dict[scientificname]
                            currentname = ab_idtoname_dict[algaebaseid]                            
                            # Add info as Json.
                            infojson = {}
                            infojson['Source'] = 'AlgaeBase'
                            infojson['Hint'] = 'Valid name'
                            infojsonstring = json.dumps(infojson, # encoding = 'utf-8', 
                                                        sort_keys = True, indent = None)         
                            # Create and print row.
                            outrow = [scientificname, currentname, '', infojsonstring]
                            outsynonyms.write(field_separator.join(outrow) + row_delimiter)                
                        except:
                            synonymerrorscounter += 1
                            print('ERROR. Synonym lookup failed: ' + scientificname)
                    
                else:
                    highertaxacounter += 1
        #
        print('')
        print('Number of matches: ' + str(matchcounter))
        print('Number of no match: ' + str(nomatchcounter))
        print('Number of synonyms: ' + str(synonymcounter))
        print('Number of no synonym errors: ' + str(synonymerrorscounter))
        print('Number of higher taxa: ' + str(highertaxacounter))
        #
        algaebasefile.close()            
        infile.close()
        outlinks.close
        outsynonyms.close
    #
    except Exception as e:
        print("ERROR: Exception %s" % (e.args[0]))
        print("ERROR: Script will be terminated.")
        sys.exit(1)
    finally:
        pass

        
# Main.
if __name__ == '__main__':
    execute()
    
