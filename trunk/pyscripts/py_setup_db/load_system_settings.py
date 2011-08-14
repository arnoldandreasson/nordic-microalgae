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

def execute(db_host = 'localhost', 
            db_name = 'nordicmicroalgae', 
            db_user = 'root', 
            db_passwd = ''):
    """ Settings for internal use in the web application Nordic Microalgae. """
    db = None
    cursor = None
    try:
        # Connect to db.
        db = connect_to_db.connect(db_host, db_name, db_user, db_passwd)
        cursor=db.cursor()
        # Remove all rows from table.
        cursor.execute(" delete from system_settings ")
        # Create empty dictionary.
        keydict = {} 
        #
        # Facts:
        # "Field list" contains all used fields stored in json records.
        # Note that more fields can occur due to earlier use, but these fields are currently used. 
        # The "Field list" will be transformed to columns when exporting data to file. 
        #
        keydict["Facts"] = {
            "Field list": [
                "Note on taxonomy",
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
                "Literature",
                "Countries",
                "Geographic areas",
                "Habitats",
                "Trophic types"
            ],
            "Field types": {
                "Note on taxonomy": "text",
                "Morphology": "text",
                "Ecology": "text",
                "Other remarks": "text",
                "Tropic type": "text",
                "Harmful": "text",
                "Note on harmfulness": "text",
                "Substrate": "text",
                "Life form": "text",
                "Width": "text",
                "Length": "text",
                "Size": "text",
                "Resting spore": "text",
                "Literature": "text",
                "Countries": "text list",
                "Geographic areas": "text list",
                "Habitats": "text list",
                "Trophic types": "text list"
            }
        }        
        #
        # Media:
        # "Field list" contains all used fields stored in json records.
        # Note that more fields can occur due to earlier use, but these fields are currently used. 
        # The "Field list" list will be transformed to columns when exporting data to file. 
        #
        keydict["Media"] = {
            "Field list": [
                "Title",
                "Creator", # OLD
# NEW                "Photographer or artist",
                "Institute",
                "Contributor",
                "Caption",
                "Sampling date",
                "Location",
                "Latitude",
                "Longitude",                
                "License",
                "Preservation",
                "Stain",
                "Contrast enhancement",
                "Observation technique",
                "Image galleries"
            ],
            "Field types": {
                "Title": "text",
                "Creator": "text",
                "Institute": "text",
                "Contributor": "text",
                "Caption": "text",
                "Sampling date": "text",
                "Location": "text",
                "Latitude": "text",
                "Longitude": "text",
                "License": "text",
                "Preservation": "text",
                "Stain": "text",
                "Contrast enhancement": "text",
                "Observation technique": "text",
                "Image galleries": "text list"
            }
        }
        #
        # External facts:
        # "Field list" contains all used fields stored in json records.
        # External facts will not be exported to file. They are imported from
        # text files and can not be modified from the web application.
        # Source of data and copyright notice are important to handle properly. 
        #
        keydict["External facts"] = {
            "Provider list": [
                "AlgaeBase",
                "WORMS",
                "IOC",
                "Dyntaxa"
            ],
            "Providers": {
                "AlgaeBase": {
                    "Field list": [
                        "TODO"
                    ],
                    "Source of data": "",
                    "Copyright notice": ""
                },
                "WORMS": {
                    "Field list": [
                        "TODO"
                    ],
                    "Source of data": "",
                    "Copyright notice": ""
                },
                "IOC": {
                    "Field list": [
                        "Harmfulness, IOC"
                    ],
                    "Source of data": "",
                    "Copyright notice": ""
                },
                "Dyntaxa": {
                    "Field list": [
                        "TODO"
                    ],
                    "Source of data": "",
                    "Copyright notice": ""
                }
            }
        }
        #
        # Information to be used when linking to external web pages.
        #
        keydict["External links"] = {
            "Providers": [
                "AlgaeBase",
                "WORMS",
                "IOC",
                "Dyntaxa"
            ],
            "Providers": {
                "AlgaeBase": {
                    "Provider image": "AlgaeBase.jpg",
                    "Home URL": "http://algaebase.org",
                    "Taxon URL": "http://algaebase.org/browse/taxonomy/?id=<replace-id>",
                    "PDF URL": "TODO"
                },
                "WORMS": {
                    "Provider image": "WORMS.jpg",
                    "Home URL": "http://www.marinespecies.org",
                    "Taxon URL": "TODO?id=<replace-id>"
                },
                "IOC": {
                    "Provider image": "IOC-HAB.jpg",
                    "Home URL": "http://www.marinespecies.org/hab/",
                    "Taxon URL": "http://www.marinespecies.org/hab/aphia.php?p=taxdetails&id=<replace-id>"
                },
                "DynTaxa": {
                    "Provider image": "DynTaxa.jpg",
                    "Home URL": "http://www.artdata.slu.se/dyntaxa",
                    "Taxon URL": "TODO?id=<replace-id>"
                }
            }
        }
        #
        #
        #
        keydict["Species view"] = {
            "Ranks": [
                "Species pair", 
                "Species", 
                "Subspecies", 
                "Variety", 
                "Form", 
                "Hybrid" 
            ],
            "Field list": [ # TODO: Fields only?
#                "Component.Images", # TODO: Component or Division or ... this is not the web component available via api.
#                "Component.Classification",
#                "Component.Similar species",
                "Facts.Note on taxonomy",
                "Facts.Tropic type",
                "Facts.Morphology",
                "Facts.Ecology",
                "Facts.Other remarks",
                "Facts.Tropic type",
                "Facts.Harmful",
                "Facts.Note on harmfulness",
                "External Facts.IOC.Harmfulness, IOC",
                "Facts.Substrate",
                "Facts.Life form",
                "Facts.Width",
                "Facts.Length",
                "Facts.Size",
                "Facts.Resting spore",
                "Facts.Literature",
#                "Component.HELCOM PEG"
            ]
        }
        #
        #
        #
        keydict["Taxon view"] = {
            "Ranks": [
                "Domain", 
                "Kingdom", 
                "Subkingdom", 
                "Phylum", 
                "Subphylum", 
                "Superclass", 
                "Class", 
                "Subclass", 
                "Infraclass", 
                "Superorder", 
                "Order", 
                "Suborder", 
                "Infraorder", 
                "Superfamily", 
                "Family", 
                "Subfamily", 
                "Tribe", 
                "Genus", 
                "Subgenus" 
            ],
            "Field list": [
#                "Component.Classification",
#                "Component.Similar species",
                "Facts.Note on taxonomy",
#                "Facts.Tropic type",
#                "Facts.Morphology",
#                "Facts.Ecology",
#                "Facts.Other remarks",
#                "Facts.Tropic type",
#                "External Facts.IOC.Harmful",
#                "External Facts.IOC.Note on harmfulness",
#                "Facts.Substrate",
#                "Facts.Life form",
#                "Facts.Width",
#                "Facts.Length",
#                "Facts.Size",
#                "Facts.Resting spore",
#                "Facts.Literature"
#                "Component.HELCOM PEG"
            ]
        }
        #
        #
        #
        keydict["Image view"] = {
            "Field list": [
                "Media.Title",
                "Media.Creator",
                "Media.Institute",
                "Media.Contributor",
                "Media.Caption",
                "Media.Sampling date",
                "Media.Location",
#                "Component.Geo position",
                "Media.Latitude",
                "Media.Longitude",
                "Media.License",
                "Media.Preservation",
                "Media.Stain",
                "Media.Contrast enhancement",
                "Media.Observation technique",
                "Media.Image galleries"
            ]
        }        
        #
        # Facts view formats:
        # Information needed when viewing data.
        # "Type" is also used when importing/exporting data to distinguish between text fields and lists of texts.
        #
        keydict["Facts view formats"] = {
            "Note on taxonomy": {"Type": "text", "CSS class": "", "Hint": "", "Help": ""},
            "Morphology": {"Type": "text", "CSS class": "", "Hint": "", "Help": ""},
            "Ecology": {"Type": "text", "CSS class": "", "Hint": "", "Help": ""},
            "Other remarks": {"Type": "text", "CSS class": "", "Hint": "", "Help": ""},
            "Tropic type": {"Type": "text", "CSS class": "", "Hint": "", "Help": ""},
            "Harmful": {"Type": "text", "CSS class": "", "Hint": "", "Help": ""},
            "Note on harmfulness": {"Type": "text", "CSS class": "", "Hint": "", "Help": ""},
            "Substrate": {"Type": "text", "CSS class": "", "Hint": "", "Help": ""},
            "Life form": {"Type": "text", "CSS class": "", "Hint": "", "Help": ""},
            "Width": {"Type": "text", "CSS class": "", "Hint": "", "Help": ""},
            "Length": {"Type": "text", "CSS class": "", "Hint": "", "Help": ""},
            "Size": {"Type": "text", "CSS class": "", "Hint": "", "Help": ""},
            "Resting spore": {"Type": "text", "CSS class": "", "Hint": "", "Help": ""},
            "Literature": {"Type": "text", "CSS class": "", "Hint": "", "Help": ""}
            
#            "Country": {"Type": "text list", "CSS class": "", "Hint": "", "Help": ""}
#            "Geographic area": {"Type": "text list", "CSS class": "", "Hint": "", "Help": ""}
#            "Habitat": {"Type": "text list", "CSS class": "", "Hint": "", "Help": ""}
#            "Trophic type": {"Type": "text list", "CSS class": "", "Hint": "", "Help": ""}

        }
        #
        # Media view formats:
        # Information needed when viewing data.
        # "Type" is also used when importing/exporting data to distinguish between text fields and lists of texts.
        #
        keydict["Media view formats"] = {
            "Title": {"Type": "text", "CSS class": "", "Hint": "", "Help": ""},
            "Creator": {"Type": "text", "CSS class": "", "Hint": "", "Help": ""},
            "Institute": {"Type": "text", "CSS class": "", "Hint": "", "Help": ""},
            "Contributor": {"Type": "text", "CSS class": "", "Hint": "", "Help": ""},
            "Caption": {"Type": "text", "CSS class": "", "Hint": "", "Help": ""},
            "Sampling date": {"Type": "date", "CSS class": "", "Hint": "", "Help": ""},
            "Location": {"Type": "text", "CSS class": "", "Hint": "", "Help": ""},
            "Latitude": {"Type": "geo_position_latitude", "CSS class": "", "Hint": "", "Help": ""},
            "Longitude": {"Type": "geo_position_longitude", "CSS class": "", "Hint": "", "Help": ""},
            "License": {"Type": "text", "CSS class": "", "Hint": "", "Help": ""},
            "Preservation": {"Type": "text", "CSS class": "", "Hint": "", "Help": ""},
            "Stain": {"Type": "text", "CSS class": "", "Hint": "", "Help": ""},
            "Contrast enhancement": {"Type": "text", "CSS class": "", "Hint": "", "Help": ""},
            "Observation technique": {"Type": "text", "CSS class": "", "Hint": "", "Help": ""}
        }
        #
        # Facts edit formats:
        # Information needed when editing data.
        #
        keydict["Facts edit formats"] = {
            "Note on taxonomy": {"Type": "textarea", "Description": ""},
            "Morphology": {"Type": "textarea", "Description": ""},
            "Ecology": {"Type": "textarea", "Description": ""},
            "Other remarks": {"Type": "textarea", "Description": ""},
            "Tropic type": {"Type": "textarea", "Description": ""},
            "Harmful": {"Type": "textarea", "Description": ""},
            "Note on harmfulness": {"Type": "textarea", "Description": ""},
            "Substrate": {"Type": "textarea", "Description": ""},
            "Life form": {"Type": "textarea", "Description": ""},
            "Width": {"Type": "textarea", "Description": ""},
            "Length": {"Type": "textarea", "Description": ""},
            "Size": {"Type": "textarea", "Description": ""},
            "Resting spore": {"Type": "textarea", "Description": ""},
            "Literature": {"Type": "textarea", "Description": ""}
        }
        #
        # Media edit formats:
        # Information needed when editing data.
        #
        keydict["Media edit formats"] = {
            "Title": {"Type": "textfield", "Description": "usually the name of the organism"},
            "Creator": {"Type": "textfield", "Description": "photographer or artist"},
            "Institute": {"Type": "textfield", "Description": "usually your institute, university or company"},
            "Contributor": {"Type": "textfield", "Description": ""},
            "Caption": {"Type": "textarea", "Description": "the text describing the illustration"},
            "Sampling date": {"Type": "textfield", "Description": ""},
            "Location": {"Type": "textfield", "Description": "where the water sample/organism was collected"},
            "Latitude": {"Type": "geo_position_latitude", "Description": ""},
            "Longitude": {"Type": "geo_position_longitude", "Description": ""},

            "License": {"Type": "radios", 
                "Options": ["Creative Commons Attribution 3.0 Unported", 
                                "Creative Commons Attribution-NoDerivs 3.0 Unported", 
                                "Creative Commons Attribution-ShareAlike 3.0 Unported", 
                                "Public domain"],
                "Default value": "Creative Commons Attribution 3.0 Unported", 
                "Description": "Please visit <a href='http://creativecommons.org/licenses/'>Creative Commons</a> for more information"},

            "Preservation": {"Type": "checkboxes", 
                "Options": ["Not described", "No preservation", "Lugols iodine", "Formaldehyde", "Glutardialdehyde", "Osmium tetroxide", "Other preservative"],
                "Default value": "Not described", 
                "Description": ""},
            "Stain": {"Type": "checkboxes", 
                "Options": ["Not described", "No stain", "DAPI", "Primulin", "Proflavin", "Calcofluor-Fluorescent brightener", 
                            "Uranyl acetate", "Shadow cast", "Sputter coated", "Other stain"], 
                "Default value": "Not described", 
                "Description": ""},
            "Contrast enhancement": {"Type": "checkboxes", 
                "Options": ["Not described", "No contrast enhancement", "DIC/Nomarski", "Phase contrast", "Acid cleaned and mounted in resin with high refractive index", "Other"], 
                "Default value": "Not described", 
                "Description": ""},
            "Observation technique": {"Type": "checkboxes", 
                "Options": ["Not described", "Light microscopy", "Fluorescence microscopy", "TEM Transmission Electron Micoscopy", 
                                "SEM Scanning Electron Microscopy", "Photography from land Photography from ship Photography from air Satellite remote sensing", 
                                "Other observation technique"], 
                "Default value": "Not described", 
                "Description": ""},
            "Image galleries": {"Type": "checkboxes", 
                "Options": ["HELCOM-PEG", "Skagerrak-Kattegat", "Norwegian Sea", "Freshwater", 
                            "Swedish benthic freshwater diatoms"], 
                "Default value": "", 
                "Description": ""}
        }
        #
        # HELCOM PEG:
        # Display information for HELCOM PEG size classes table.
        #
        keydict["HELCOM PEG"] = {
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
                    ],
                "Geometric shape images": {
                    "sphere": "sphere.jpg",
                    "rotational ellipsoid": "rotational_ellipsoid.jpg",
                    "cylinder": "cylinder.jpg",
                    "chain of spheres": "chain_of_spheres.jpg",
#                    "spheres": "spheres.jpg",                       
                    "flattened ellipsoid": "flattened_ellipsoid.jpg",
                    "cone + half sphere": "cone_plus_half_sphere.jpg",
                    "sphere-20%": "sphere_20percent.jpg",
                    "sphere-10%": "sphere_10percent.jpg",
                    "cone-10%": "cone_10percent.jpg",
                    "2 cones": "2_cones.jpg",
                    "half cone + cut flattened ellipsoid": "half_cone_plus_cut_flattened_ellipsoid.jpg",
                    "half cone": "half_cone.jpg",
                    "monoraphidioid": "monoraphidoid.jpg",
                    "sphere-25%": "sphere_25percent.jpg",
                    "2 cones-30%": "2_cones_30percent.jpg",
                    "flattened ellipsoid - 20%": "flattened_ellipsoid_20percent.jpg",
                    "(cone + half sphere)-20%": "cone_plus_half_sphere_20percent.jpg",
                    "(cone + half sphere)-25%": "cone_plus_half_sphere_25percent.jpg",
#                    "rotational ellipsoid-20%": "rotational ellipsoid.jpg",                       
                    "girdle diameter": "girdle_diameter.jpg",
                    "half sphere": "half_sphere.jpg",
                    "flattened ellipsoid-20%": "flattened_ellipsoid_20percent.jpg",
                    "cone+ half sphere": "cone_plus_half_sphere.jpg",
#                    "truncated cone + half sphere": "truncated cone and half sphere.jpg",                       
                    "cone": "cone.jpg",
                    "rotational ellipsoid x 0.5": "rotational_ellipsoid_x_05.jpg",
                    "oval cylinder": "oval_cylinder.jpg",
                    "prism on triangle base": "prism_on_triangle_base.jpg",
                    "parallelepiped": "parallelepiped.jpg",
                    "half parallelepiped": "half_parallelepiped.jpg",
#                    "cone + half sphere - 40%": "cone  and half sphere.jpg",
                    "parallelepiped-30%": "parallelepiped_30percent.jpg",
                    "parallelepiped-10%": "parallelepiped_10percent.jpg",
                    "Pyramid": "pyramid.jpg",
#                    "parallelepiped/2": "parallelepiped.jpg",
                    "parallelepiped-40%": "parallelepiped_40percent.jpg",
                    "parallelepiped-20%": "parallelepiped_20percent.jpg",
                    "oval cylinder-30%": "oval_cylinder_30percent.jpg",
                    "trapezoid": "trapezoid.jpg",
                    "two truncated cones": "2_truncated_cones.jpg",
                    "parallelepiped-25%": "parallelepiped_25percent.jpg",
                    "half sphere-30%": "half_sphere_30percent.jpg",
                    "Cone+half sphere": "cone_plus_half_sphere.jpg",
#                    "2 spheres * 5/8": "2 sphere.jpg"                    
                    },
                "Source of data": 
                    """
                    Olenina, I., Hajdu, S., Edler, L., Andersson, A., Wasmund, N., Busch, S., Göbel, J., 
                    Gromisz, S., Huseby, S., Huttunen, M., Jaanus, A., Kokkonen, P., Ledaine, I. and Niemkiewicz, 
                    E. 
                    <a href="http://www.helcom.fi/stc/files/Publications/Proceedings/bsep106.pdf">
                    2006 Biovolumes and size-classes of phytoplankton in the Baltic Sea HELCOM Balt.Sea Environ. Proc. No. 106, 144pp. (PDF)</a>,  
                    <br/> 
                    <a href="http://www.ices.dk/env/repfor/index.asp">HELCOM PEG Biovolume</a>,   
                    <a href="http://www.ices.dk/env/repfor/PEG_BVOL2011.xls">PEG_BVOL2011.xls</a>
                    """,
                "Copyright notice": ""
        }
        #
        # Filters:
        # Display information for taxon filters. Filters are divided into groups.
        # - Label: Displayed text.
        # - Defaults: Indicates if the filter should be selected by default.
        # - Filter and value: Used to match values in the db-table taxa_filter_search.
        #                     Example: "where ((filter = 'Illustrated' and value = 'True') and
        #                                      (filter = 'HELCOM PEG' and value = 'True') and
        #                                      ((filter = 'Country' and value = 'Denmark') or
        #                                       (filter = 'Country' and value = 'Finland')) and
        #                                      ((filter = 'Geographic area' and value = 'Baltic sea') or
        #                                       (filter = 'Geographic area' and value = 'Skagerakk')))
        #
        keydict["Filters"] = {
            "Group list": [
                    "Select",
                    "Country (not yet implemented)",
                    "Geographic area (not yet implemented)",
                    "Habitat (not yet implemented)",
                    "Trophic type (not yet implemented)"
            ],
            "Groups": {
                "Select": [
                        {"Label": "Show illustrated only", "Default": "False", "Filter": "Illustrated", "Value": "True"}, 
                        {"Label": "Show HELCOM PEG only", "Default": "False", "Filter": "HELCOM PEG", "Value": "True"}, 
                        {"Label": "Show Swedish benthic freshwater diatoms only", "Default": "False", "Filter": "Benthic FW. diatoms", "Value": "True"}, 
                        {"Label": "Show IOC Harmful algae only", "Default": "False", "Filter": "Harmful", "Value": "True"}
                ],
                "Country (not yet implemented)": [
                        {"Label": "Show all", "Default": "True", "Type": "Master", "Filter": "Country"}, 
                        {"Label": "Denmark", "Default": "False", "Filter": "Country", "Value": "Denmark"}, 
                        {"Label": "Finland", "Default": "False", "Filter": "Country", "Value": "Finland"}, 
                        {"Label": "Norway", "Default": "False", "Filter": "Country", "Value": "Norway"}, 
                        {"Label": "Sweden", "Default": "False", "Filter": "Country", "Value": "Sweden"} 
                 ],
                "Geographic area (not yet implemented)": [
                        {"Label": "Show all", "Default": "True", "Type": "Master", "Filter": "Geographic area"}, 
                        {"Label": "Baltic sea", "Default": "False", "Filter": "Geographic area", "Value": "Baltic sea"},
                        {"Label": "Skagerakk", "Default": "False", "Filter": "Geographic area", "Value": "Skagerakk"},
                        {"Label": "North sea", "Default": "False", "Filter": "Geographic area", "Value": "North sea"},
                        {"Label": "Norwegian sea", "Default": "False", "Filter": "Geographic area", "Value": "Norwegian sea"} 
                ],
                "Habitat (not yet implemented)": [
                        {"Label": "Show all", "Default": "True", "Type": "Master", "Filter": "Habitat"}, 
                        {"Label": "Marine/planktonic", "Default": "False", "Filter": "Habitat", "Value": "Marine/planktonic"}, 
                        {"Label": "Marine/benthic", "Default": "False", "Filter": "Habitat", "Value": "Marine/benthic"}, 
                        {"Label": "Freshwater/planktonic", "Default": "False", "Filter": "Habitat", "Value": "Freshwater/planktonic"}, 
                        {"Label": "Freshwater/benthic", "Default": "False", "Filter": "Habitat", "Value": "Freshwater/benthic"} 
                ],
                "Trophic type (not yet implemented)": [
                        {"Label": "Show all", "Default": "True", "Type": "Master", "Filter": "Trophic type"}, 
                        {"Label": "Photo- or mixotrophic", "Default": "False", "Filter": "Trophic type", "Value": "Photo- or mixotrophic"}, 
                        {"Label": "Heterotrophic", "Default": "False", "Filter": "Trophic type", "Value": "Heterotrophic"} 
                ]
            }
        }
        #
        # Iterate over keydict keys and insert into db table.
        #
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
        if db: db.close()
        if cursor: cursor.close()


# Main.
if __name__ == '__main__':
    execute()

