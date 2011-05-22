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
    
def execute(db_host = 'localhost', 
            db_name = 'nordicmicroalgae', 
            db_user = 'root', 
            db_passwd = '',
            ):
    """ Automatically generated db table for taxon navigation, next, previous, etc. """
    db = None
    cursor = None
    out = None
    try:
        # Connect to db.
        db = connect_to_db.connect(db_host, db_name, db_user, db_passwd)
        cursor=db.cursor()
        # Remove all rows from table.
        cursor.execute(" delete from taxa_navigation ")
        #
        taxa = []
        idtoname = {}
        idtotaxon = {}
        childcount = {} # 
        taxanavigation = {} 
        # Read taxa.
        cursor.execute("select id, name, rank, parent_id from taxa")
        for id, name, rank, parent_id in cursor.fetchall():
            # Add taxon records to taxa.
            taxondict = {'id': id, 'name': name, 'rank': rank, 'parent_id': parent_id}
            taxa.append(taxondict)
            # Taxonid to name.
            idtoname[id] = name
            # Taxonid to taxon dictionary.
            idtotaxon[id] = taxondict
            # Add empty navigation records.
            navigationdict = {'name': name, 
                              'rank': rank, 
                              'prev_in_rank': '', 
                              'next_in_rank': '', 
                              'prev_in_tree': '', 
                              'next_in_tree': '', 
                              'sort_order_tree': 0, 
                              'classification': '', 
                              'children': '', 
                              'siblings': ''}
            # Save result.
            taxanavigation[id] = navigationdict
        #
        # Add previous and next ordered by rank and name.
        # Sort taxa by rank and name.
        taxa.sort(taxa_by_rank_name_sortfunction) # Sort function defined below.
        previousid = None
        previousrank = None
        for item in taxa:
            id = item['id']
            rank = item['rank']
            # Stop chain when changing rank.
            if previousrank and (previousrank == rank):
                if previousid:
                    # Save result.
                    taxanavigation[id]['prev_in_rank'] = idtoname[previousid]
                    taxanavigation[previousid]['next_in_rank'] = idtoname[id]
            else:
                if previousid:
                    # Save result.
                    taxanavigation[id]['prev_in_rank'] = ''
                    taxanavigation[previousid]['next_in_rank'] = ''
            previousrank = rank                 
            previousid = id
        #
        # Add classification.
        for item in taxa:
            id = item['id']
            classification = item['name']
            parenttaxon = item
            while parenttaxon['parent_id'] != 0:
                parenttaxon = idtotaxon[parenttaxon['parent_id']]
                classification = parenttaxon['name'] + ';' + classification
            # Save result.
            taxanavigation[id]['classification'] = classification
            item['classification'] = classification # Used in sort function.
        #
        # Add previous and next name in tree walk. Add value to sort_order_tree.
        # Sort taxa by classification.
        taxa.sort(taxa_by_classification_sortfunction) # Sort function defined below.
        previousid = None
        for index, item in enumerate(taxa):
            id = item['id']
            # Save result.
            taxanavigation[id]['sort_order_tree'] = index
            if previousid:
            # Save result.
                taxanavigation[id]['prev_in_tree'] = idtoname[previousid]
                taxanavigation[previousid]['next_in_tree'] = idtoname[id]
            previousid = id
        #
        # Calculate number of children.
        # Will be used in lists of children and siblings.
        for item in taxa:
            id = item['id']
            name = item['name']
            count = 0
            for item2 in taxa:
                if id == item2['parent_id']:
                    count += 1
            # Save result.
            childcount[name] = count
        #
        # Add children.
        for item in taxa:
            id = item['id']
            children = []
            for item2 in taxa:
                if id == item2['parent_id']:
                    children.append(item2['name'])
            children.sort()
            # Add child-counter to children.
            for index, child in enumerate(children):
                children[index] = child + ':' + unicode(childcount[child])
            # Save result.
            taxanavigation[id]['children'] = ';'.join(children)
        #
        # Add siblings.
        for item in taxa:
            id = item['id']
            name = item['name']
            rank = item['rank']
            parent = item['parent_id']
            siblings = []
            for item2 in taxa:
                if name != item2['name']: # Siblings only.
                    if (parent == item2['parent_id']) and (rank == item2['rank']): # Check rank due to error in tree.
                        siblings.append(item2['name'])
            siblings.sort()
            # Add child-counter to siblings.
            for index, child in enumerate(siblings):
                siblings[index] = child + ':' + unicode(childcount[child])
            # Save result.
            taxanavigation[id]['siblings'] = ';'.join(siblings)
        #
        # Insert all rows in taxa_navigation table.
        for id in taxanavigation:
            navdict = taxanavigation[id]
            
#            print(  unicode(id), navdict['name'], 
#                    navdict['prev'], navdict['next'], 
#                    navdict['prev_tree'], navdict['next_tree'], 
#                    navdict['classification'], navdict['children'], navdict['siblings'] 
#                    )
            #            
            cursor.execute("insert into taxa_navigation " + 
                           "(taxon_id, name, rank, " + 
                           "prev_in_rank, next_in_rank, " + 
                           "prev_in_tree, next_in_tree, sort_order_tree, " + 
                           "classification, children, siblings) " + 
                           "values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           (unicode(id), navdict['name'], navdict['rank'], 
                            navdict['prev_in_rank'], navdict['next_in_rank'], 
                            navdict['prev_in_tree'], navdict['next_in_tree'], navdict['sort_order_tree'], 
                            navdict['classification'], navdict['children'], navdict['siblings'] 
                            ))
    #
    except mysql.Error, e:
        print("ERROR: MySQL %d: %s" % (e.args[0], e.args[1]))
        print("ERROR: Script will be terminated.")
        sys.exit(1)
    finally:
        if db: db.close()
        if cursor: cursor.close()
        if out: out.close()

# Sort functions for taxa list.
def taxa_by_rank_name_sortfunction(s1, s2):
    """ """
    str1 = s1.get('rank', '') + ':' + s1.get('name', '')
    str2 = s2.get('rank', '') + ':' + s2.get('name', '')
    if str1 < str2: return -1
    if str1 > str2: return 1
    return 0 # Both are equal.

def taxa_by_classification_sortfunction(s1, s2):
    """ """
    str1 = s1['classification']
    str2 = s2['classification']
    if str1 < str2: return -1
    if str1 > str2: return 1
    return 0 # Both are equal.


# Main.
if __name__ == '__main__':
    execute()
    
