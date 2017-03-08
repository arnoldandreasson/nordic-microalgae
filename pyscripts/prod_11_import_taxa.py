#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Nordicmicroalgae. http://nordicmicroalgae.org/
# Copyright (c) 2011-2017 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import nordicmicroalgae_settings as settings

from py_import import import_taxa
from py_setup_db import load_taxa_ranks
from py_import import generate_taxa_hierarchy_search
from py_import import generate_taxa_navigation

def execute(db_host = settings.MYSQL_HOST, 
            db_name = settings.MYSQL_DATABASE, 
            db_user = settings.MYSQL_USER, 
            db_passwd = settings.MYSQL_PASSWORD):
    """ """
    #
    print("\n=== Load taxa ranks. ===\n")
    load_taxa_ranks.execute(db_host, db_name, db_user, db_passwd)
    #
    print("\n=== Import taxa. ===\n")
    import_taxa.execute(db_host, db_name, db_user, db_passwd,
                        file_name = 'data_import/taxa_dyntaxa.txt',
                        delete_db_content = True)
    #
    print("\n=== Generate taxa hierarchy search. ===\n")
    generate_taxa_hierarchy_search.execute(db_host, db_name, db_user, db_passwd)
    #    
    print("\n=== Generate taxa navigation. ===\n")
    generate_taxa_navigation.execute(db_host, db_name, db_user, db_passwd) 
    #
    print("\n=== Finished. ===\n")


if __name__ == "__main__":
    execute()

