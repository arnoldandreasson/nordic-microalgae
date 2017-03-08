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
  
def execute(file_name = '../data_external/peg_bvol2013.txt', 
#            translate_file_name = '../data_external/peg_to_dyntaxa.txt', 
            out_file_name = '../data_prepared/peg_bvol2013.json', 
            infile_encoding = 'cp1252', # 2013.
#            infile_encoding = 'utf16', # 2011, 2012.
            outfile_encoding = 'utf8',
            field_separator = '\t', 
            row_delimiter = '\r\n'):
    """ Prepare import file for HELCOM PEG. """    
    #
    try:
        #
        taxa = []
        header = []
        #
        pegfile = codecs.open(file_name, mode = 'r', encoding = infile_encoding)
        # Iterate over rows in file.
        for rowindex, row in enumerate(pegfile):
            if rowindex == 0: # First row is assumed to be the header row.
                headers = list(map(str.strip, row.split(field_separator)))
                # headers = list(map(unicode, headers))
                # Translate headers.
                for columnname in headers: 
                    header.append(translate_header(columnname.strip()))
            else:
                row = list(map(str.strip, row.split(field_separator)))
                # row = list(map(unicode, row))
                taxonDict = {}
                sizeClassDict = {}
                column = 0
                for value in row:
                    if len(value.strip()) > 0:
                        # Separate columns containing taxon and 
                        # size-class related info.                
                        if is_taxon_related(header, column):
                            taxonDict[header[column]] = value.strip()
                        else:
                            if is_column_numeric(header, column):
                                sizeClassDict[header[column]] = value.strip().replace(',', '.')
                            else:
                                sizeClassDict[header[column]] = value.strip()
                            
#                            if is_column_numeric(header, column):
#                                try:
#                                    value1 = value.strip()
#                                    value2 = value1.replace(',', '.')
#                                    value3 = value2.replace(' ', '')
#                                    float_value = float(value3)
#                                    sizeClassDict[header[column]] = float_value
#                                    if header[column] == 'Size class':  # Covert SIZECLASS to integer.
#                                        sizeClassDict[header[column]] = int(float_value)
#                                except:
#                                    # Use string format if not valid numeric. 
#                                    sizeClassDict[header[column]] = value.strip()
#                                    if value != '-':
#                                        print('ERROR float:' + value + '     ' + value.strip().replace(',', '.').replace(' ', '')) 
#                            else:
#                                sizeClassDict[header[column]] = value.strip()

                    column += 1
                # Check if the taxon-related data already exists.
                taxonExists = False
                for taxon in taxa:
                    if taxon['Species'] == taxonDict['Species']:
                        taxonExists = True
                        taxon['Size classes'].append(sizeClassDict)
                        continue
                # First time. Create the list and add dictionary for 
                # size classes. 
                if taxonExists == False:
                    taxa.append(taxonDict)
                    taxonDict['Size classes'] = []
                    taxonDict['Size classes'].append(sizeClassDict)
        #        
        pegfile.close()
        
        # Open file.
        out = codecs.open(out_file_name, mode = 'w', encoding = outfile_encoding)
        out.write(json.dumps(taxa, # encoding = 'utf8', 
                             sort_keys=True, indent=4))
        #
        out.close()
    #
    except Exception as e:
        print("ERROR: Exception %s" % (e.args[0]))
        print("ERROR: Script will be terminated.")
        raise # DEBUG
        sys.exit(1)
    finally:
        pass


def translate_header(importFileHeader):
    """ Convert import file column names to key names used in dictionary. """        
#        if (importFileHeader == u'Division'): return u'Division'
#        if (importFileHeader == u'Class'): return u'Class'
#        if (importFileHeader == u'Order'): return u'Order'
#        if (importFileHeader == u'Species'): return u'Species'
    if (importFileHeader == u'SFLAG (sp., spp., cf., complex, group)'): return u'SFLAG' # Modified
    if (importFileHeader == u'STAGE (cyst, naked)'): return u'Stage' # Modified
#        if (importFileHeader == u'Author'): return u'Author'
#        if (importFileHeader == u'AphiaID'): return u'AphiaID'
#        if (importFileHeader == u'Trophy'): return u'Trophy'
#        if (importFileHeader == u'Geometric shape'): return u'Geometric shape'
    if (importFileHeader == u'FORMULA'): return u'Formula' # Modified
    if (importFileHeader == u'Size class No'): return u'Size class' # Modified
    if (importFileHeader == u'SizeClassNo'): return u'Size class' # Modified
    if (importFileHeader == u'Nonvalid_SIZCL'): return u'Nonvalid size class' # Modified
    if (importFileHeader == u'Not_accepted'): return u'Not accepted' # Modified
