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

import import_taxa
import import_taxa_facts
import import_taxa_facts_drafts
import import_taxa_external_links
import import_taxa_external_facts
import import_taxa_helcom_peg
import import_taxa_synonyms
import import_taxa_media
import generate_taxa_hierarchy_search
import generate_taxa_navigation
import generate_taxa_filter_search

def execute():
    """ Script that creates and populates a test database. """
    #
    print("\n=== Import data: taxa. ===\n")
    import_taxa.execute(file_name = '../data_import/taxa_dyntaxa.txt')
    #
    print("\n=== Import data: taxa_synonyms, DynTaxa. ===\n")
    import_taxa_synonyms.execute(file_name = '../data_import/synonyms_dyntaxa.txt')
    print("\n=== Import data: taxa_synonyms, AlgaeBase. ===\n")
    import_taxa_synonyms.execute(file_name = '../data_import/synonyms_algaebase.txt')
    #
    print("\n=== Import data: taxa_facts. ===\n")
    import_taxa_facts.execute(file_name = '../data_import/facts_b_neat.txt')
    #
#    print("\n=== Import data: taxa_facts_drafts. ===\n")
###    import_taxa_facts_drafts.execute()
    #
    print("\n=== Import data: taxa_external_links, AlgaeBase. ===\n")
    import_taxa_external_links.execute(
            provider = "AlgaeBase",
            link_type = "Taxon URL",
            url_template = "http://algaebase.org/search/species/detail/?species_id=<replace-id>",
            file_name = '../data_import/external_links_algaebase.txt' 
            )
    print("\n=== Import data: taxa_external_links, IOC-HAB. ===\n")
    import_taxa_external_links.execute(
            provider = "IOC-HAB",
            link_type = "Taxon URL",
            url_template = "http://www.marinespecies.org/hab/aphia.php?p=taxdetails&id=<replace-id>",
            file_name = '../data_import/external_links_ioc_hab.txt' 
            )
    #
#    print("\n=== Import data: taxa_external_facts. ===\n")
    import_taxa_external_facts.execute(
            provider = "IOC-HAB",
            file_name = '../data_import/external_facts_ioc_hab.txt', 
            )
    #
    print("\n=== Import data: taxa_helcom_peg. ===\n")
    import_taxa_helcom_peg.execute(
            file_name = '../data_import/peg_bvol2010.json',
            translate_file_name = '../data_import/peg_to_dyntaxa.txt'
            )
    #
    print("\n=== Import data: taxa_media. ===\n")
    import_taxa_media.execute(file_name = '../data_import/media_b_neat.txt')
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
    print("\n=== Finished. ===\n")


# Main.
if __name__ == '__main__':
    execute()
