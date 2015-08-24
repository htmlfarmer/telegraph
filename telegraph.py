import sys
import subprocess
import urllib
import urllib2
import socket # needed for timeout
import re
import json
import xml.etree.ElementTree as ET

"""
About: This program searches Vacinity Information based on IP Address
        geo = a JSON object with lat/lng
        address = Street Address Information for the IP Address
        wiki = a XML object with localized wikipedia info based on lat/lng
        # http://www.census.gov/geo/maps-data/data/tiger.html
        # https://geoiptool.com/en/?ip=128.128.76.17
        # http://wiki.openstreetmap.org/wiki/Nominatim
        # http://www.geonames.org/export/ws-overview.html
        NOTE: Free 135 MB GeoIP Database http://dev.maxmind.com/geoip/geoip2/geolite2/
"""

if(len(sys.argv) > 1):
    host = sys.argv[1]
else:
    host= "ubuntu.com" #"www.google.com" #"73.186.246.38" #128.128.76.17 #WHOI.edu

# traceroute: to collect timing info along this route

traceroute = subprocess.Popen(
    ["traceroute", "-q", "5", host],
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE
)

tracetext, error = traceroute.communicate()

matcher = re.compile("(?<=\()\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?=\) )")
ips = matcher.findall(tracetext)
print ips #print tracetext

def GET_REQUEST(address):

    timeout = 60
    socket.setdefaulttimeout(timeout)

    user_agent = 'Network Graph Research (Linux; Cape Cod, MA)'
    headers = { 'User-Agent' : user_agent }

    req = urllib2.Request(url = address, headers = headers)
    response = urllib2.urlopen(req)
    content = response.read()
    return content

# Get the IP ADDRESS Geo Location lat/lng
# https://geoiptool.com/en/?ip=128.128.76.17
locations = []

ips.pop(0) #the first address is localhost and it needs to be removed

# blacklist = {"lng": "lat"}
# wichita maybe okay: "-97.2251" : "37.7083"
blacklist = {"-6.2597" : "53.3478", "-97.0" : "38.0", "-97.2251" : "37.7083"}

for ip in ips:
    geohtml = GET_REQUEST("https://www.geoiptool.com/en/?ip=" + ip)
    matcher = re.compile("{lat: .*}")
    geo = matcher.search(geohtml).group()
    geo = geo.replace("lat","\"lat\"")
    geo = geo.replace("lng","\"lng\"")
    geo = json.loads(geo) # if you need the json data type
    lat = geo["lat"] #"41.618116"
    lng = geo["lng"] #"-70.485361"
    if str(lng) not in blacklist:
        locations.append([lng, lat])

print locations

"""
# Area Lookup for lat/lng of IP ADDRESS
# http://nominatim.openstreetmap.org/search?q=us+41.618116,-70.485361&format=json&addressdetails=1
openmap = GET_REQUEST("http://nominatim.openstreetmap.org/search?q=us+"+ str(lat) +","+ str(lng) + "&format=json&addressdetails=1")
address = json.loads(openmap)
print address

# IF NEEDED: address lookup http://pelias.mapzen.com/reverse?lat=41.6178&lon=-70.5147

# Do a Wikipedia Lookup Based on geolocation (Cape Cod, MA)
# http://api.geonames.org/findNearbyWikipedia?lat=41.618116&lng=-70.485361&username=demo
wikihtml = GET_REQUEST("http://api.geonames.org/findNearbyWikipedia?lat="+ str(lat) +"&lng="+ str(lng) + "&username=asolr")
wiki = ET.fromstring(wikihtml) # if you need the xml data type
print ET.tostring(wiki)
"""
