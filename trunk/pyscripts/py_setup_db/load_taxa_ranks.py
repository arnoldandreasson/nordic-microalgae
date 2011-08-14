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

import MySQLdb as mysql
import sys

def execute(db_host = 'localhost', 
            db_name = 'nordicmicroalgae', 
            db_user = 'root', 
            db_passwd = ''):
    """ Creates table with sort order information for taxonomic rank. """
    db = None
    cursor = None
    try:
        # Connect to db.
        db = mysql.connect(host = db_host, db = db_name, 
                           user = db_user, passwd = db_passwd,
                           use_unicode = True, charset = 'utf8')
        cursor=db.cursor()
        # Delete all rows.
        cursor.execute(""" delete from taxa_ranks """) 
        # Insert new rows.
        cursor.execute("""

insert into taxa_ranks(rank, sort_order) values ('Rootlevel', 0); -- For internal use.
insert into taxa_ranks(rank, sort_order) values ('Domain', 5); -- Note: Empire or Domain.
insert into taxa_ranks(rank, sort_order) values ('Kingdom', 15);
insert into taxa_ranks(rank, sort_order) values ('Subkingdom', 16);
insert into taxa_ranks(rank, sort_order) values ('Phylum', 25); -- Note: Division in botany.
insert into taxa_ranks(rank, sort_order) values ('Subphylum', 26);
insert into taxa_ranks(rank, sort_order) values ('Superclass', 34);
insert into taxa_ranks(rank, sort_order) values ('Class', 35);
insert into taxa_ranks(rank, sort_order) values ('Subclass', 36);
insert into taxa_ranks(rank, sort_order) values ('Infraclass', 37);
insert into taxa_ranks(rank, sort_order) values ('Superorder', 44);
insert into taxa_ranks(rank, sort_order) values ('Order', 45);
insert into taxa_ranks(rank, sort_order) values ('Suborder', 46);
insert into taxa_ranks(rank, sort_order) values ('Infraorder', 47);
insert into taxa_ranks(rank, sort_order) values ('Superfamily', 54);
insert into taxa_ranks(rank, sort_order) values ('Family', 55);
insert into taxa_ranks(rank, sort_order) values ('Subfamily', 56);
insert into taxa_ranks(rank, sort_order) values ('Tribe', 65);
insert into taxa_ranks(rank, sort_order) values ('Genus', 75);
insert into taxa_ranks(rank, sort_order) values ('Subgenus', 76);
insert into taxa_ranks(rank, sort_order) values ('Species pair', 84);
insert into taxa_ranks(rank, sort_order) values ('Species', 85);
insert into taxa_ranks(rank, sort_order) values ('Subspecies', 86);
insert into taxa_ranks(rank, sort_order) values ('Variety', 94); -- Note: Botany.
insert into taxa_ranks(rank, sort_order) values ('Form', 95); -- Note: Zoology.
insert into taxa_ranks(rank, sort_order) values ('Hybrid', 96);

        """)
    #
    except mysql.Error, e:
        print("ERROR: MySQL %d: %s" % (e.args[0], e.args[1]))
        print("ERROR: Script will be terminated.")
        sys.exit(1)
    finally:
        if cursor: cursor.close()
        if db: db.close()


# Main.
if __name__ == '__main__':
    execute()

