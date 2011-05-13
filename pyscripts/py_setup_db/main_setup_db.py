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

import create_tables
import load_system_settings
import load_taxa_ranks

def execute():
    """ Script that creates and populates a test database. """
    #
    print("\n=== Create tables. ===\n")
    print("Note: An exception 'lost connection...' will occur during database rebuild.")
    create_tables.execute()
    #
    print("\n=== Load: system_settings. ===\n")
    load_system_settings.execute()
    #
    print("\n=== Load: taxa_ranks. ===\n")
    load_taxa_ranks.execute()
    #
    print("\n=== Finished. ===\n")


# Main.
if __name__ == '__main__':
    execute()
