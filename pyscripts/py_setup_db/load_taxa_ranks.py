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

# Example AlgaeBase: --
#  e: Eukaryota, (Empire or Domain)
#  k: Plantae, (Kingdom)
#  sk: Biliphyta, ()
#  p: Rhodophyta, (Phylum)
#  sp: Eurhodophytina, (Subphylum)
#  c: Florideophyceae, (Class)
#  sc: Rhodymeniophycidae, (Subclass)
#  o: Ceramiales, (Order)
#  f: Delesseriaceae, (Family)
#  sf: Delesserioideae, (Subfamily)
#  t: Delesserieae, (Tribe)
#  g: Delesseria(Genus)
#

try:
    import nordicmicroalgae_settings
except:
    # For development.
    MYSQL_HOST = 'localhost' 
    MYSQL_DATABASE = 'nordicmicroalgae' 
    MYSQL_USER = 'root' 
    MYSQL_PASSWORD = ''

import sys

def execute(db_host = MYSQL_HOST, 
            db_name = MYSQL_DATABASE, 
            db_user = MYSQL_USER, 
            db_passwd = MYSQL_PASSWORD):
    """ 
    Creates table with sort order information for taxonomic rank. 
    All data is located in this Python script.
    """
    db = None
    cursor = None
    try:
        # Connect to db.
        db = mysql.connector.connect(host = db_host, db = db_name, 
                           user = db_user, passwd = db_passwd,
                           use_unicode = True, charset = 'utf8')
        cursor=db.cursor()
        # Delete all rows.
        cursor.execute(""" delete from taxa_ranks """) 
        # Insert new rows.
#         cursor.execute("""
        cursor.execute(""" insert into taxa_ranks(rank, sort_order) values ('Rootlevel', 0); """) # For internal use.
        cursor.execute(""" insert into taxa_ranks(rank, sort_order) values ('Domain', 5); """) # Note: Empire or Domain.
        cursor.execute(""" insert into taxa_ranks(rank, sort_order) values ('Kingdom', 15); """)
        cursor.execute(""" insert into taxa_ranks(rank, sort_order) values ('Subkingdom', 16); """)
        cursor.execute(""" insert into taxa_ranks(rank, sort_order) values ('Phylum', 25); """) # Note: Division in botany.
        cursor.execute(""" insert into taxa_ranks(rank, sort_order) values ('Subphylum', 26); """)
        cursor.execute(""" insert into taxa_ranks(rank, sort_order) values ('Superclass', 34); """)
        cursor.execute(""" insert into taxa_ranks(rank, sort_order) values ('Class', 35); """)
        cursor.execute(""" insert into taxa_ranks(rank, sort_order) values ('Subclass', 36); """)
        cursor.execute(""" insert into taxa_ranks(rank, sort_order) values ('Infraclass', 37); """)
        cursor.execute(""" insert into taxa_ranks(rank, sort_order) values ('Superorder', 44); """)
        cursor.execute(""" insert into taxa_ranks(rank, sort_order) values ('Order', 45); """)
        cursor.execute(""" insert into taxa_ranks(rank, sort_order) values ('Suborder', 46); """)
        cursor.execute(""" insert into taxa_ranks(rank, sort_order) values ('Infraorder', 47); """)
        cursor.execute(""" insert into taxa_ranks(rank, sort_order) values ('Superfamily', 54); """)
        cursor.execute(""" insert into taxa_ranks(rank, sort_order) values ('Family', 55); """)
        cursor.execute(""" insert into taxa_ranks(rank, sort_order) values ('Subfamily', 56); """)
        cursor.execute(""" insert into taxa_ranks(rank, sort_order) values ('Tribe', 65); """)
        cursor.execute(""" insert into taxa_ranks(rank, sort_order) values ('Genus', 75); """)
        cursor.execute(""" insert into taxa_ranks(rank, sort_order) values ('Subgenus', 76); """)
        cursor.execute(""" insert into taxa_ranks(rank, sort_order) values ('Species pair', 84); """)
        cursor.execute(""" insert into taxa_ranks(rank, sort_order) values ('Species', 8); """)
        cursor.execute(""" insert into taxa_ranks(rank, sort_order) values ('Subspecies', 86); """)
        cursor.execute(""" insert into taxa_ranks(rank, sort_order) values ('Variety', 94); """) # Note: Botany.
        cursor.execute(""" insert into taxa_ranks(rank, sort_order) values ('Form', 95); """) # Note: Zoology.
        cursor.execute(""" insert into taxa_ranks(rank, sort_order) values ('Hybrid', 96); """)
    #
    except mysql.connector.Error as e:
        print("ERROR: MySQL %d: %s" % (e.args[0], e.args[1]))
        print("ERROR: Script will be terminated.")
        sys.exit(1)
    finally:
        if cursor: cursor.close()
        if db: db.close()


# To be used when this module is launched directly from the command line.
import getopt
def main():
    # Parse command line options.
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:d:u:p:", ["host=", "database=", "user=", "password="])
    except getopt.error as msg:
        print(msg)
        sys.exit(2)
    # Create dictionary with named arguments.
    params = {}
    for opt, arg in opts:
        if opt in ("-h", "--host"):
            params['db_host'] = arg
        elif opt in ("-d", "--database"):
            params['db_name'] = arg
        elif opt in ("-u", "--user"):
            params['db_user'] = arg
        elif opt in ("-p", "--password"):
            params['db_passwd'] = arg
    # Execute with parameter list.
    execute(**params) # The "two stars" prefix converts the dictionary into named arguments. 

if __name__ == "__main__":
    main()

