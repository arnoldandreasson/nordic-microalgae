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

import MySQLdb as mysql
import sys
    
def execute(db_host = 'localhost', 
            db_name = 'nordicmicroalgae', 
            db_user = 'root', 
            db_passwd = ''
            ):
    """ Automatically generated db table for fast taxon classification lookup. """
    try:
        # Connect to db.
        db = mysql.connect(host = db_host, db = db_name, 
                           user = db_user, passwd = db_passwd,
                           use_unicode = True, charset = 'utf8')
        cursor_1=db.cursor()
        cursor_2=db.cursor()
        # Remove all rows from table.
        cursor_1.execute(" delete from taxa_hierarchy_search ")
        #
        cursor_1.execute("select id, parent_id from taxa")
        for row_1 in cursor_1.fetchall():
            taxon_id, parent_id = row_1
            #
            if taxon_id == parent_id:
                # Handle error in dyntaxa. Will generate infinite loop.
                print("ERROR: taxon_id = parent_id:" + unicode(taxon_id))
                continue # Continue with next taxon.
            #
            try:
                while (parent_id) and (parent_id != 0):
                    #                
                    cursor_2.execute("insert into taxa_hierarchy_search(taxon_id, ancestor_id) values(%s, %s)",
                                     (unicode(taxon_id), unicode(parent_id)))
                    #
                    cursor_2.execute("select parent_id from taxa " + 
                                     "where id = %s", (unicode(parent_id)))
                    result = cursor_2.fetchone()
                    if result:
                        parent_id = result[0]
                    else:
                        parent_id = 0
            except mysql.Error, e:
                print("ERROR: taxon_id: " + unicode(taxon_id) + " parent_id: " + unicode(parent_id))
                print("ERROR %d: %s" % (e.args[0], e.args[1]))
    #
    except mysql.Error, e:
        print("ERROR: MySQL %d: %s" % (e.args[0], e.args[1]))
        print("ERROR: Script will be terminated.")
        sys.exit(1)
    finally:
        if db: db.close()
        if cursor_1: cursor_1.close()
        if cursor_2: cursor_2.close()


# Main.
if __name__ == '__main__':
    execute()
    
