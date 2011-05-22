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
import connect_to_db

def execute():
    """ Creates all tables in the database. """
    try:
        # Connect to db.
        db = connect_to_db.connect()
        cursor=db.cursor()
        #
        cursor.execute("""
        
-- ===== TAXA =====

-- Table: taxa --
drop table if exists taxa;
create table taxa (
  id                 int unsigned auto_increment not null, -- PK.
  name               varchar(128) not null default '',
  author             varchar(256) not null default '',
  rank               varchar(64) not null default '',
  parent_id          int unsigned not null default 0, -- FK to taxa.id. 
  -- constraints:
  primary key (id),
  key (name),
  key (rank),
  key (parent_id)  
) engine=MyISAM charset=utf8;

-- Table: taxa_ranks --
drop table if exists taxa_ranks;
create table taxa_ranks (
  rank               varchar(64) not null,
  sort_order         int unsigned not null,
  -- constraints:
  primary key (rank)
) engine=MyISAM charset=utf8;

-- Table: taxa_synonyms --
drop table if exists taxa_synonyms;
create table taxa_synonyms (
  taxon_id           int unsigned not null, -- FK.
  synonym_name       varchar(128) not null default '',
  synonym_author     varchar(256) not null default '',
  info_json          text not null default '',
  -- constraints:
  primary key (taxon_id),
  key (synonym_name)
) engine=MyISAM charset=utf8;

-- Table: taxa_hierarchy_search --
-- Note: Should be automatically generated from taxa.
drop table if exists taxa_hierarchy_search;
create table taxa_hierarchy_search (
  taxon_id           int unsigned not null, -- FK.
  ancestor_id        int unsigned not null, -- FK to taxa.id. 
  -- constraints:
  primary key (taxon_id, ancestor_id), 
  key (ancestor_id)  
) engine=MyISAM charset=utf8;

-- Table: taxa_navigation --
-- Note: Should be automatically generated from taxa.
drop table if exists taxa_navigation;
create table taxa_navigation (
  taxon_id           int unsigned not null, -- FK.
  name               varchar(128) not null default '',
  rank               varchar(128) not null default '',
  prev_in_rank       varchar(128) not null default '',
  next_in_rank       varchar(128) not null default '',
  prev_in_tree       varchar(128) not null default '',
  next_in_tree       varchar(128) not null default '',
  sort_order_tree    int unsigned not null default 0,
  classification     text not null default '',
  children           text not null default '',
  siblings           text not null default '',
  -- constraints:
  primary key (taxon_id), 
  key (name, rank)  
) engine=MyISAM charset=utf8;


-- ===== FACTS =====

-- Table: taxa_facts --
drop table if exists taxa_facts;
create table taxa_facts (
  taxon_id           int unsigned not null, -- FK, PK.
  facts_json         text not null default '',
  -- constraints:
  primary key (taxon_id) 
) engine=MyISAM charset=utf8;

-- Table: taxa_facts_drafts --
drop table if exists taxa_facts_drafts;
create table taxa_facts_drafts (
  taxon_id           int unsigned not null, -- FK, PK.
  facts_json         text not null default '',
  -- constraints:
  primary key (taxon_id) 
) engine=MyISAM charset=utf8;

-- Table: taxa_filter_search --
-- Note: Should be automatically generated from taxa_facts.
drop table if exists taxa_filter_search;
create table taxa_filter_search (
  taxon_id           int unsigned not null, -- FK, PK.
  filter             varchar(64) not null default '', -- PK. -- Country, Geographic area, Habitat, Trophic type.
  value              varchar(64) not null default '',
  -- constraints:
  primary key (taxon_id, filter, value), 
  key (filter) 
) engine=MyISAM charset=utf8;

-- ===== MEDIA =====

-- Table: taxa_media --
drop table if exists taxa_media;
create table taxa_media (
  taxon_id           int unsigned not null, -- FK, PK.
  media_id           varchar(64) not null default '',
  media_type         varchar(64) not null default '',
  user_name          varchar(128) not null default '',
  metadata_json      text not null default '',
  -- constraints:
  primary key (taxon_id, media_id, media_type), 
  key (media_type)  
) engine=MyISAM charset=utf8;

-- Table: taxa_media_list --
drop table if exists taxa_media_list;
create table taxa_media_list (
  taxon_id           int unsigned not null, -- FK, PK.
  media_list         text not null default '',
  -- constraints:
  primary key (taxon_id) 
) engine=MyISAM charset=utf8;

-- ===== EXTERNAL =====

-- Table: taxa_external_links --
drop table if exists taxa_external_links;
create table taxa_external_links (
  taxon_id           int unsigned not null, -- FK, PK.
  provider           varchar(64) not null default '', -- PK.
  type               varchar(64) not null default '', -- PK.
  value              varchar(64) not null default '',
  -- constraints:
  primary key (taxon_id, provider, type)
) engine=MyISAM charset=utf8;

-- Table: taxa_facts_external --
drop table if exists taxa_facts_external;
create table taxa_facts_external (
  taxon_id           int unsigned not null, -- FK, PK.
  provider           varchar(64) not null default '', -- PK.
  facts_json         text not null default '',
  -- constraints:
  primary key (taxon_id, provider)
) engine=MyISAM charset=utf8;

-- Table: taxa_facts_peg (Plankton Expert Group) --
drop table if exists taxa_facts_peg;
create table taxa_facts_peg (
  taxon_id           int unsigned not null, -- FK, PK.
  facts_json         text not null default '',
  -- constraints:
  primary key (taxon_id) 
) engine=MyISAM charset=utf8;

-- ===== SYSTEM =====

-- Table: system_settings --
drop table if exists system_settings;
create table system_settings (
  settings_key        varchar(64) not null default '', -- PK.
  settings_value      text not null default '',
  -- constraints:
  primary key (settings_key)
) engine=MyISAM charset=utf8;

-- Table: change_history --
drop table if exists change_history;
create table change_history (
  id                  int unsigned auto_increment not null, -- PK.
  taxon_id            int unsigned not null, -- FK.
  current_taxon_name  varchar(128) not null default '',
  user_name           varchar(128) not null default '',
  description         text,
  timestamp           datetime,
  -- constraints:
  primary key (id),
  key (taxon_id, timestamp),
  key (user_name, timestamp),
  key (timestamp)
) engine=MyISAM charset=utf8;

        """)
    #
    except mysql.Error, e:
        print("ERROR: MySQL %d: %s" % (e.args[0], e.args[1]))
        print("ERROR: Script will be terminated.")
        sys.exit(1)
    finally:
        ### if cursor: cursor.close()
        if db: db.close()


# Main.
if __name__ == '__main__':
    execute()

