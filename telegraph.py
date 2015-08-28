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

# CONFIGURATION SETTINGS
pnum = 10 # number of pings to hostname/ip
tnum = 5 # number of pings per traceroute

if(len(sys.argv) > 1):
    host = sys.argv[1]
else:
    host = "mit.edu" #"boston.com" #"www.google.com" #"facebook.com" #"www.whoi.edu"

# traceroute: to collect timing info along this route

# TRACE ROUTE and PING analyzer

# ping: to see the total time along the route

pingtext = ""
pingprocess = subprocess.Popen(
    ["ping", "-c", str(pnum), host],
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE
)

# read the process line by line
while True:
  line = pingprocess.stdout.readline()
  pingtext += line;
  if line != '':
    #the real code does filtering here
    print line.rstrip()
  else:
    break

# matcher for speeds (min,avg,max,mdev)
matcher = re.compile("(\d+.\d+)/(\d+.\d+)/(\d+.\d+)/(\d+.\d+)")
speeds = matcher.search(pingtext)
ping = {}
if(speeds):
    speeds = speeds.groups()
    # the ping times are for the FULL traceroute
    ping = {"ip" : host, # TODO ask Todd maybe has ideas?
            "host": host,
            "min" : float(speeds[0]),
            "avg" : float(speeds[1]),
            "max" : float(speeds[2]),
            "sdev" : float(speeds[3])
            }
    print ping # verify all the timings are correct for the trace
else: # in CASE of ERROR with a PING
    ping = {"ip" : host, # TODO ask Todd maybe has ideas?
        "host": host,
        "min" : "",
        "avg" : "",
        "max" : "",
        "sdev" : ""
        }

# traceroute: to collect timing info along this route

# function for calculating standard deviation
def sdev(data, avg):
    tdev = 0
    for dev in data:
        tdev += abs(dev-avg)
    return tdev/len(data)

# traceroute is the main variable that stored all the traceroute info
traceroute = []
def append_trace(ip, host, times):
    minimum = min(times)
    maximum = max(times)
    average = sum(times)/len(times)
    variance = sdev(times, average)

    trace = {"ip" : ip[0],
        "host" : host[0],
        "times": times,
        "min" : minimum,
        "avg" : average,
        "max" : maximum,
        "sdev" : variance
        #"address" : address,
        #"lat" : lat,
        #"lng" : lng
        #"accesspoint" : router_number
        }
    traceroute.append(trace)
    print trace

def parse_trace(line):
    # get all the ip address for the route
    matcher = re.compile("(?<=\()\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?=\) )")
    ip = matcher.findall(line)

    # get all the text domain names for the route
    matcher = re.compile("(?<=  )[a-zA-Z0-9\-\.]+\.[a-zA-Z0-9]{1,5}(?= \()")
    host = matcher.findall(line)

    # get all the timing information for the route
    matcher = re.compile("\d{1,5}\.\d{1,3}(?= ms)")
    times = matcher.findall(line)

    if len(ip) != 0 and len(host) != 0 and len(times) >= 1:
        for i in range(len(times)):
            times[i] = float(times[i]) # convert time to a number
        append_trace(ip, host, times)

traceprocess = subprocess.Popen(
    ["traceroute", "-q", str(tnum), host],
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE
)

# read the traceroute process line by line
tracetext = ""
while True:
  # TODO if you we see "* * *" quit the loop regex
  line = traceprocess.stdout.readline()
  tracetext += line;
  # if we see 3 or more *'s in a row break
  if line != '' and (re.search('(\* ){3,}', line) is None):
    #the real code does filtering here
    parse_trace(line)
    #print line.rstrip() # remove return at end of line
  else:
    break

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

traceroute.pop(0) #the first address is localhost and it needs to be removed

# blacklist = {"lng": "lat"}
# wichita maybe okay: "-97.2251" : "37.7083"
blacklist = {"-6.2597" : "53.3478", "-97.0" : "38.0", "-97.2251" : "37.7083"}

for index in range(len(traceroute)):
    geohtml = GET_REQUEST("https://www.geoiptool.com/en/?ip=" + traceroute[index]["ip"])
    matcher = re.compile("{lat: .*}")
    geo = matcher.search(geohtml).group()
    geo = geo.replace("lat","\"lat\"")
    geo = geo.replace("lng","\"lng\"")
    geo = json.loads(geo) # if you need the json data type
    lat = geo["lat"] #"41.618116"
    lng = geo["lng"] #"-70.485361"
    if str(lng) not in blacklist:
        traceroute[index]["lat"] = lat
        traceroute[index]["lng"] = lng
    else: # blacklist / bogus location
        traceroute[index]["lat"] = ""
        traceroute[index]["lng"] = ""
    print traceroute[index]

