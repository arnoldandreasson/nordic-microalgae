#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Nordicmicroalgae. http://nordicmicroalgae.org/
# Copyright (c) 2011-2017 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

# Settings for MySql.

MYSQL_HOST = 'localhost' 
MYSQL_DATABASE = 'nordicmicroalgae' 
MYSQL_USER = 'root' 
MYSQL_PASSWORD = ''

# Paths to directories and files. 

PATH_TO_DOWNLOADS = 'test_download'
PATH_TO_BACKUP = 'test_backup'

# Media settings.

MEDIA_PATH_TO_UPLOADED_FILES = 'test_media_uploaded_files'
MEDIA_PATH_TO_ORIGINAL_FILES = 'test_media_original'
MEDIA_PATH_TO_STANDARD_FILES = 'test_media_large'
MEDIA_PATH_TO_THUMBNAIL_FILES = 'test_media_small'
MEDIA_PATH_TO_EXCLUDE_LIST = 'test_media_exclude_list.txt'

MEDIA_STANDARD_IMAGE_SIZE = (700, 1400)
MEDIA_THUMBNAIL_SIZE = (200, 150)
