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

# import string
import codecs
  
#def execute(dyntaxa_file_name = '../data_external/dyntaxa_taxa_xxxxxxxx.txt', 
#            algaebase_file_name = '../data_external/algaebase_xxxxxxxx.txt', 
def execute(dyntaxa_file_name = '../data_external/dyntaxa_taxa_20110523.txt', 
            algaebase_file_name = '../data_misc/AlgaeBaseGenera_11_April_2011_utf16.txt', 
            out_file_name = '../data_misc/match_genus_classifications_dyntaxa_vs_algaebase.txt', 
            infile_encoding = 'utf16',
            outfile_encoding = 'utf16',
            field_separator = '\t', 
            row_delimiter = '\r\n'):
    """ Compares classification for genus between Dyntaxa and Algaebase.  """    
    #
    taxa = []
    nametotaxonrow = {}
    #
    outheader = ['Dyntaxa id', 'Algaebase id', 'Name', 'Rank',
                 'DT Kingdom', 'DT Phylum', 'DT Class', 'DT Order', 'DT Family', 'DT Genus',
                 'AB Kingdom', 'AB Phylum', 'AB Class', 'AB Order', 'AB Family', 'AB Genus',
                 'Compare Kingdom', 'Compare Phylum', 'Compare Class', 'Compare Order', 'Compare Family', 'Compare Genus',
                 'Algaebase hierarchy']
    #
    # Load ranks.
    rankdict = create_rankdict()
    #
    # Open Dyntaxa file for reading.
    dyntaxafile = codecs.open(dyntaxa_file_name, mode = 'r', encoding = infile_encoding)
    # Iterate over rows in file.
    for rowindex, row in enumerate(dyntaxafile):
        if rowindex == 0: # First row is assumed to be the header row.
            # Header: TaxonId    SortOrder    TaxonTypeId    ScientificName    Author    CommonName    Kingdom    Phylum    Class    Order    Family    Genus    OrganismGroupId    IsSwedishTaxon    IsRedlisted    IsRedlistedSpecies    IsNatura2000Listed    RedlistCategoryId    OrganismGroup    OrganismSubGroupId    OrganismSubGroup    RedlistTaxonCategoryId    RedlistCategory    RedlistCriteria    Landscape
            pass
        else:
            row = list(map(str.strip, row.split(field_separator)))
            # row = list(map(unicode, row))
            #
            id = row[0] # ScientificName
            name = row[3] # ScientificName
            rank = rankdict.get(row[2], None) # TaxonTypeId
            if rank == 'Genus':
                # Create row for printing.
                taxonrow = [id, '', name, rank,
                         row[6], row[7], row[8], row[9], row[10], row[11], 
                         '', '', '', '', '', '', 
                         '', '', '', '', '', '',
                         '']
                # Check if already exists.
                if name in nametotaxonrow:
                    print("ERROR: Dyntaxa taxon already exists. Name: " + name + ".")
                    continue
                #
                taxa.append(taxonrow)
                nametotaxonrow[name] = taxonrow 
    dyntaxafile.close()
    #            
    # Open Algaebase file for reading.
    algaebasefile = codecs.open(algaebase_file_name, mode = 'r', encoding = infile_encoding)
    # Iterate over rows in file.
    for rowindex, row in enumerate(algaebasefile):
        if rowindex == 0: # First row is assumed to be the header row.
            # Header: genus    id    Genus_authority    Genus_Year    hierarchy
            pass
        else:
            row = list(map(str.strip, row.split(field_separator)))
            # row = list(map(unicode, row))
            #
            name = row[0]
            id = row[1]
            hierarchy = row[4]
            #
            if name in nametotaxonrow:
                # Update row for printing.
                taxonrow = nametotaxonrow[name]
                #
                # Parse hierarchy.
                # Example: e: Eukaryota, k: Plantae, sk: Biliphyta, p: Rhodophyta, sp: Eurhodophytina, 
                #          c: Florideophyceae, sc: Rhodymeniophycidae, o: Gigartinales, f: Gigartinaceae, 
                #          g: Chondrus
                hierdict = {}
                hierlist = list(map(str.strip, row[4].split(',')))
                for item in hierlist:
                    if not ':' in item:
                        continue 
                    key, value = item.split(':')
                    hierdict[key.strip()] = value.strip()
                #
                taxonrow[1] = id
                taxonrow[22] = hierarchy
                #
                taxonrow[10] = hierdict.get('k', '') # 'AB Kingdom'
                taxonrow[11] = hierdict.get('p', '') # 'AB Phylum'
                taxonrow[12] = hierdict.get('c', '') # 'AB Class'
                taxonrow[13] = hierdict.get('o', '') # 'AB Order'
                taxonrow[14] = hierdict.get('f', '') # 'AB Family'
                taxonrow[15] = hierdict.get('g', '') # 'AB Genus'
                #
                # Compare Dyntaxa and Algaebase.
                if taxonrow[4] == taxonrow[10]: # 'Compare Kingdom'
                    taxonrow[16] = '='
                else:
                    taxonrow[16] = '<>'
                if taxonrow[5] == taxonrow[11]: # 'Compare Phylum'
                    taxonrow[17] = '='
                else:
                    taxonrow[17] = '<>'
                if taxonrow[6] == taxonrow[12]: # 'Compare Class'
                    taxonrow[18] = '='
                else:
                    taxonrow[18] = '<>'
                if taxonrow[7] == taxonrow[13]: # 'Compare Order'
                    taxonrow[19] = '='
                else:
                    taxonrow[19] = '<>'
                if taxonrow[8] == taxonrow[14]: # 'Compare Family'
                    taxonrow[20] = '='
                else:
                    taxonrow[20] = '<>'
                if taxonrow[9] == taxonrow[15]: # 'Compare Genus'
                    taxonrow[21] = '='
                else:
                    taxonrow[21] = '<>'
            else:
#                    print("ERROR: Algebase genus not found in Dyntaxa: %s" % (name))
                pass
    algaebasefile.close()
    #
    # Create and write to outfile.
    outfile = codecs.open(out_file_name, mode = 'w', encoding = outfile_encoding)
    # Header, define and print.
    outfile.write(field_separator.join(outheader) + row_delimiter)
    # Iterate over rows in taxa dictionary.
    for rowindex, row in enumerate(taxa):
        #
        outfile.write(field_separator.join(row) + row_delimiter)                
    #            
    outfile.close

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
