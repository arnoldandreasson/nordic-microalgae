#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Nordicmicroalgae. http://nordicmicroalgae.org/
# Copyright (c) 2011-2017 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

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

import mysql.connector
import sys

def execute(db_host = 'localhost', 
            db_name = 'nordicmicroalgae', 
            db_user = 'root', 
            db_passwd = ''):
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


if __name__ == "__main__":
    execute()

