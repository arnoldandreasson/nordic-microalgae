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

import codecs
import string

def execute(species_file_name = '../data_external/b_neat_species.txt', 
            facts_file_name = '../data_external/b_neat_species_data.txt', 
            out_file_name = '../data_prepared/facts_b_neat.txt', 
            infile_encoding = 'utf16', 
            outfile_encoding = 'utf16', 
            field_separator = '\t', 
            row_delimiter = '\r\n'): # For windows usage.
    """ Prepare import file to the taxa_media table. """
    try:
        # Read species file and store taxonid:name in dictionary.
        # Header: id, hierarchy, species_name, author_year, last_modified
        speciesdict = {}
        speciesfile = codecs.open(species_file_name, mode = 'r', encoding = infile_encoding)    
        # Iterate over rows in file.
        for rowindex, row in enumerate(speciesfile):
            if rowindex == 0: # First row is assumed to be the header row.
                headers = map(string.strip, row.split(field_separator))
                headers = map(unicode, headers)
            else:
                # Replace characters interpreted as latin-1.
                row = row.replace(u'Âµ', u'µ') # Âµ  µ
                row = row.replace(u'Ã¤', u'ä') # Ã¤  ä
                row = row.replace(u'Ã¥', u'å') # Ã¥  å
                row = row.replace(u'Ã¦', u'æ') # Ã¦  æ
                row = row.replace(u'Ã«', u'ë') # Ã«  ë 
                row = row.replace(u'Ã¶', u'ö') # Ã¶  ö 
                row = row.replace(u'Ã¼', u'ü') # Ã¼  ü
                row = row.replace(u'Ã˜', u'Ø') # Ã˜. Ø
                row = row.replace(u'Ã¸', u'ø') # Ã¸ ø
                row = row.replace(u'Ã©', u'é') # Ã©  é
                row = row.replace(u'Ã¤', u'ä') # Ã¤ ä
                row = row.replace(u'Ã«', u'ë') # Ã« ë
                row = row.replace(u'Ã¶', u'ö') # Ã¶ ö
                               
                row = map(string.strip, row.split(field_separator))                
                row = map(unicode, row)
                #
                speciesdict[row[0]] = row[2]
        #
        speciesfile.close()
        # Create outdatafile.
        out = codecs.open(out_file_name, mode = 'w', encoding = outfile_encoding)
        # Header, define and print.
        outheader = ['Scientific name', 'Note on taxonomy', 'Morphology', 'Ecology', 'Other remarks',    
                     'Tropic type', 'Harmful', 'Note on harmfulness', 'Substrate', 'Life form',
                     'Width', 'Length', 'Size', 'Resting spore', 'Literature', 'Last modified']
        out.write(field_separator.join(outheader) + row_delimiter)
        # Open image file for reading.
        imagesfile = codecs.open(facts_file_name, mode = 'r', encoding = infile_encoding)    
        # Iterate over rows in file.
        for rowindex, row in enumerate(imagesfile):
            if rowindex == 0: # First row is assumed to be the header row.
                # Header: id    species_id    note_on_taxonomy    morphology    ecology    other_remarks    
                #         tropic_type    harmful    note_on_harmfulness    substrate    life_form    
                #         width    length    size    resting_spore    literature    last_modified
                pass
            else:
                # Replace html tags. 
                row = row.replace(u'<i>', u'<em>')  
                row = row.replace(u'</i>', u'</em>')  
                row = row.replace(u'<b>', u'<strong>')  
                row = row.replace(u'</b>', u'</strong>')  
                # Replace characters interpreted as latin-1.
                row = row.replace(u'Âµ', u'µ') # Âµ  µ
                row = row.replace(u'Ã¤', u'ä') # Ã¤  ä
                row = row.replace(u'Ã¥', u'å') # Ã¥  å
                row = row.replace(u'Ã¦', u'æ') # Ã¦  æ
                row = row.replace(u'Ã«', u'ë') # Ã«  ë 
                row = row.replace(u'Ã¶', u'ö') # Ã¶  ö 
                row = row.replace(u'Ã¼', u'ü') # Ã¼  ü
                row = row.replace(u'Ã˜', u'Ø') # Ã˜. Ø
                row = row.replace(u'Ã¸', u'ø') # Ã¸ ø
                row = row.replace(u'Ã©', u'é') # Ã©  é
                row = row.replace(u'Ã¤', u'ä') # Ã¤ ä
                row = row.replace(u'Ã«', u'ë') # Ã« ë
                row = row.replace(u'Ã¶', u'ö') # Ã¶ ö
                row = row.replace(u'Ã–', u'Ö') # Ã– Ö
                row = row.replace(u'Ã…', u'Å') # Ã… Å
                row = row.replace(u'ÃŸ', u'ß') # ÃŸ ß
                row = row.replace(u'Ãœ', u'Ü') # Ãœ Ü
                row = row.replace(u'Ã¡', u'á') # Ã¡ á 
                row = row.replace(u'Ã­', u'í') # Ã­ í
                row = row.replace(u'Ã³', u'ó') # Ã³ ó
                row = row.replace(u'â€™', u'’') # â€™ ’
                row = row.replace(u'â€œ', u'“') # â€œ “                
                row = row.replace(u'â€', u'”') # â€ ”                
                #
                row = map(string.strip, row.split(field_separator))
                row = map(unicode, row)
                #
                # 0 : id 
                # 18 : last_modified
                scientificname = speciesdict[row[1]] # species_id

                # Create row.
                outrow = [scientificname, row[2].strip('"'), row[3].strip('"'), row[4].strip('"'), row[5].strip('"'), 
                          row[6].strip('"'), row[7].strip('"'), row[8].strip('"'), row[9].strip('"'), row[10].strip('"'), 
                          row[11].strip('"'), row[12].strip('"'), row[13].strip('"'), row[14].strip('"'), row[15].strip('"'), row[16].strip('"')] 
                # Print row.
                out.write(field_separator.join(outrow) + row_delimiter)                
        #            
        imagesfile.close()
        out.close                
    #
#    except Exception, e:
#        print("ERROR: Exception %s" % (e.args[0]))
#        print("ERROR: Script will be terminated.")
#        sys.exit(1)
    finally:
        pass


# Main.
if __name__ == '__main__':
    execute()
