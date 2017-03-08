#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Nordicmicroalgae. http://nordicmicroalgae.org/
# Copyright (c) 2011-2017 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import nordicmicroalgae_settings as settings

import os
from py_export import export_to_backup

def execute(db_host = settings.MYSQL_HOST, 
            db_name = settings.MYSQL_DATABASE, 
            db_user = settings.MYSQL_USER, 
            db_passwd = settings.MYSQL_PASSWORD, 
            path_to_backup = settings.PATH_TO_BACKUP):
    """ """
    if not os.path.exists(path_to_backup):
        print('Directory created: ' + path_to_backup)
        os.makedirs(path_to_backup)
    #
    print("\n=== Export: taxa_facts_backup, taxa_media_backup, taxa_media_list_backup and change_history_backup. ===\n")
    export_to_backup.execute(db_host, db_name, db_user, db_passwd, 
                             taxa_facts_file_name = os.path.join(path_to_backup, 'backup_taxa_facts.txt'), 
                             taxa_media_file_name = os.path.join(path_to_backup, 'backup_taxa_media.txt'), 
                             taxa_media_list_file_name = os.path.join(path_to_backup, 'backup_taxa_media_list.txt'), 
                             change_history_file_name = os.path.join(path_to_backup, 'backup_change_history.txt')) 
    #
    print("\n=== Finished. ===\n")


if __name__ == "__main__":
    execute()

