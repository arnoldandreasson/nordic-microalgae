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

import py_export.export_taxa as export_taxa
import py_export.export_taxa_facts as export_taxa_facts
import py_export.export_taxa_media as export_taxa_media
import py_backup.export_to_backup as export_to_backup

def execute(db_host, db_name, db_user, db_passwd, path_to_downloads):
    """ """
    #
    print("\n=== Export: taxa. ===\n")
    export_taxa.execute(db_host, db_name, db_user, db_passwd,
                        file_name = path_to_downloads + 'taxa.txt')
    #
    print("\n=== Export: taxa_facts. ===\n")
    export_taxa_facts.execute(db_host, db_name, db_user, db_passwd, 
                              file_name = path_to_downloads + 'taxa_facts.txt')
    #
    print("\n=== Export: taxa_media. ===\n")
    export_taxa_media.execute(db_host, db_name, db_user, db_passwd, 
                              file_name = path_to_downloads + 'taxa_media.txt')
    #    
    print("\n=== Export: taxa_facts_backup, taxa_media_backup, taxa_media_list_backup and change_history_backup. ===\n")
    export_to_backup.execute(db_host, db_name, db_user, db_passwd, 
                             taxa_facts_file_name = path_to_downloads + 'taxa_facts_backup.txt', 
                             taxa_media_file_name = path_to_downloads + 'taxa_media_backup.txt', 
                             taxa_media_list_file_name = path_to_downloads + 'taxa_media_list_backup.txt', 
                             change_history_file_name = path_to_downloads + 'change_history_backup.txt') 
    #
    print("\n=== Finished. ===\n")


# To be used when this module is launched directly from the command line.
import getopt, sys
def main():
    # Parse command line options.
    try:
        opts, args = getopt.getopt(sys.argv[1:], 
                                   "h:d:u:p:d:", 
                                   ["host=", "database=", "user=", "password=", "downloadspath="])
    except getopt.error, msg:
        print msg
        sys.exit(2)
    # Create dictionary with named arguments.
    params = {"db_host": "localhost", 
              "db_name": "nordicmicroalgae", 
              "db_user": "root", 
              "db_passwd": "",
              "path_to_downloads": "data_download/"}
    for opt, arg in opts:
        if opt in ("-h", "--host"):
            params['db_host'] = arg
        elif opt in ("-d", "--database"):
            params['db_name'] = arg
        elif opt in ("-u", "--user"):
            params['db_user'] = arg
        elif opt in ("-p", "--password"):
            params['db_passwd'] = arg
        elif opt in ("-d", "--downloadspath"):
            params['path_to_downloads'] = arg
    # Execute with parameter list.
    execute(**params) # The "two stars" prefix converts the dictionary into named arguments. 

if __name__ == "__main__":
    main()

