#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Nordicmicroalgae. http://nordicmicroalgae.org/
# Copyright (c) 2011-2017 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import nordicmicroalgae_settings as settings

from py_import import import_taxa_external_links
from py_import import import_taxa_external_facts
from py_import import import_taxa_helcom_peg
from py_import import import_taxa_synonyms
from py_import import generate_taxa_facts_external_identities
from py_import import import_taxa_external_facts_culture_collections

def execute(db_host = settings.MYSQL_HOST, 
            db_name = settings.MYSQL_DATABASE, 
            db_user = settings.MYSQL_USER, 
            db_passwd = settings.MYSQL_PASSWORD):
    """ """
    #
    print("\n=== Import data: taxa_synonyms, DynTaxa. ===\n")
    import_taxa_synonyms.execute(
            db_host = db_host, db_name = db_name, db_user = db_user, db_passwd = db_passwd, 
            file_name = 'data_import/synonyms_dyntaxa.txt',
            delete_db_content = True # Delete content, first import.
                                 )
    print("\n=== Import data: taxa_synonyms, AlgaeBase. ===\n")
    import_taxa_synonyms.execute(
            db_host = db_host, db_name = db_name, db_user = db_user, db_passwd = db_passwd, 
            file_name = 'data_import/synonyms_algaebase.txt')
    #
    print("\n=== Import data: taxa_external_links, Dyntaxa. ===\n")
    import_taxa_external_links.execute(
            db_host = db_host, db_name = db_name, db_user = db_user, db_passwd = db_passwd, 
            provider = "Dyntaxa",
            link_type = "Taxon URL",
            url_template = "http://dyntaxa.se/Taxon/Info/<replace-id>",
            file_name = 'data_import/external_links_dyntaxa.txt',
            delete_db_content = True # Delete content, first import. 
            )
    print("\n=== Import data: taxa_external_links, AlgaeBase. ===\n")
    import_taxa_external_links.execute(
            db_host = db_host, db_name = db_name, db_user = db_user, db_passwd = db_passwd, 
            provider = "AlgaeBase",
            link_type = "Taxon URL",
            url_template = "http://algaebase.org/search/species/detail/?species_id=<replace-id>",
            file_name = 'data_import/external_links_algaebase.txt'
            )
    print("\n=== Import data: taxa_external_links, IOC. ===\n")
    import_taxa_external_links.execute(
            db_host = db_host, db_name = db_name, db_user = db_user, db_passwd = db_passwd, 
            provider = "IOC",
            link_type = "Taxon URL",
            url_template = "http://www.marinespecies.org/hab/aphia.php?p=taxdetails&id=<replace-id>",
            file_name = 'data_import/external_links_ioc_hab.txt' 
            )

#
# Remove. SCCAP is not an external link list. Should be managed as external facts.
#
#    print("\n=== Import data: taxa_external_links, SCCAP. ===\n")
#    import_taxa_external_links.execute(
#            db_host = db_host, db_name = db_name, db_user = db_user, db_passwd = db_passwd, 
#            provider = "IOC",
#            link_type = "Taxon URL",
#            url_template = "<replace-id>", # Complete url is provided in file.
#            file_encoding = 'cp1252',
#            file_name = 'data_import/external_links_sccap.txt' 
#            )    



    #
    print("\n=== Import data: taxa_external_facts. ===\n")
    import_taxa_external_facts.execute(
            db_host = db_host, db_name = db_name, db_user = db_user, db_passwd = db_passwd,
            provider_dyntaxa_id = "Dyntaxa",
            file_name_dyntaxa_id = 'data_import/taxa_dyntaxa.txt', 
            provider_algaebase_id = "AlgaeBase",
            file_name_algaebase_id = 'data_import/external_links_algaebase.txt', 
            provider_omnidia_codes = "SLU",
            file_name_omnidia_codes = 'data_import/external_facts_omnidia_codes.txt', 
            provider_rebecca_codes = "NIVA",
            file_name_rebecca_codes = 'data_import/external_facts_rebecca_codes.txt', 
            provider_ioc_hab = "IOC",
            file_name_ioc_hab = 'data_import/external_facts_ioc_hab.txt',
            delete_db_content = True # Delete content, first import. 
            )
    #
    print("\n=== Import data: taxa_helcom_peg. ===\n")
    import_taxa_helcom_peg.execute(
            db_host = db_host, db_name = db_name, db_user = db_user, db_passwd = db_passwd, 
            file_name = 'data_import/peg_bvol2013.json',
            translate_file_name = 'data_import/peg_to_dyntaxa.txt'
            )
    #
    print("\n=== Import data: taxa_external_facts_culture_collections. ===\n")
    import_taxa_external_facts_culture_collections.execute(
            db_host = db_host, db_name = db_name, db_user = db_user, db_passwd = db_passwd, 
            file_name_sccap = 'data_import/external_facts_culture_collections_sccap.txt'
            )
    #
    print("\n=== Import data: Generate external identities. ===\n")
    generate_taxa_facts_external_identities.execute(
            db_host = db_host, db_name = db_name, db_user = db_user, db_passwd = db_passwd
            )
    #
    print("\n=== Finished. ===\n")


if __name__ == "__main__":
    execute()

