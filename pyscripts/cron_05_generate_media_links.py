#!/usr/bin/python3
# -*- coding:utf-8 -*-
#
# Project: Nordicmicroalgae. http://nordicmicroalgae.org/
# Copyright (c) 2011-2017 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import nordicmicroalgae_settings as settings
import mysql.connector
import sys
import os

def execute(db_host = settings.MYSQL_HOST, 
            db_name = settings.MYSQL_DATABASE, 
            db_user = settings.MYSQL_USER, 
            db_passwd = settings.MYSQL_PASSWORD,
            original_path = settings.MEDIA_PATH_TO_ORIGINAL_FILES,
            large_path  = settings.MEDIA_PATH_TO_STANDARD_FILES,
            small_path   = settings.MEDIA_PATH_TO_THUMBNAIL_FILES):
    """ Generate symbolic links for '<Scientific name>.jpg' to the 'default' image.
        Note: For linux systems only.  """
    
    db = None
    cursor = None
    try:
        # Connect to db.
        db = mysql.connector.connect(host = db_host, db = db_name, 
                           user = db_user, passwd = db_passwd,
                           use_unicode = True, charset = 'utf8')
        cursor=db.cursor()        
        
        # Create dictionary for translations from taxon_id to taxon_name.
        taxonidtoname = {}
        cursor.execute("select id, name from taxa")
        for taxon_id, taxon_name in cursor.fetchall():
            taxonidtoname[taxon_id] = taxon_name

        # TAXA MEDIA LIST.    
        cursor.execute("select taxon_id, media_list from taxa_media_list")
        for taxon_id, media_list in cursor.fetchall():
            if taxon_id in taxonidtoname:
                taxonname = taxonidtoname[taxon_id]
                if not taxonname:
                    continue
                
                default_image_file = ''
                image_files = media_list.split(';')
                if len(image_files) > 0:
                    name, ext = os.path.splitext(image_files[0])
                    default_image_file = name + '.jpg'
                
                # Original size files.
                generate_symbolic_link(taxonname, default_image_file, original_path)                
                # Large size files.
                generate_symbolic_link(taxonname, default_image_file, large_path)
                # small size files.
                generate_symbolic_link(taxonname, default_image_file, small_path)
    #
    except mysql.connector.Error as e:
        print("ERROR: MySQL %d: %s" % (e.args[0], e.args[1]))
        print("ERROR: Script will be terminated.")
        sys.exit(1)
    finally:
        if db: db.close()
        if cursor: cursor.close()

def generate_symbolic_link(scientific_name,
                           default_image_file_name,
                           absolute_directory_path):
    """ Create relative symlinks: (Scientific name 1.jpg -> media_list[0].jpg) """

    link_file_name = scientific_name + '.jpg'
    
    # print('DEBUG: ' + link_file_name + '   ' + default_image_file_name + '   ' + absolute_directory_path)
    
    try:
        # Change cwd to create relative symlinks
        os.chdir(absolute_directory_path)
        # Remove the old link.
        if os.path.islink(link_file_name):
            os.remove(link_file_name)
        # Add new link if default image exists.
        if default_image_file_name:
            if os.path.isfile(default_image_file_name):
                os.symlink(default_image_file_name, link_file_name)
    except Exception as e:
        print('Failed to create symlink. From: ' + link_file_name + '   To: ' + default_image_file_name)


if __name__ == "__main__":
    execute()

