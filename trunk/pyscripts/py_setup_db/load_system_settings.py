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

import MySQLdb as mysql
import sys
import connect_to_db
import json

def execute():
    """ Settings for internal use in the web application Nordic Microalgae. """
    try:
        # Connect to db.
        db = connect_to_db.connect()
        cursor=db.cursor()
        # Remove all rows from table.
        cursor.execute(" delete from system_settings ")
        #
        keydict = {} 
        #
        keydict['External links'] = \
            {
                "AlgaeBase": {
                    "Taxon url": "http://algaebase.org/browse/taxonomy/?id=<replace-id>",
                    "Home url": "http://algaebase.org"
                }
            }
        keydict['Facts'] = \
            {
                "Headers": [
                    "Morphology",
                    "Ecology",
                    "Other remarks",
                    "Tropic type",
                    "Harmful",
                    "Note on harmfulness",
                    "Substrate",
                    "Life form",
                    "Width",
                    "Length",
                    "Size",
                    "Resting spore",
                    "Literature"
                ]
            }
        keydict['External facts'] = \
            {
                "AlgaeBase": {
                    "Headers": [
                        "Test"
                    ]
                }
            }
        keydict['HELCOM PEG'] = \
            {
                "Species fields": [
                    "Species",
                    "Author",
                    "Division",
                    "Class",
                    "Order",
                    "SFLAG",
                    "Stage",
                    "Trophy",
                    "Geometric shape",
                    "Formula"
                    ],
                "Size class fields": [
                    "Size class",
                    "Unit",
                    "Size range",
                    "Length(l1), µm",
                    "Length(l2), µm",
                    "Width(w), µm",
                    "Height(h), µm",
                    "Diameter(d1), µm",
                    "Diameter(d2), µm",
                    "No. of cells/counting unit",
                    "Calculated volume, µm3",
                    "Comment",
                    "Filament: length of cell (µm)",
                    "Calculated Carbon pg/counting unit",
                    "Comment on Carbon calculation" #,
#                    "Correction/addition 2009",
#                    "Correction/addition 2010"
                    ]
            }
#"Species"
#"Author"
#"Division"
#"Class"
#"Order"
#"SFLAG"
#"Stage"
#"Trophy"
#"Geometric shape"
#"Formula"
#
#"Size class"
#"Unit"
#"Size range"
#"Length(l1), µm"
#"Length(l2), µm"
#"Width(w), µm"
#"Height(h), µm"
#"Diameter(d1), µm"
#"Diameter(d2), µm"
#"No. of cells/counting unit"
#"Calculated volume, µm3"
#"Comment"
#"Filament: length of cell, µm"
#"Calculated Carbon pg/counting unit"
#"Comment on Carbon calculation"
#"Correction/addition 2009"
#"Correction/addition 2010"
            
        keydict['Filters'] = \
            {
                "Groups": [
                        "Select",
                        "Country",
                        "Geographic area",
                        "Habitat",
                        "Trophic type"
                ],
                "Select": [
                        {"Label": "Show illustrated only", "Default": "False"}, 
                        {"Label": "Show HELCOM PEG only", "Default": "False"}, 
                        {"Label": "Show Harmful algae only", "Default": "False"}
                ],
                "Country": [
                        {"Label": "Denmark", "Default": "True"}, 
                        {"Label": "Finland", "Default": "True"}, 
                        {"Label": "Norway", "Default": "True"}, 
                        {"Label": "Sweden", "Default": "True"} 
                 ],
                "Geographic area": [
                        {"Label": "Baltic sea", "Default": "True"},
                        {"Label": "Skagerakk", "Default": "True"},
                        {"Label": "North sea", "Default": "True"},
                        {"Label": "Norwegian sea", "Default": "True"}, 
                        {"Label": "Greenland sea", "Default": "True"} 
                ],
                "Habitat": [
                        {"Label": "Marine/planktonic", "Default": "True"}, 
                        {"Label": "Marine/benthic", "Default": "True"}, 
                        {"Label": "Freshwater/planktonic", "Default": "True"}, 
                        {"Label": "Freshwater/benthic", "Default": "True"} 
                ],
                "Trophic type": [
                        {"Label": "Photo- or mixotrophic", "Default": "True"}, 
                        {"Label": "Heterotrophic", "Default": "True"} 
                ],
            }
        #
        # Iterate over keydict keys and insert into db table.
        for key in keydict.keys():
            jsonstring = json.dumps(keydict[key], encoding = 'utf-8', 
                                 sort_keys=True, indent=4)
            cursor.execute("insert into system_settings(settings_key, settings_value) values (%s, %s)", 
                           (unicode(key), unicode(jsonstring)))
    #
    except mysql.Error, e:
        print("ERROR: MySQL %d: %s" % (e.args[0], e.args[1]))
        print("ERROR: Script will be terminated.")
        sys.exit(1)
    finally:
        if cursor: cursor.close()
        if db: db.close()


# Main.
if __name__ == '__main__':
    execute()

