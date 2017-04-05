#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Nordicmicroalgae. http://nordicmicroalgae.org/
# Copyright (c) 2011-2017 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import nordicmicroalgae_settings as settings

import mysql.connector # From mysql-connector-python or mysql-connector.
import sys

def execute(db_host = settings.MYSQL_HOST, 
            db_name = settings.MYSQL_DATABASE, 
            db_user = settings.MYSQL_USER, 
            db_passwd = settings.MYSQL_PASSWORD):
    """ 
    Creates all tables in the database. 
    All table definitions is located in this Python script as pure text.
    """
    db = None
    cursor = None
    try:
        # Connect to db.
        db = mysql.connector.connect(
                        host = db_host, 
                        db = db_name, 
                        user = db_user, 
                        passwd = db_passwd,
#                        use_unicode = True, charset = 'utf8')
                        use_unicode = True, charset = 'utf8mb4')
        cursor=db.cursor()
        #
        sql_statements = """
                
-- ===== TAXA =====

-- Table: taxa --
drop table if exists taxa;
create table taxa (
  id                 int unsigned auto_increment not null, -- PK.
  name               varchar(100) not null default '',
  author             varchar(200) not null default '',
  rank               varchar(64) not null default '',
  parent_id          int unsigned not null default 0, -- FK to taxa.id. 
  -- constraints:
  primary key (id),
  key (name),
  key (rank),
  key (parent_id)  
) engine=MyISAM charset=utf8mb4;

-- Table: taxa_ranks --
drop table if exists taxa_ranks;
create table taxa_ranks (
  rank               varchar(64) not null,
  sort_order         int unsigned not null,
  -- constraints:
  primary key (rank)
) engine=MyISAM charset=utf8mb4;

-- Table: taxa_synonyms --
drop table if exists taxa_synonyms;
create table taxa_synonyms (
  taxon_id           int unsigned not null, -- FK.
  synonym_name       varchar(100) not null default '',
  synonym_author     varchar(200) not null default '',
  info_json          text,
  -- constraints:
  primary key (taxon_id, synonym_name),
  key (synonym_name)
) engine=MyISAM charset=utf8mb4;

-- Table: taxa_hierarchy_search --
-- Note: Should be automatically generated from taxa.
drop table if exists taxa_hierarchy_search;
create table taxa_hierarchy_search (
  taxon_id           int unsigned not null, -- FK.
  ancestor_id        int unsigned not null, -- FK to taxa.id. 
  -- constraints:
  primary key (taxon_id, ancestor_id), 
  key (ancestor_id)  
) engine=MyISAM charset=utf8mb4;

-- Table: taxa_navigation --
-- Note: Should be automatically generated from taxa.
drop table if exists taxa_navigation;
create table taxa_navigation (
  taxon_id           int unsigned not null, -- FK.
  name               varchar(100) not null default '',
  rank               varchar(100) not null default '',
  parent             varchar(100) not null default '',
  prev_in_rank       varchar(100) not null default '',
  next_in_rank       varchar(100) not null default '',
  prev_in_tree       varchar(100) not null default '',
  next_in_tree       varchar(100) not null default '',
  sort_order_tree    int unsigned not null default 0,
  classification     text,
  children           text,
  siblings           text,
  -- constraints:
  primary key (taxon_id), 
  key (name, rank)  
) engine=MyISAM charset=utf8mb4;
        
-- ===== FACTS =====

-- Table: taxa_facts --
drop table if exists taxa_facts;
create table taxa_facts (
  taxon_id           int unsigned not null, -- FK, PK.
  facts_json         text,
  -- constraints:
  primary key (taxon_id) 
) engine=MyISAM charset=utf8mb4;

-- Table: taxa_facts_drafts --
drop table if exists taxa_facts_drafts;
create table taxa_facts_drafts (
  taxon_id           int unsigned not null, -- FK, PK.
  facts_json         text,
  -- constraints:
  primary key (taxon_id) 
) engine=MyISAM charset=utf8mb4;

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
) engine=MyISAM charset=utf8mb4;

-- ===== MEDIA =====

-- Table: taxa_media --
drop table if exists taxa_media;
create table taxa_media (
  taxon_id           int unsigned not null, -- FK, PK.
  media_id           varchar(100) not null default '', -- PK.
  media_type         varchar(50) not null default '', -- PK.
  user_name          varchar(100) not null default '',
  metadata_json      text,
  -- constraints:
  primary key (taxon_id, media_id, media_type), 
  key (media_id),  
  key (media_type)  
) engine=MyISAM charset=utf8mb4;

-- Table: taxa_media_list --
drop table if exists taxa_media_list;
create table taxa_media_list (
  taxon_id           int unsigned not null, -- FK, PK.
  media_list         text,
  -- constraints:
  primary key (taxon_id) 
) engine=MyISAM charset=utf8mb4;

-- Table: taxa_media_filter_search --
-- Note: Should be automatically generated from taxa_media.
drop table if exists taxa_media_filter_search;
create table taxa_media_filter_search (
  taxon_id           int unsigned not null, -- FK.
  media_id           varchar(100) not null default '', -- PK.
  filter             varchar(64) not null default '', -- PK, K. -- 
  value              varchar(64) not null default '', -- PK.
  -- constraints:
  primary key (media_id, filter, value), 
  key (filter) 
) engine=MyISAM charset=utf8mb4;

-- ===== EXTERNAL =====

-- Table: taxa_external_links --
drop table if exists taxa_external_links;
create table taxa_external_links (
  taxon_id           int unsigned not null, -- FK, PK.
  provider           varchar(64) not null default '', -- PK.
  type               varchar(64) not null default '', -- PK.
  value              text,
  -- constraints:
  primary key (taxon_id, provider, type)
) engine=MyISAM charset=utf8mb4;

-- Table: taxa_external_facts --
drop table if exists taxa_external_facts;
create table taxa_external_facts (
  taxon_id           int unsigned not null, -- FK, PK.
  provider           varchar(64) not null default '', -- PK.
  facts_json         text,
  -- constraints:
  primary key (taxon_id, provider)
) engine=MyISAM charset=utf8mb4;

-- Table: taxa_helcom_peg (HELCOM PEG, Plankton Expert Group) --
drop table if exists taxa_helcom_peg;
create table taxa_helcom_peg (
  taxon_id           int unsigned not null, -- FK, PK.
  facts_json         text,
  -- constraints:
  primary key (taxon_id) 
) engine=MyISAM charset=utf8mb4;

-- ===== SYSTEM =====

-- Table: system_settings --
drop table if exists system_settings;
create table system_settings (
  settings_key        varchar(64) not null default '', -- PK.
  settings_value      text,
  -- constraints:
  primary key (settings_key)
) engine=MyISAM charset=utf8mb4;

-- Table: change_history --
drop table if exists change_history;
create table change_history (
  id                  int unsigned auto_increment not null, -- PK.
  taxon_id            int unsigned not null, -- FK.
  current_taxon_name  varchar(100) not null default '',
  user_name           varchar(100) not null default '',
  description         text,
  timestamp           datetime,
  -- constraints:
  primary key (id),
  key (taxon_id, timestamp),
  key (user_name, timestamp),
  key (timestamp)
) engine=MyISAM charset=utf8mb4;

commit;

"""

        
        # Execute the statements.
        for result in cursor.execute(sql_statements, multi=True):
            pass
        #
        if db: db.close()
    #
    except mysql.connector.Error as e:
        print("ERROR: MySQL %d: %s" % (e.args[0], e.args[1]))
        print("ERROR: Script will be terminated.")
        sys.exit(1)


if __name__ == "__main__":
    execute()

