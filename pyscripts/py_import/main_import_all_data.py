#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Nordicmicroalgae. http://nordicmicroalgae.org/
# Copyright (c) 2011-2017 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

from pyscripts.py_import import import_taxa
from pyscripts.py_import import import_taxa_facts
###import import_taxa_facts_drafts
from pyscripts.py_import import import_taxa_external_links
from pyscripts.py_import import import_taxa_external_facts
from pyscripts.py_import import import_taxa_helcom_peg
from pyscripts.py_import import import_taxa_synonyms
from pyscripts.py_import import import_taxa_media
from pyscripts.py_import import generate_taxa_hierarchy_search
from pyscripts.py_import import generate_taxa_navigation
from pyscripts.py_import import generate_taxa_filter_search
from pyscripts.py_import import generate_taxa_media_filter_search

def execute():
    """ Script that creates and populates a test database. """
    #
    print("\n=== Import data: taxa. ===\n")
    import_taxa.execute(file_name = '../data_import/taxa_dyntaxa.txt',
                        delete_db_content = True)
    #
    print("\n=== Import data: taxa_synonyms, DynTaxa. ===\n")
    import_taxa_synonyms.execute(file_name = '../data_import/synonyms_dyntaxa.txt',
                                 delete_db_content = True)
    print("\n=== Import data: taxa_synonyms, AlgaeBase. ===\n")
    import_taxa_synonyms.execute(file_name = '../data_import/synonyms_algaebase.txt')
    #
    print("\n=== Import data: taxa_facts. ===\n")
    import_taxa_facts.execute(file_name = '../data_import/facts_b_neat.txt',
                              delete_db_content = True)
    #
#    print("\n=== Import data: taxa_facts_drafts. ===\n")
###    import_taxa_facts_drafts.execute()
    #
    print("\n=== Import data: taxa_external_links, AlgaeBase. ===\n")
    import_taxa_external_links.execute(
            provider = "AlgaeBase",
            link_type = "Taxon URL",
            url_template = "http://algaebase.org/search/species/detail/?species_id=<replace-id>",
            file_name = '../data_import/external_links_algaebase.txt',
            delete_db_content = True 
            )
    print("\n=== Import data: taxa_external_links, IOC. ===\n")
    import_taxa_external_links.execute(
            provider = "IOC",
            link_type = "Taxon URL",
            url_template = "http://www.marinespecies.org/hab/aphia.php?p=taxdetails&id=<replace-id>",
            file_name = '../data_import/external_links_ioc_hab.txt' 
            )
    #
#    print("\n=== Import data: taxa_external_facts. ===\n")
    import_taxa_external_facts.execute(
#             provider = "IOC",
#             file_name = '../data_import/external_facts_ioc_hab.txt',
            delete_db_content = True 
            )
    #
    print("\n=== Import data: taxa_helcom_peg. ===\n")
    import_taxa_helcom_peg.execute(
            file_name = '../data_import/peg_bvol2013.json',
            translate_file_name = '../data_import/peg_to_dyntaxa.txt'
            )
    #
    print("\n=== Import data: taxa_media. ===\n")
    import_taxa_media.execute(file_name = '../data_import/media_b_neat.txt',
                              delete_db_content = True)
    #
    #
    print("\n=== Generate data: taxa_hierarchy_search. ===\n")
    generate_taxa_hierarchy_search.execute()
    #
    print("\n=== Generate data: taxa_navigation. ===\n")
    generate_taxa_navigation.execute()
    #
    print("\n=== Generate data: taxa_filter_search. ===\n")
    generate_taxa_filter_search.execute()
    #
    print("\n=== Generate data: taxa_media_filter_search. ===\n")
    generate_taxa_media_filter_search.execute()
    #
    print("\n=== Finished. ===\n")


# Main.
if __name__ == '__main__':
    execute()
