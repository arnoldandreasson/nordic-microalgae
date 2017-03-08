#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Nordicmicroalgae. http://nordicmicroalgae.org/
# Copyright (c) 2011-2017 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).


import nordicmicroalgae_settings as settings

import os
from py_export import export_taxa
from py_export import export_taxa_facts
from py_export import export_taxa_media
from py_export import export_taxa_checklists


def execute(db_host = settings.MYSQL_HOST, 
            db_name = settings.MYSQL_DATABASE, 
            db_user = settings.MYSQL_USER, 
            db_passwd = settings.MYSQL_PASSWORD, 
            path_to_downloads = settings.PATH_TO_DOWNLOADS):
    """ """
    if not os.path.exists(path_to_downloads):
        print('Directory created: ' + path_to_downloads)
        os.makedirs(path_to_downloads)
    #
    print("\n=== Export: taxa. ===\n")
    export_taxa.execute(db_host, db_name, db_user, db_passwd,
                        file_name = os.path.join(path_to_downloads, 'taxa.txt'))
    #
    print("\n=== Export: taxa_facts. ===\n")
    export_taxa_facts.execute(db_host, db_name, db_user, db_passwd, 
                              file_name = os.path.join(path_to_downloads, 'taxa_facts.txt'))
    #
    print("\n=== Export: taxa_media. ===\n")
    export_taxa_media.execute(db_host, db_name, db_user, db_passwd, 
                              file_name = os.path.join(path_to_downloads, 'taxa_media.txt'))
    #    
    print("\n=== Export: nordicmicroalgae_checklist and nordicmicroalgae_checklist_short. ===\n")
    export_taxa_checklists.execute(db_host, db_name, db_user, db_passwd, 
                                   checklist_short_file_name = os.path.join(path_to_downloads, 'nordicmicroalgae_checklist_short.txt'), 
                                   checklist_long_file_name = os.path.join(path_to_downloads, 'nordicmicroalgae_checklist.txt')) 
    #
    print("\n=== Finished. ===\n")


if __name__ == "__main__":
    execute()

