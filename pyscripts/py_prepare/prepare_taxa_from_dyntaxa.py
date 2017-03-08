#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Nordicmicroalgae. http://nordicmicroalgae.org/
# Copyright (c) 2011-2017 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import sys
# import string
import codecs
  
def execute(taxa_file_name = '../data_external/dyntaxa_taxa_20110523.txt', 
            names_file_name = '../data_external/dyntaxa_names_20110523.txt', 
            parents_file_name = '../data_external/dyntaxa_parents_20110523.txt', 
#def execute(taxa_file_name = '../data_external/dyntaxa_taxa_xxxxxxxx.txt', 
#            names_file_name = '../data_external/dyntaxa_names_xxxxxxxx.txt', 
#            parents_file_name = '../data_external/dyntaxa_parents_xxxxxxxx.txt', 
            out_file_name = '../data_prepared/taxa_dyntaxa.txt', 
            infile_encoding = 'utf16',
            outfile_encoding = 'utf16',
            field_separator = '\t', 
            row_delimiter = '\r\n'):
    """ Prepare import file to the main taxa table. """    
    #
    try:       
        #
        taxonidtonamedict = {} # Key: Taxon id, value: Scientific name
        taxonidtoparentiddict = {} # Key: Taxon id, value: Parent id
        #
        # Load ranks.
        rankdict = create_rankdict()
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
                author = row[4] # Author
                rank = rankdict.get(row[2], None) # TaxonTypeId
                if scientificname:
                    # Check if already exists.
                    if scientificname in taxonidtonamedict:
                        print("ERROR: Taxon already exists. Name: " + scientificname + ".")
                        continue
                    #
                    taxonidtonamedict[row[0]] = scientificname 
        #            
        # Open parents file for reading.
        parentsfile = codecs.open(parents_file_name, mode = 'r', encoding = infile_encoding)
        # Iterate over rows in file.
        for rowindex, row in enumerate(parentsfile):
            if rowindex == 0: # First row is assumed to be the header row.
                # Header: ParentTaxonId    ChildTaxonId    ParentChildRelationId
                pass
            else:
                row = list(map(str.strip, row.split(field_separator)))
                # row = list(map(unicode, row))
                #
                if row[2] == '2': # ParentChildRelationId.
                    if (row[0] in taxonidtonamedict) and \
                       (row[1] in taxonidtonamedict):
                        taxonidtoparentiddict[row[1]] = row[0]
                    else:
                        print("ERROR: Invalid taxonid: %s, %s" % (row[0], row[1]))
        parentsfile.close()
        #
        # Create outdatafile.
        out = codecs.open(out_file_name, mode = 'w', encoding = outfile_encoding)
        # Header, define and print.
        outheader = ['Scientific name', 'Author', 'Rank', 'Parent name', 'Dyntaxa id']
        out.write(field_separator.join(outheader) + row_delimiter)
        # Restart taxafile and iterate.
        taxafile.seek(0)            
        # Iterate over rows in file.
        for rowindex, row in enumerate(taxafile):
            if rowindex == 0: # First row is assumed to be the header row.
                # Header: TaxonId    SortOrder    TaxonTypeId    ScientificName    Author    CommonName    Kingdom    Phylum    Class    Order    Family    Genus    OrganismGroupId    IsSwedishTaxon    IsRedlisted    IsRedlistedSpecies    IsNatura2000Listed    RedlistCategoryId    OrganismGroup    OrganismSubGroupId    OrganismSubGroup    RedlistTaxonCategoryId    RedlistCategory    RedlistCriteria    Landscape
                pass
            else:
                row = list(map(str.strip, row.split(field_separator)))
                # row = list(map(unicode, row))
                #
                taxonid = row[0]
                scientificname = row[3] # ScientificName
                author = row[4] # Author
                rank = rankdict.get(row[2], None) # TaxonTypeId
                parentname = ''
                #
                if taxonid in taxonidtoparentiddict:
                    parentid = taxonidtoparentiddict[taxonid]
                    if parentid in taxonidtonamedict:
                        parentname = taxonidtonamedict[parentid]
                    else:
                        print("ERROR: Not in taxonidtonamedict: " + parentid)
                else:
                    if rank != 'Kingdom':
                        print("ERROR: No parent found: " + rank + "  " + taxonid + "  " + scientificname)
                # Create row.
                outrow = [scientificname, author, rank, parentname, taxonid]
                # Print row.
                out.write(field_separator.join(outrow) + row_delimiter)                
        #            
        taxafile.close()
        out.close
    #
    except Exception as e:
        print("ERROR: Exception %s" % (e.args[0]))
        print("ERROR: Script will be terminated.")
        sys.exit(1)
    finally:
        pass

def create_rankdict():
    """ Rank-list as defined by Dyntaxa. """
    #
    rankdict = {        
        "1": "Kingdom",
        "2": "Phylum",
        "3": "Subphylum",
        "4": "Superclass",
        "5": "Class",
        "6": "Subclass",
        "7": "Superorder",
        "8": "Order",
        "9": "Suborder",
        "10": "Superfamily",
        "11": "Family",
        "12": "Subfamily",
        "13": "Tribe",
        "14": "Genus",
        "15": "Subgenus",
        "16": "Section",
        "17": "Species",
        "18": "Subspecies",
        "19": "Variety",
        "20": "Form",
        "21": "Hybrid",
        "22": "Cultural variety",
        "23": "Population",
        "24": "Group of families",
        "25": "Infraclass",
        "26": "Parvclass",
        "27": "Sensu lato",
        "28": "Species pair",
        "-2": "Group",
        "-1": "Group of lichens",
        "29": "Infraorder",
        "30": "Avdelning",
        "31": "Underavdelning"}
    #
    return rankdict        

        
# Main.
if __name__ == '__main__':
    execute()
    
