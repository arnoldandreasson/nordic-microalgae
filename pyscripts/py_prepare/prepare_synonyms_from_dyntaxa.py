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
  
#def execute(taxa_file_name = '../data_external/dyntaxa_taxa_xxxxxxxx.txt', 
#            names_file_name = '../data_external/dyntaxa_names_xxxxxxxx.txt', 
def execute(taxa_file_name = '../data_external/dyntaxa_taxa_20110523.txt', 
            names_file_name = '../data_external/dyntaxa_names_20110523.txt', 
            out_file_name = '../data_prepared/synonyms_dyntaxa.txt', 
            infile_encoding = 'utf16',
            outfile_encoding = 'utf16',
            field_separator = '\t', 
            row_delimiter = '\r\n'):
    """ Prepare import file to the main taxa table. 
    
TaxonNameTypeId    Name
0    Scientific
1    Swedish
2    English
3    Danish
4    Norwegian
5    Finnish
6    Icelandic
7    American english
8    NNkod
9    ITIS-name
10    ITIS-number
11    ERMS-name
12    Geman
13    Original name
14    Faeroe
15    Anamorf name
16    GUID   
    
TaxonNameUseTypeId    snamn    definition
0    Godkänd namngivning    Namngivningen är korrekt och används eller har använts tidigare för aktuellt taxon. Vid uttag av synonymer ska detta namn listas.
1    Preliminärt namnförslag    Namnförslag. Namnet ska inte exporteras eller på annat sätt visas utåt.
2    Ogiltig namngivning    Tveksamma synonymer som inte bör visas utåt.
3    Felstavad    Felstavat namn. Bör finnas i databasen eftersom denna felstavning ofta förekommer i listor.
4    Obsrek    Gramatiskt anpassad skrivning anpassad för Artportalerna.    
    
    """    
    #
    try:       
        #
        taxonidtonamedict = {} # Key: Taxon id, value: Scientific name
        #
        # Open taxa file for reading.
        taxafile = codecs.open(taxa_file_name, mode = 'r', encoding = infile_encoding)
        # Iterate over rows in file.
        for rowindex, row in enumerate(taxafile):
            if rowindex == 0: # First row is assumed to be the header row.
                # Header: TaxonId    SortOrder    TaxonTypeId    ScientificName    Author    CommonName    Kingdom    Phylum    Class    Order    Family    Genus    OrganismGroupId    IsSwedishTaxon    IsRedlisted    IsRedlistedSpecies    IsNatura2000Listed    RedlistCategoryId    OrganismGroup    OrganismSubGroupId    OrganismSubGroup    RedlistTaxonCategoryId    RedlistCategory    RedlistCriteria    Landscape
                pass
            else:
                row = list(map(str.strip, row.split(field_separator)))
                # row = list(map(unicode, row))
                #
                scientificname = row[3] # ScientificName
                if scientificname:
                    # Check if already exists.
                    if scientificname in taxonidtonamedict:
                        print("ERROR: Taxon already exists. Name: " + scientificname + ".")
                        continue
                    #
                    taxonidtonamedict[row[0]] = scientificname 
        #
        # Create outdatafile.
        out = codecs.open(out_file_name, mode = 'w', encoding = outfile_encoding)
        # Header, define and print.
        outheader = ['Scientific name', 'Synonym name', 'Synonym author', 'Info json']
        out.write(field_separator.join(outheader) + row_delimiter)
        #            
        # Open name file for reading.
        parentsfile = codecs.open(names_file_name, mode = 'r', encoding = infile_encoding)
        # Iterate over rows in file.
        for rowindex, row in enumerate(parentsfile):
            if rowindex == 0: # First row is assumed to be the header row.
                # Header: TaxonNameId    TaxonId    TaxonNameTypeId    TaxonNameUseTypeId    Name    Author    IsRecommended    UpdatedBy    UpdatedDate    ReferenceId    ReferenceName    ReferenceYear    ReferenceText
                pass
            else:
                row = list(map(str.strip, row.split(field_separator)))
                # row = list(map(unicode, row))
                #
                taxonid = row[1]
                taxonnametypeId = row[2]
                taxonnameusetypeid = row[3]
                name = row[4]
                author = row[5]
                isrecommended = row[6]
                #
                # Skip if names as equal.
                if taxonidtonamedict[taxonid] == name:
                    continue
                # Skip if not ERMS (11) or original name (13).
#                if not (taxonnametypeId in [u'11', u'13']): 
#                # Skip if not original name (13).
                if not (taxonnametypeId in [u'13']): 
                    continue
                # Add info as Json.
                infojson = {}
                infojson['Source'] = 'DynTaxa'
#                if taxonnametypeId == u'11': infojson['Hint'] = 'ERMS name'        
                if taxonnametypeId == u'13': infojson['Hint'] = 'Original name'
                if taxonnameusetypeid == u'3': infojson['Hint'] = 'Misspelled, but commonly used.'
                infojsonstring = json.dumps(infojson, # encoding = 'utf-8', 
                                            sort_keys = True, indent = None)         
                # Create row.
                outrow = [taxonidtonamedict[taxonid], name, author, infojsonstring]
                # Print row.
                out.write(field_separator.join(outrow) + row_delimiter)                
                
        taxafile.close()
        out.close
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
    
