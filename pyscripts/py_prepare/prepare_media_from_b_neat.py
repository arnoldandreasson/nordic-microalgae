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
import codecs
import string

def execute(species_file_name = '../data_external/b_neat_species.txt', 
            images_file_name = '../data_external/b_neat_images.txt', 
            out_file_name = '../data_prepared/media_b_neat.txt', 
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
                row = map(string.strip, row.split(field_separator))
                row = map(unicode, row)
                #
                speciesdict[row[0]] = row[2]
        speciesfile.close()
        # Create outdatafile.
        out = codecs.open(out_file_name, mode = 'w', encoding = outfile_encoding)
        # Header, define and print.
        outheader = ['Scientific name', 'Media id', 'Media type', 'User name', 'Sort order', 
                     'Location', 'Latitude DD', 'Longitude DD', 'Media format', 'Date', 
                     'Date added', 'Title', 'Description', 'Creator', 'Publisher', 'Contributor', 'Rights']
        out.write(field_separator.join(outheader) + row_delimiter)
        # Open image file for reading.
        imagesfile = codecs.open(images_file_name, mode = 'r', encoding = infile_encoding)    
        # Iterate over rows in file.
        for rowindex, row in enumerate(imagesfile):
            if rowindex == 0: # First row is assumed to be the header row.
                # Header: id, species_id, filename, users_id, sort_order, date_added, location, latitude, longitude, dc_title, dc_creator, dc_description, dc_publisher, dc_contributor, dc_date, dc_type, dc_format, dc_rights, last_modified
                pass
            else:
                row = map(string.strip, row.split(field_separator))
                row = map(unicode, row)
                #
                # 0 : id 
                # 18 : last_modified
                scientificname = speciesdict[row[1]] # 1 : species_id
                mediaid = row[2] # 2 : filename
                mediatype = row[15] # 15 : dc_type
                username = row[3] # 3 : users_id # TODO: Convert to user name.
                sortorder = row[4] # 4 : sort_order 
                location = row[6] # 6 : location 
                latitude = row[7] # 7 : latitude 
                longitude = row[8] # 8 : longitude                 
                mediaformat = row[16] # 16 : dc_format
                date = row[14] # 14 : dc_date 
                date_added = row[5] # 5 : date_added 
                title = row[9] # 9 : dc_title 
                description = row[11] # 11 : dc_description 
                creator = row[10] # 10 : dc_creator 
                publisher = row[12] # 12 : dc_publisher 
                contributor = row[13] # 13 : dc_contributor                  
                rights = row[17] # 17 : dc_rights 
                # Create row.
                outrow = [scientificname, mediaid, mediatype, username, sortorder, 
                          location, latitude, longitude, 
                          mediaformat, date, date_added, 
                          title, description, creator, publisher, contributor, rights] 
                # Print row.
                out.write(field_separator.join(outrow) + row_delimiter)                
        #            
        imagesfile.close()
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
