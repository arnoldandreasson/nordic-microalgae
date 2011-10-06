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
import json

def execute(db_host = 'localhost', 
            db_name = 'nordicmicroalgae', 
            db_user = 'root', 
            db_passwd = ''
            ):
    """ Automatically generated the taxa facts field 'ID’s in other systems'. """
    db = None
    cursor = None
    try:
        # Connect to db.
        db = mysql.connect(host = db_host, db = db_name, 
                           user = db_user, passwd = db_passwd,
                           use_unicode = True, charset = 'utf8')
        cursor=db.cursor()        
        #
        # Loop through all taxa.
        cursor.execute("select id, name from taxa")
        for taxon_id, name in cursor.fetchall():            
            dyntaxaid = None
            algaebaseid = None
            omnidiacode = None
            # Get Dyntaxa id.
            cursor.execute("select facts_json from taxa_external_facts where (taxon_id = %s) and (provider = %s)", 
                           (taxon_id, u'Dyntaxa'))
            result = cursor.fetchone()
            if result:
                factsdict = json.loads(result[0], encoding = 'utf-8')
                dyntaxaid = factsdict['Dyntaxa id']
            # Get Algaebase id.
            cursor.execute("select facts_json from taxa_external_facts " +
                           "where (taxon_id = %s) and (provider = %s)", 
                           (taxon_id, u'AlgaeBase'))
            result = cursor.fetchone()
            if result:
                factsdict = json.loads(result[0], encoding = 'utf-8')
                algaebaseid = factsdict['Algaebase id']
            # Get OMNIDIA code.
            cursor.execute("select facts_json from taxa_external_facts " +
                           "where (taxon_id = %s) and (provider = %s)", 
                           (taxon_id, u'SLU'))
            result = cursor.fetchone()
            if result:
                factsdict = json.loads(result[0], encoding = 'utf-8')
                omnidiacode = factsdict['OMNIDIA code']
            #
            # Create html content for the facts field 'ID’s in other systems'.
            htmlstring = '<ul>'
            if dyntaxaid:
                htmlstring += '<li>Dynamic taxa ID: ' + unicode(dyntaxaid) + '<br/>' + \
                              """More info at <a href="http://www.artdata.slu.se/dyntaxa"> <i>http://www.artdata.slu.se/dyntaxa</i>.</a>and <a href="http://www.norbaf.net"> <i>http://www.norbaf.net</i>.</a>""" + \
                              '</li>'
            if algaebaseid:
                htmlstring += '<li>AlgaeBase ID: ' + unicode(algaebaseid) + '</li>'
            if omnidiacode:
                htmlstring += '<li>OMNIDIA code: ' + unicode(omnidiacode) + '<br/>' + \
                              """Used by many freshwater diatomists. See <a href="http://omnidia.free.fr/omnidia_english.htm"> <i>http://omnidia.free.fr/omnidia_english.htm</i>.</a>and <a href="http://www.norbaf.net"> <i>http://www.norbaf.net</i>.</a>""" + \
                              '</li>'
            htmlstring += '</ul>'
            #
            # Get facts_json from db.
            cursor.execute("select facts_json from taxa_external_facts where (taxon_id = %s) and (provider = %s)", 
                           (taxon_id, u'Generated facts'))
            result = cursor.fetchone()
            if result:
                # From string to dictionary.
                factsdict = json.loads(result[0], encoding = 'utf-8')
            else:
                # Add empty columns.
                factsdict = {}
            # Update facts.
            if dyntaxaid or algaebaseid or omnidiacode:
                factsdict["ID’s in other systems"] = htmlstring
            else:
                if "ID’s in other systems" in factsdict:
                    del factsdict["ID’s in other systems"] # Delete if it was earlier added.
            # Convert facts to string.
            jsonstring = json.dumps(factsdict, encoding = 'utf-8', 
                                 sort_keys=True, indent=4)
            # Check if db row exists. 
            cursor.execute("select count(*) from taxa_external_facts where (taxon_id = %s) and (provider = %s)", 
                           (taxon_id, u'Generated facts'))
            result = cursor.fetchone()
            if result[0] == 0: 
                cursor.execute("insert into taxa_external_facts(taxon_id, provider, facts_json) values (%s, %s, %s)", 
                               (unicode(taxon_id), u'Generated facts', jsonstring))
            else:
                cursor.execute("update taxa_facts set taxa_external_facts = %s where (taxon_id = %s) and (provider = %s)", 
                               (jsonstring, unicode(taxon_id), u'Generated facts'))
            
    #
    except mysql.Error, e:
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
    except getopt.error, msg:
        print msg
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