#        if (importFileHeader == u'Unit'): return u'Unit'
    if (importFileHeader == u'size range,'): return u'Size range' # Modified
    if (importFileHeader == u'Length (l1), µm'): return u'Length(l1), µm' # Modified
    if (importFileHeader == u'Length(l1)µm'): return u'Length(l1), µm' # Modified
    if (importFileHeader == u'Length (l2), µm'): return u'Length(l2), µm' # Modified
    if (importFileHeader == u'Length(l2)µm'): return u'Length(l2), µm' # Modified
    if (importFileHeader == u'Width (w), µm'): return u'Width(w), µm' # Modified
    if (importFileHeader == u'Width(w)µm'): return u'Width(w), µm' # Modified
    if (importFileHeader == u'Height (h), µm'): return u'Height(h), µm' # Modified
    if (importFileHeader == u'Height(h)µm'): return u'Height(h), µm' # Modified
    if (importFileHeader == u'Diameter (d1), µm'): return u'Diameter(d1), µm' # Modified
    if (importFileHeader == u'Diameter(d1)µm'): return u'Diameter(d1), µm' # Modified
    if (importFileHeader == u'Diameter (d2), µm'): return u'Diameter(d2), µm' # Modified
    if (importFileHeader == u'Diameter(d2)µm'): return u'Diameter(d2), µm' # Modified
    if (importFileHeader == u'No. of cells/ counting unit'): return u'No. of cells/counting unit' # Modified
    if (importFileHeader == u'Calculated  volume, µm3'): return u'Calculated volume, µm3' # Modified
    if (importFileHeader == u'Calculated  volume µm3'): return u'Calculated volume, µm3' # Modified
    if (importFileHeader == u'Comment'): return u'Comment'
    if (importFileHeader == u'Filament: length of cell (µm)'): return u'Filament: length of cell, µm' # Modified
    if (importFileHeader == u'Calculated Carbon pg/counting unit        (Menden-Deuer & Lessard 2000)'): return u'Calculated Carbon pg/counting unit' # Modified
    if (importFileHeader == u'Calculated Carbon pg/counting unit'): return u'Calculated Carbon pg/counting unit' # Modified
#    if (importFileHeader == u'Comment on Carbon calculation'): return u'Comment on Carbon calculation'
    if (importFileHeader == u'CORRECTION / ADDITION                            2009'): return u'Correction/addition 2009' # Modified
    if (importFileHeader == u'CORRECTION / ADDITION                            2010'): return u'Correction/addition 2010' # Modified
    if (importFileHeader == u'CORRECTION / ADDITION                            2011'): return u'Correction/addition 2011' # Modified
    if (importFileHeader == u'Corrections/Additions 2013'): return u'Corrections/additions 2013' # Modified
    return importFileHeader     
        
def is_taxon_related(header, column):
    """ """        
    if (header[column] == u'Division'): return True
    if (header[column] == u'Class'): return True
    if (header[column] == u'Order'): return True
    if (header[column] == u'Species'): return True
    if (header[column] == u'Author'): return True
    if (header[column] == u'SFLAG'): return True
    if (header[column] == u'Stage'): return True
    if (header[column] == u'Trophy'): return True
    if (header[column] == u'Geometric shape'): return True
    if (header[column] == u'Formula'): return True
    return False # Related to size class.     
    
def is_column_numeric(header, column):
    """ """        
    if (header[column] == u'Size class'): return True
    if (header[column] == u'Length(l1), µm'): return True
    if (header[column] == u'Length(l2), µm'): return True
    if (header[column] == u'Width(w), µm'): return True
    if (header[column] == u'Height(h), µm'): return True
    if (header[column] == u'Diameter(d1), µm'): return True
    if (header[column] == u'Diameter(d2), µm'): return True
    if (header[column] == u'No. of cells/counting unit'): return True
    if (header[column] == u'Calculated volume, µm3'): return True
    if (header[column] == u'Filament: length of cell, µm'): return True
    if (header[column] == u'Calculated Carbon pg/counting unit'): return True
    return False     


# Main.
if __name__ == '__main__':
    execute()
    
