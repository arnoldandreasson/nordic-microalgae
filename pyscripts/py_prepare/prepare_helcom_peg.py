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
import json
  
def execute(file_name = '../data_external/peg_bvol2010.txt', 
#            translate_file_name = '../data_external/peg_to_dyntaxa.txt', 
            out_file_name = '../data_prepared/peg_bvol2010.json', 
            infile_encoding = 'utf16',
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
                headers = map(string.strip, row.split(field_separator))
                headers = map(unicode, headers)
                # Translate headers.
                for columnname in headers: 
                    header.append(translate_header(columnname.strip()))
            else:
                row = map(string.strip, row.split(field_separator))
                row = map(unicode, row)
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
        out.write(json.dumps(taxa, encoding = 'utf8', sort_keys=True, indent=4))
        #
        out.close()
    #
    except Exception, e:
        print("ERROR: Exception %s" % (e.args[0]))
        print("ERROR: Script will be terminated.")
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
#        if (importFileHeader == u'Trophy'): return u'Trophy'
#        if (importFileHeader == u'Geometric shape'): return u'Geometric shape'
    if (importFileHeader == u'FORMULA'): return u'Formula' # Modified
    if (importFileHeader == u'Size class No'): return u'Size class' # Modified
#        if (importFileHeader == u'Unit'): return u'Unit'
    if (importFileHeader == u'size range,'): return u'Size range' # Modified
    if (importFileHeader == u'Length (l1), µm'): return u'Length(l1), µm' # Modified
    if (importFileHeader == u'Length (l2), µm'): return u'Length(l2), µm' # Modified
    if (importFileHeader == u'Width (w), µm'): return u'Width(w), µm' # Modified
    if (importFileHeader == u'Height (h), µm'): return u'Height(h), µm' # Modified
    if (importFileHeader == u'Diameter (d1), µm'): return u'Diameter(d1), µm' # Modified
    if (importFileHeader == u'Diameter (d2), µm'): return u'Diameter(d2), µm' # Modified
    if (importFileHeader == u'No. of cells/ counting unit'): return u'No. of cells/counting unit' # Modified
    if (importFileHeader == u'Calculated  volume, µm3'): return u'Calculated volume, µm3' # Modified
    if (importFileHeader == u'Comment'): return u'Comment'
    if (importFileHeader == u'Filament: length of cell (µm)'): return u'Filament: length of cell, µm' # Modified
    if (importFileHeader == u'Calculated Carbon pg/counting unit        (Menden-Deuer & Lessard 2000)'): return u'Calculated Carbon pg/counting unit' # Modified
#    if (importFileHeader == u'Comment on Carbon calculation'): return u'Comment on Carbon calculation'
    if (importFileHeader == u'CORRECTION / ADDITION                            2009'): return u'Correction/addition 2009' # Modified
    if (importFileHeader == u'CORRECTION / ADDITION                            2010'): return u'Correction/addition 2010' # Modified
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
    
