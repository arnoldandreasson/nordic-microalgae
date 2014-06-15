#!/usr/bin/python

# Nordic Microalgae Mobile. http://m.nordicmicroalgae.org
#
# Author: Andreas Loo, info@andreasloo.se
# Copyright (c) 2013 SMHI, Swedish Meteorological and Hydrological Institute
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

import SimpleHTTPServer
import SocketServer
import os


# Serve app for development purposes
def serve_app():
    os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/app")
    RequestHandler = SimpleHTTPServer.SimpleHTTPRequestHandler
    RequestHandler.extensions_map[".webapp"] = "application/x-web-app-manifest+json"
    httpd = SocketServer.TCPServer(("", 8000), RequestHandler)
    print "Serving at port 8000"
    httpd.serve_forever()

if __name__ == "__main__":
    serve_app()
