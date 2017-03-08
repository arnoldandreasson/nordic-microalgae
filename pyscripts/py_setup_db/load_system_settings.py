#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Nordicmicroalgae. http://nordicmicroalgae.org/
# Copyright (c) 2011-2017 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import mysql.connector
import sys
import json

def execute(db_host = 'localhost', 
            db_name = 'nordicmicroalgae', 
            db_user = 'root', 
            db_passwd = ''):
    """ 
    Settings for internal use in the web application Nordic Microalgae. 
    All data is located in this Python script.
    """
    db = None
    cursor = None
    try:
        # Connect to db.
        db = mysql.connector.connect(
                        host = db_host, db = db_name, 
                        user = db_user, passwd = db_passwd,
                        use_unicode = True, charset = 'utf8')
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
                "Photographer/artist",
                "Copyright holder",
                "Copyright stamp",
                "Institute",
                "Contributing organisation",
                "Contributor",
                "Caption",
                "Sampling date",
                "Geographic area",
                "Location",
                "Latitude, degree",
                "Latitude, minute",
                "Longitude, degree",                
                "Longitude, minute",                
                "License",
                "Preservation",
                "Stain",
                "Contrast enhancement",
                "Technique",
                "Image galleries"
            ],
            "Field types": {
                "Title": "text",
                "Photographer/artist": "text",
                "Copyright holder": "text",
                "Copyright stamp": "text",
                "Institute": "text",
                "Contributing organisation": "text",
                "Contributor": "text",
                "Caption": "text",
                "Sampling date": "text",
                "Geographic area": "text",
                "Location": "text",
                "Latitude, degree": "text",
                "Latitude, minute": "text",
                "Longitude, degree": "text",
                "Longitude, minute": "text",
                "License": "text",
                "Preservation": "text list",
                "Stain": "text list",
                "Contrast enhancement": "text list",
                "Technique": "text list",
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
                "Dyntaxa",
                "SLU",
                "Generated facts"
            ],
            "Providers": {
                "AlgaeBase": {
                    "Field list": [
                        "Algaebase id"
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
                        "Dyntaxa id"
                    ],
                    "Source of data": "",
                    "Copyright notice": ""
                },
                "SLU": {
                    "Field list": [
                        "OMNIDIA code"
                    ],
                    "Source of data": "",
                    "Copyright notice": ""
                },
                "Generated facts": {
                    "Field list": [
                        "IDs in other systems",
                        "Culture collections"
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
                "External Facts.Generated facts.IDs in other systems",
                "Facts.Note on taxonomy",
                "Facts.Tropic type",
                "Facts.Morphology",
                "Facts.Ecology",
                "Facts.Other remarks",
                "Facts.Harmful",
                "Facts.Note on harmfulness",
                "External Facts.IOC.Harmfulness, IOC",
#                "External Facts.SLU.OMNIDIA code",
                "Facts.Substrate",
                "Facts.Life form",
                "Facts.Width",
                "Facts.Length",
                "Facts.Size",
                "Facts.Resting spore",
                "External Facts.Generated facts.Culture collections",
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
        keydict["Media view"] = {
            "Field list": [
                "Title",
                "Photographer/artist",
                "Copyright holder",
                "Copyright stamp",
                "Institute",
                "Contributing organisation",
                "Contributor",
                "Caption",
                "Sampling date",
                "Geographic area",
                "Location",
                "Latitude, degree",
                "Latitude, minute",
                "Longitude, degree",
                "Longitude, minute",
                "License",
                "Technique",
                "Preservation",
                "Contrast enhancement",
                "Stain",
                "Image galleries"
            ]
        }
        #
        #
        #
        keydict["Mediaset view"] = {
            "Field list": [
                "Title",
                "Date added",
                "Photographer/artist",
                "Contributing organisation"
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
            "Photographer/artist": {"Type": "text", "CSS class": "", "Hint": "", "Help": ""},
            "Copyright holder": {"Type": "text", "CSS class": "", "Hint": "", "Help": ""},
            "Copyright stamp": {"Type": "text", "CSS class": "", "Hint": "", "Help": ""},
            "Institute": {"Type": "text", "CSS class": "", "Hint": "", "Help": ""},
            "Contributing organisation": {"Type": "text", "CSS class": "", "Hint": "", "Help": ""},
            "Contributor": {"Type": "text", "CSS class": "", "Hint": "", "Help": ""},
            "Caption": {"Type": "text", "CSS class": "", "Hint": "", "Help": ""},
            "Sampling date": {"Type": "date", "CSS class": "", "Hint": "", "Help": ""},
            "Geographic area": {"Type": "text", "CSS class": "", "Hint": "", "Help": ""},
            "Location": {"Type": "text", "CSS class": "", "Hint": "", "Help": ""},
            "Latitude, degree": {"Type": "geo_position_latitude", "CSS class": "", "Hint": "", "Help": ""},
            "Latitude, minute": {"Type": "geo_position_latitude", "CSS class": "", "Hint": "", "Help": ""},
            "Longitude, degree": {"Type": "geo_position_longitude", "CSS class": "", "Hint": "", "Help": ""},
            "Longitude, minute": {"Type": "geo_position_longitude", "CSS class": "", "Hint": "", "Help": ""},
            "License": {"Type": "text", "CSS class": "", "Hint": "", "Help": ""},
            "Preservation": {"Type": "text", "CSS class": "", "Hint": "", "Help": ""},
            "Stain": {"Type": "text", "CSS class": "", "Hint": "", "Help": ""},
            "Contrast enhancement": {"Type": "text", "CSS class": "", "Hint": "", "Help": ""},
            "Technique": {"Type": "text", "CSS class": "", "Hint": "", "Help": ""}
        }
        #
        # Facts edit formats:
        # Information needed when editing data.
        #
        keydict["Facts edit formats"] = {
            "Note on taxonomy": {"Type": "textarea", "Description": "", "Visual": "True"},
            "Morphology": {"Type": "textarea", "Description": "", "Visual": "True"},
            "Ecology": {"Type": "textarea", "Description": "", "Visual": "True"},
            "Other remarks": {"Type": "textarea", "Description": "", "Visual": "True"},
            "Tropic type": {"Type": "textarea", "Description": ""},
            "Harmful": {"Type": "textarea", "Description": ""},
            "Note on harmfulness": {"Type": "textarea", "Description": "", "Visual": "True"},
            "Substrate": {"Type": "textarea", "Description": ""},
            "Life form": {"Type": "textarea", "Description": ""},
            "Width": {"Type": "textarea", "Description": ""},
            "Length": {"Type": "textarea", "Description": ""},
            "Size": {"Type": "textarea", "Description": ""},
            "Resting spore": {"Type": "textarea", "Description": ""},
            "Literature": {"Type": "textarea", "Description": "", "Visual": "True"}
        }
        #
        # Media edit formats:
        # Information needed when editing data.
        #
        keydict["Media edit formats"] = {
            "Title": {"Type": "textfield", "Description": "Usually the name of the organism.", "Required": "True"}, # Mandatory.
            "Photographer/artist": {"Type": "textfield", "Description": "Photographer or artist.", "Required": "True"}, # Mandatory.
            "Copyright holder": {"Type": "textfield", "Description": ""},
            "Copyright stamp": {"Type": "textfield", "Description": "This text will be used for the stamping images with the name of the copyright holder. Leave empty if no stamp is needed. Fill in the name of the Copyright holder if you want a stamp. Keep the text as short as possible."},
            "Institute": {"Type": "textfield", "Description": "Usually your institute, university or company."},
            "Contributing organisation": {"Type": "textfield", "Description": "This could be e.g. HELCOM-PEG, the name of an institute or a company. Maximum number of characters is 28. The text is shown e.g. under the author name in Galleries and Latest images."},
            "Contributor": {"Type": "textfield", "Description": "", "Required": "True"}, # Mandatory.
            "Caption": {"Type": "textarea", "Description": "The text describing the illustration. Caption is not saved in template.", "Visual": "True"},
            "Sampling date": {"Type": "textfield", "Description": ""},
            "Geographic area": {"Type": "select", "Description": "Choose the area where the organism was collected.", 
                "Options": ["", 
                            "Baltic Sea - Bothnian Bay",
                            "Baltic Sea - The Quark",
                            "Baltic Sea - Bothnian Sea",
                            "Baltic Sea - Archipelago Sea",
                            "Baltic Sea - Åland Sea",
                            "Baltic Sea - Gulf of Finland",
                            "Baltic Sea - Gulf of Riga",
                            "Baltic Sea - Northern Baltic proper",
                            "Baltic Sea - Central Baltic proper",
                            "Baltic Sea - Southern Baltic proper",
                            "Baltic Sea - The Gulf of Gdansk",
                            "Baltic Sea - Arkona Basin",
                            "Baltic Sea - Mecklenburger Bight",
                            "Baltic Sea - Kiel Bay",
                            "Baltic Sea - S Little Belt",
                            "Baltic Sea - S Great Belt",
                            "Baltic Sea - S part of the Sound",
                            "Kattegat - off shore",
                            "Kattegat - Swedish coast",
                            "Kattegat - Danish coast",
                            "Kattegat - N Little Belt",
                            "Kattegat - N Great Belt",
                            "Kattegat - N part of the Sound",
                            "Limfjorden",
                            "Skagerrak - off shore",
                            "Skagerrak - Swedish coast",
                            "Skagerrak - Oslo fjord",
                            "Skagerrak - Norwegian coast",
                            "North Sea - off shore",
                            "North Sea- Norwegian coast",
                            "North Sea - Danish coast",
                            "Norwegian Sea - off shore",
                            "Norwegian Sea - coast",
                            "Barent Sea - off shore",
                            "Barent Sea - Norwegian coast",
                            "Barent Sea - Svalbard",
                            
                            "Iceland - NE",
                            "Iceland - SW",

                            "Greenland Sea - off shore",
                            "Greenland Sea - Greenland coast",
                            "Arctic ocean - off shore",
                            "Arctic ocean - Svalbard coast",
                            "Arctic ocean - Greenland coast",
                            "Atlantic ocean - off shore",
                            "Lake - Denmark",
                            "Lake - Estonia",
                            "Lake - Finland",
                            "Lake - Greenland",
                            "Lake - Iceland",
                            "Lake - Germany",
                            "Lake - Latvia",
                            "Lake - Lithuania",
                            "Lake - Norway",
                            "Lake - Poland",
                            "Lake - Russia",
                            "Lake - Sweden",
                            "River - Denmark",
                            "River - Estonia",
                            "River - Finland",
                            "River - Greenland",
                            "River - Iceland",
                            "River - Germany",
                            "River - Latvia",
                            "River - Lithuania",
                            "River - Norway",
                            "River - Poland",
                            "River - Russia",
                            "River - Sweden"],
                "Default value": ""},            
            "Location": {"Type": "textfield", "Description": "Where the water sample/organism was collected."},
            
            "Latitude, degree": {"Type": "geo_position_latitude", "Description": "Example: 57 (use - for West of Greenwhich)."},
            "Latitude, minute": {"Type": "geo_position_latitude", "Description": "Example: 59.2"},
            "Longitude, degree": {"Type": "geo_position_longitude", "Description": "Example: 10 (use - for Southern hemisphere)."},
            "Longitude, minute": {"Type": "geo_position_longitude", "Description": "Example 59.5"},

            "License": {"Type": "radios", 
                "Options": ["Creative Commons Attribution 3.0 Unported", 
                                "Creative Commons Attribution-NoDerivs 3.0 Unported", 
                                "Creative Commons Attribution-ShareAlike 3.0 Unported", 
                                "Public domain"],
                "Default value": "Creative Commons Attribution-NoDerivs 3.0 Unported", 
                "Description": """                
'Creative Commons Attribution-NoDerivs 3.0 Unported' is recommended. This license is the most restrictive of our the licenses, 
only allowing others to download your works and share them with others as long as they credit you, 
but they can’t change them in any way. 
Please visit <a href='http://creativecommons.org/licenses/'>Creative Commons</a> for more information."""},

            "Preservation": {"Type": "checkboxes", 
                "Options": ["Not described", "No preservation", "Lugols iodine", "Formaldehyde", "Glutardialdehyde", "Osmium tetroxide", "Other preservative"],
                "Default value": "", 
                "Description": ""},
            "Stain": {"Type": "checkboxes", 
                "Options": ["Not described", "No stain", "DAPI", "Primulin", "Proflavin", "Calcofluor-Fluorescent brightener", 
                            "Uranyl acetate", "Shadow cast", "Sputter coated", "Other stain"], 
                "Default value": "", 
                "Description": ""},
            "Contrast enhancement": {"Type": "checkboxes", 
                "Options": ["Not described", "No contrast enhancement", "DIC/Nomarski", "Phase contrast", "Acid cleaned and mounted in resin with high refractive index", "Other"], 
                "Default value": "", 
                "Description": ""},
            "Technique": {"Type": "checkboxes", 
                "Options": ["Not described",
                            "Drawing", "Painting",  
                            "Light microscopy", "Fluorescence microscopy", "TEM Transmission Electron Micoscopy", 
                            "SEM Scanning Electron Microscopy", "Photography from land", "Photography from ship", 
                            "Photography from air", "Satellite remote sensing", 
                            "Other technique"], 
                "Default value": "", 
                "Description": ""},
            "Image galleries": {"Type": "checkboxes", 
                "Options": ["HELCOM-PEG", 
                            "NOMP",
                            "Kuylenstierna", 
                            "Skagerrak-Kattegat", 
                            "Norwegian Sea", 
                            "Marine Research Institute - Iceland", 
                            "Freshwater", 
                            "Swedish benthic freshwater diatoms", 
                            "Diatom resting stages", "Dinoflagellate cysts", "Other resting stages"], 
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
                    <a href="http://helcom.fi/Lists/Publications/BSEP106.pdf" target="_blank">
                    2006 Biovolumes and size-classes of phytoplankton in the Baltic Sea HELCOM Balt.Sea Environ. Proc. No. 106, 144pp. (PDF)</a>,  
                    <br/> 
                    <a href="http://www.ices.dk/marine-data/vocabularies/Documents/PEG_BVOL.zip" target="_blank">PEG_BVOL.zip</a>
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
                    "For contributors"
                    # Remove until implemented:
                    #"Country (not yet implemented)",
                    #"Geographic area (not yet implemented)",
                    #"Habitat (not yet implemented)",
                    #"Trophic type (not yet implemented)"
            ],
            "Groups": {
                "Select": [
                        {"Label": "Illustrated only", "Default": "False", "Filter": "Illustrated", "Value": "True"}, 
                        {"Label": "HELCOM-PEG species", "Default": "False", "Filter": "HELCOM PEG", "Value": "True"}, 
                        {"Label": "IOC Harmful algae only", "Default": "False", "Filter": "Harmful", "Value": "True"}
                ],
                "For contributors": [
                        {"Label": "Not illustrated", "Default": "False", "Filter": "Not illustrated", "Value": "True"}, 
                ]
#                "Country (not yet implemented)": [
#                        {"Label": "Show all", "Default": "True", "Type": "Master", "Filter": "Country"}, 
#                        {"Label": "Denmark", "Default": "False", "Filter": "Country", "Value": "Denmark"}, 
#                        {"Label": "Finland", "Default": "False", "Filter": "Country", "Value": "Finland"}, 
#                        {"Label": "Norway", "Default": "False", "Filter": "Country", "Value": "Norway"}, 
#                        {"Label": "Sweden", "Default": "False", "Filter": "Country", "Value": "Sweden"} 
#                 ],
#                "Geographic area (not yet implemented)": [
#                        {"Label": "Show all", "Default": "True", "Type": "Master", "Filter": "Geographic area"}, 
#                        {"Label": "Baltic sea", "Default": "False", "Filter": "Geographic area", "Value": "Baltic sea"},
#                        {"Label": "Skagerrak", "Default": "False", "Filter": "Geographic area", "Value": "Skagerrak"},
#                        {"Label": "North sea", "Default": "False", "Filter": "Geographic area", "Value": "North sea"},
#                        {"Label": "Norwegian sea", "Default": "False", "Filter": "Geographic area", "Value": "Norwegian sea"} 
#                ],
#                "Habitat (not yet implemented)": [
#                        {"Label": "Show all", "Default": "True", "Type": "Master", "Filter": "Habitat"}, 
#                        {"Label": "Marine/planktonic", "Default": "False", "Filter": "Habitat", "Value": "Marine/planktonic"}, 
#                        {"Label": "Marine/benthic", "Default": "False", "Filter": "Habitat", "Value": "Marine/benthic"}, 
#                        {"Label": "Freshwater/planktonic", "Default": "False", "Filter": "Habitat", "Value": "Freshwater/planktonic"}, 
#                        {"Label": "Freshwater/benthic", "Default": "False", "Filter": "Habitat", "Value": "Freshwater/benthic"} 
#                ],
#                "Trophic type (not yet implemented)": [
#                        {"Label": "Show all", "Default": "True", "Type": "Master", "Filter": "Trophic type"}, 
#                        {"Label": "Photo- or mixotrophic", "Default": "False", "Filter": "Trophic type", "Value": "Photo- or mixotrophic"}, 
#                        {"Label": "Heterotrophic", "Default": "False", "Filter": "Trophic type", "Value": "Heterotrophic"} 
#                ]
            }
        }
        #
        # Filter groups:
        # Display information for taxon groups.
        # - Label: Displayed text.
        # - Defaults: Indicates if the group should be selected by default.
        # - Color: Displayed background color.
        # - Value: Used to match values in the db-table taxa_filter_search.
        #                     Example: "where ((filter = 'Group' and value = 'Cyanobacteria')
        #
        keydict["Filter groups"] = {
            "Group list": [
                    "All",
                    "Cyanobacteria",
                    "Diatoms",
                    "Dinoflagellates",
                    "Other microalgae",
                    "Ciliates",
                    "Other protozoa"
            ],
            "Groups": {
                "All": {"Label": "All", "Default": "True", "Filter": "Group", "Color": "ffffff", "Value": "All", "Hint": "All species, subspecies, forma and varieties"},
                "Cyanobacteria": {"Label": "Cyanobacteria", "Default": "False", "Filter": "Group", "Color": "bcffff", "Value": "Cyanobacteria", "Hint": "Cyanophyta"},
                "Diatoms": {"Label": "Diatoms", "Default": "False", "Filter": "Group", "Color": "ffe7bc", "Value": "Diatoms", "Hint": "Bacillariophyceae"},
                "Dinoflagellates": {"Label": "Dinoflagellates", "Default": "False", "Filter": "Group", "Color": "e7c7c7", "Value": "Dinoflagellates", "Hint": "Dinophyceae (auto, mixo- and heterotrophic)"},
                "Other microalgae": {"Label": "Other microalgae", "Default": "False", "Filter": "Group", "Color": "bcddbc", "Value": "Other microalgae", "Hint": "Includes many autotrophic flagellates etc."},
                "Ciliates": {"Label": "Ciliates", "Default": "False", "Filter": "Group", "Color": "bcbcff", "Value": "Ciliates", "Hint": "Includes tintinnids and naked ciliates"},
                "Other protozoa": {"Label": "Other protozoa", "Default": "False", "Filter": "Group", "Color": "ffffbc", "Value": "Other protozoa", "Hint": "Includes choanoflagellates, other heterotrophic flagellates, foraminifera, radiolarians etc."}            
            }
        }
        #
        # Iterate over keydict keys and insert into db table.
        #
        for key in keydict.keys():
            jsonstring = json.dumps(keydict[key], # encoding = 'utf-8', 
                                 sort_keys=True, indent=4)
            cursor.execute("insert into system_settings(settings_key, settings_value) values (%s, %s)", 
                           (str(key), str(jsonstring)))
    #
    except mysql.connector.Error as e:
        print("ERROR: MySQL %d: %s" % (e.args[0], e.args[1]))
        print("ERROR: Script will be terminated.")
        sys.exit(1)
    finally:
        if db: db.close()
        if cursor: cursor.close()


# To be used when this module is launched directly from the command line.
import getopt
def main():
    # Parse command line options.
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:d:u:p:", ["host=", "database=", "user=", "password="])
    except getopt.error as msg:
        print(msg)
        sys.exit(2)
    # Create dictionary with named arguments.
    params = {}
    for opt, arg in opts:
        if opt in ("-h", "--host"):
            params['db_host'] = arg
        elif opt in ("-d", "--database"):
            params['db_name'] = arg
        elif opt in ("-u", "--user"):
            params['db_user'] = arg
        elif opt in ("-p", "--password"):
            params['db_passwd'] = arg
    # Execute with parameter list.
    execute(**params) # The "two stars" prefix converts the dictionary into named arguments. 

if __name__ == "__main__":
    main()

