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

import sys
import string
import codecs
  
def execute(algaebase_file_name = '../data_external/algaebase_species_20090318.txt', 
            taxa_file_name = '../data_import/taxa.txt', 
            out_file_name = '../data_prepared/algaebase_external_links.txt', 
            infile_encoding = 'utf16',
            outfile_encoding = 'utf16',
            field_separator = '\t', 
            row_delimiter = '\r\n'):
    """ Prepare import file to the main taxa table. """    
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
                # Header: Genus    genus_id    id    Accepted_name_serial    Species    Subspecies    Variety    Forma    Current_flag 
                pass
            else:
                row = map(string.strip, row.split(field_separator))
                row = map(unicode, row)
                #
                id = row[2]
                idforsynonyms = row[3]
                genus = row[0]
                species = row[4]
                subspecies = row[5]
                variety = row[6]
                forma = row[7]
                currentflag = row[8]
                #
                #
                if currentflag in ['U', 'P']: # U: uncertain taxonomically, P: not checked
                    continue
                #
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
                if currentflag in ['C', 'c']: # C: Valid or current.
                    ab_nametoid_dict[name] = id
                    ab_idtoname_dict[id] = name
                elif currentflag in ['S', 's']: # S: Synonym.
                    ab_synonymnametoid_dict[name] = idforsynonyms
                else:
                    print("Error in current flag: " + currentflag)
                
        #
        # Open taxa file.
        infile = codecs.open(taxa_file_name, mode = 'r', encoding = infile_encoding)    
        #
        # Create outdatafile.
        out = codecs.open(out_file_name, mode = 'w', encoding = outfile_encoding)
        # Header, define and print.
        outheader = ['Scientific name', 'Algaebase id', 'Synonym', 'Algaebase current name']
        out.write(field_separator.join(outheader) + row_delimiter)
        # Iterate over rows in file.
        matchcounter = 0
        nomatchcounter = 0
        synonymcounter = 0
        synonymerrorscounter = 0
        highertaxacounter = 0
        for rowindex, row in enumerate(infile):
            if rowindex == 0: # First row is assumed to be the header row.
                # Header: Scientific name    Author    Rank    Parent name
                pass
            else:
                row = map(string.strip, row.split(field_separator))
                row = map(unicode, row)
                #
                scientificname = row[0] # ScientificName
                rank = row[2] # Rank
                #
                
                if rank in ['Species', 'Subspecies', 'Variety', 'Form', 'Hybrid']:
                    if scientificname in ab_nametoid_dict:
                        matchcounter += 1
                        algaebaseid = ab_nametoid_dict[scientificname]
                        #
                        # Create row.
                        outrow = [scientificname, algaebaseid, '', '']
                        # Print row.
                        out.write(field_separator.join(outrow) + row_delimiter)                

                    elif scientificname in ab_synonymnametoid_dict:
                        try:
                            synonymcounter += 1  
                            synonym = 'S'
                            algaebaseid = ab_synonymnametoid_dict[scientificname]
                            currentname = ab_idtoname_dict[algaebaseid]
                            # Create row.
                            outrow = [scientificname, algaebaseid, synonym, currentname]
                            # Print row.
                            out.write(field_separator.join(outrow) + row_delimiter)                
                        except:
                            synonymerrorscounter += 1
                            print('ERROR. Synonym lookup failed: ' + scientificname)
                    
                    else:
                        nomatchcounter += 1
                        print('No match: ' + scientificname)
                else:
                    highertaxacounter += 1
        #
        print('')
        print('Number of matches: ' + unicode(matchcounter))
        print('Number of no match: ' + unicode(nomatchcounter))
        print('Number of no synonyms: ' + unicode(synonymcounter))
        print('Number of no synonym errors: ' + unicode(synonymerrorscounter))
        print('Number of higher taxa: ' + unicode(highertaxacounter))
        #
        algaebasefile.close()            
        infile.close()
        out.close
    #
    except Exception, e:
        print("ERROR: Exception %s" % (e.args[0]))
        print("ERROR: Script will be terminated.")
        sys.exit(1)
    finally:
        pass

        
# Main.
if __name__ == '__main__':
    execute()
    