# Area Lookup for lat/lng of IP ADDRESS
# http://nominatim.openstreetmap.org/search?q=us+41.618116,-70.485361&format=json&addressdetails=1
for index in range(len(traceroute)):
    openmap = GET_REQUEST("http://nominatim.openstreetmap.org/search?q=us+"+ str(traceroute[index]["lat"]) +","+ str(traceroute[index]["lng"]) + "&format=json&addressdetails=1")
    address = json.loads(openmap)
    traceroute[index]["address"] = address[0]["display_name"]
    if traceroute[index]["address"] != "United States of America":
        traceroute[index]["importance"] = address[0]["importance"]
    else: # TODO: unknown town
        traceroute[index]["importance"] = ""
    print traceroute[index]

print traceroute

"""
# FINAL DATA EXAMPLE:
[{'sdev': 1.9021599999999999, 'min': 8.61, 'importance': 0.325, 'ip': ['96.120.65.101'], 'address': u'Mashpee, Barnstable County, Massachusetts, 02649, United States of America', 'times': [8.61, 9.332, 9.738, 13.184, 13.195], 'host': ['96.120.65.101'], 'max': 13.195, 'lat': 41.6162, 'lng': -70.4931, 'avg': 10.8118}, {'sdev': 0.3321599999999997, 'min': 13.0, 'importance': 0.325, 'ip': ['68.87.154.77'], 'address': u'Mashpee, Barnstable County, Massachusetts, 02649, United States of America', 'times': [14.038, 13.0, 13.0, 13.0, 13.0], 'host': ['te-9-5-ur02.mashpee.ma.boston.comcast.net'], 'max': 14.038, 'lat': 41.6162, 'lng': -70.4931, 'avg': 13.2076}, {'sdev': 1.7760800000000014, 'min': 13.302, 'importance': 0.325, 'ip': ['68.85.37.93'], 'address': u'Mashpee, Barnstable County, Massachusetts, 02649, United States of America', 'times': [19.768, 15.097, 15.059, 13.413, 13.302], 'host': ['be-113-ar01.needham.ma.boston.comcast.net'], 'max': 19.768, 'lat': 41.6162, 'lng': -70.4931, 'avg': 15.327800000000002}, {'sdev': 0.13567999999999927, 'min': 24.019, 'importance': 0.325, 'ip': ['68.86.90.217'], 'address': u'Mashpee, Barnstable County, Massachusetts, 02649, United States of America', 'times': [24.019, 24.214, 24.455, 24.155, 24.369], 'host': ['be-7015-cr01.newyork.ny.ibone.comcast.net'], 'max': 24.455, 'lat': 41.6162, 'lng': -70.4931, 'avg': 24.242399999999996}, {'sdev': 0.20208000000000012, 'min': 28.687, 'importance': 0.325, 'ip': ['68.86.85.25'], 'address': u'Mashpee, Barnstable County, Massachusetts, 02649, United States of America', 'times': [28.866, 29.203, 29.153, 28.718, 28.687], 'host': ['be-10102-cr02.ashburn.va.ibone.comcast.net'], 'max': 29.203, 'lat': 41.6162, 'lng': -70.4931, 'avg': 28.925400000000003}, {'sdev': 2.1282400000000004, 'min': 21.644, 'importance': 0.325, 'ip': ['68.86.85.70'], 'address': u'Mashpee, Barnstable County, Massachusetts, 02649, United States of America', 'times': [26.493, 28.149, 28.519, 28.839, 21.644], 'host': ['he-0-14-0-0-pe07.ashburn.va.ibone.comcast.net'], 'max': 28.839, 'lat': 41.6162, 'lng': -70.4931, 'avg': 26.7288}]
"""

"""
# IF NEEDED: address lookup http://pelias.mapzen.com/reverse?lat=41.6178&lon=-70.5147

# Do a Wikipedia Lookup Based on geolocation (Cape Cod, MA)
# http://api.geonames.org/findNearbyWikipedia?lat=41.618116&lng=-70.485361&username=demo
wikihtml = GET_REQUEST("http://api.geonames.org/findNearbyWikipedia?lat="+ str(lat) +"&lng="+ str(lng) + "&username=asolr")
wiki = ET.fromstring(wikihtml) # if you need the xml data type
print ET.tostring(wiki)
"""
