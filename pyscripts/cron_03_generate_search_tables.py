#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Nordicmicroalgae. http://nordicmicroalgae.org/
# Copyright (c) 2011-2017 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import nordicmicroalgae_settings as settings

from py_import import generate_taxa_filter_search
from py_import import generate_taxa_media_filter_search

def execute(db_host = settings.MYSQL_HOST, 
            db_name = settings.MYSQL_DATABASE, 
            db_user = settings.MYSQL_USER, 
            db_passwd = settings.MYSQL_PASSWORD):
    """ """
    #
    print("\n=== Generate taxa filter search. ===\n")
    generate_taxa_filter_search.execute(db_host, db_name, db_user, db_passwd)
    #
    print("\n=== Generate taxa media filter search. ===\n")
    generate_taxa_media_filter_search.execute(db_host, db_name, db_user, db_passwd)
    #
    print("\n=== Finished. ===\n")


if __name__ == "__main__":
    execute()

