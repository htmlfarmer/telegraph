import urllib
import urllib2
import socket # needed for timeout
import re
import json
import sys
import xml.etree.ElementTree as ET

# About: Get Remote Content
# TODO: requires host to be http://

host = "" # for static host
regex = "" # for static regex

if(len(sys.argv) > 1):
    host = sys.argv[1]
    if(len(sys.argv) > 2):
        regex = sys.argv[2]
else: # requires "http://" before
    host= "http://ubuntu.com" #"www.google.com" #"73.186.246.38" #128.128.76.17 #WHOI.edu

def GET_REQUEST(address):

    timeout = 60
    socket.setdefaulttimeout(timeout)

    user_agent = 'Network Graph Research (Linux; Cape Cod, MA)'
    headers = { 'User-Agent' : user_agent }

    req = urllib2.Request(url = address, headers = headers)
    response = urllib2.urlopen(req)
    content = response.read()
    return content

# GET THE HTML from REMOTE HOST
html = GET_REQUEST(host)

if(regex):
    matcher = re.compile(regex)
    match = matcher.search(html).group()
    print match
else:
    print html
