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

# hostname to check if any (command line hostname priority)
host = ""

# CONFIGURATION SETTINGS
pnum = 5 # number of pings to hostname/ip
tnum = 5 # number of pings per traceroute

try_openstreetmap=False
try_google=True

# store all the traceroute  and ping info
traceroute = []
ping = {}

# (command line hostname priority)
if(len(sys.argv) > 1):
    host = sys.argv[1]
else:
    host = "www.whoi.edu" #"boston.com" #"www.google.com" #"facebook.com" #"mit.edu" #"harvard.edu" #"wit.edu"

def main ():
    # ping = parse_ping(pyprocess("ping", "-c", str(pnum), host))
    pyprocess("traceroute", "-q", str(tnum), host)
    me = traceroute.pop(0) #the first address is localhost and it needs to be removed
    geocode_traceroute(traceroute)
    address_traceroute(traceroute)
    print traceroute


def pyprocess(proc, flag, num, iphost):
    ptext = ""
    pprocess = subprocess.Popen(
        [proc, flag, num, iphost],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )
    # read the process line by line
    while True:
      line = pprocess.stdout.readline()
      ptext += line;
      if line != '' and (re.search('(\* ){3,}', line) is None):
          if proc == "traceroute":
              parse_trace(line) #print line.rstrip()
          else: # ping type?
              print line.rstrip()
      else:
          break
    return ptext

# standardized GET request
def GET_REQUEST(address):
    timeout = 60
    socket.setdefaulttimeout(timeout)

    user_agent = 'Network Graph Research (Linux; Cape Cod, MA)'
    headers = { 'User-Agent' : user_agent }

    req = urllib2.Request(url = address, headers = headers)
    response = urllib2.urlopen(req)
    content = response.read()
    return content

def parse_ping(pingtext):
    # matcher for speeds (min,avg,max,mdev)
    matcher = re.compile("(\d+.\d+)/(\d+.\d+)/(\d+.\d+)/(\d+.\d+)")
    speeds = matcher.search(pingtext)
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
    return ping

# format and parse a line from a traceroute
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
        append_trace(ip[0], host[0], times)

# calculate standard deviation
def sdev(data, avg):
    tdev = 0
    for dev in data:
        tdev += abs(dev-avg)
    return tdev/len(data)

# add ip, host, times to traceroute
def append_trace(ip, host, times):
    minimum = min(times)
    maximum = max(times)
    average = sum(times)/len(times)
    variance = sdev(times, average)

    trace = {"ip" : ip,
        "host" : host,
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

# Get the IP ADDRESS Geo Location lat/lng
# https://geoiptool.com/en/?ip=128.128.76.17
def ip_geocode(ip_address):
    geohtml = GET_REQUEST("https://www.geoiptool.com/en/?ip=" + ip_address)
    matcher = re.compile("{lat: .*}")
    geo = matcher.search(geohtml).group()
    geo = geo.replace("lat","\"lat\"")
    geo = geo.replace("lng","\"lng\"")
    geo = json.loads(geo) # if you need the json data type
    lat = geo["lat"] #"41.618116"
    lng = geo["lng"] #"-70.485361"
    return [lat,lng]

def geocode_traceroute(traceroute):
    # blacklist = {"lng": "lat"}
    # wichita maybe okay: "-97.2251" : "37.7083"
    blacklist = {"-6.2597" : "53.3478", "-97.0" : "38.0", "-97.2251" : "37.7083"}
    for index in range(len(traceroute)):
        latlng = ip_geocode(traceroute[index]["ip"])
        lat = latlng[0]
        lng = latlng[1]
        if str(lng) not in blacklist:
            traceroute[index]["lat"] = lat
            traceroute[index]["lng"] = lng
        else: # blacklist / bogus location
            traceroute[index]["lat"] = ""
            traceroute[index]["lng"] = ""
        print traceroute[index]

# IP ADDRESS to lat/lng
# OpenStreetMap:  http://nominatim.openstreetmap.org/search?q=us+41.618116,-70.485361&format=json&addressdetails=1
# Google:  https://maps.googleapis.com/maps/api/geocode/json?latlng=41.618116,-70.485361&sensor=false&key=AIzaSyCLXuFbu3C5ekOorvP9mib_NX4g4gsh-8I
# IF NEEDED: address lookup http://pelias.mapzen.com/reverse?lat=41.6178&lon=-70.5147
# NOT ACCURATE ENOUGH YET (TODO) so we also use google geo location

def google_geocode(latlng):
    lat = latlng[0] # lat,lng not always in this order!
    lng = latlng[1]
    if(lat != "" and lng != ""):
        googlegeo = GET_REQUEST("https://maps.googleapis.com/maps/api/geocode/json?latlng="+str(lng)+","+ str(lat)+"&sensor=false&key=AIzaSyCLXuFbu3C5ekOorvP9mib_NX4g4gsh-8I")
        return json.loads(googlegeo)
    else:
        return None

def open_geocode(latlng):
    lat = latlng[0] # lat,lng not always in this order!
    lng = latlng[1]
    if(lat != "" and lng != ""):
        opengeo = GET_REQUEST("http://nominatim.openstreetmap.org/search?q=us+"+ str(lat) +","+ str(lng) + "&format=json&addressdetails=1")
        return json.loads(opengeo)
    else: 
        return None

def append_address_trace(address, index, type):
    if(address == None):
        traceroute[index]["address"] = ""
        return
    if(type == "open"): # address[0]["display_name"]
        traceroute[index]["address"] = address[0]["display_name"]
        if traceroute[index]["address"] != "United States of America":
            traceroute[index]["importance"] = address[0]["importance"]
        else: # TODO: unknown town
            traceroute[index]["importance"] = ""
        return
    if(type == "google" and (address["status"] == "OK")):
        if(len(address["results"]) > 1):
            traceroute[index]["address"] = address["results"][1]["formatted_address"]
        else:
            traceroute[index]["address"] = ""
        return
        
def address_traceroute(traceroute):
    for index in range(len(traceroute)):
        lng = traceroute[index]["lng"]
        lat = traceroute[index]["lat"]
        if(try_google):
            gaddress = google_geocode([lat,lng])
            append_address_trace(gaddress, index, "google")
        if(try_openstreetmap):
            oaddress = open_geocode([lat,lng])
            append_address_trace(oaddress, index, "open")
        print traceroute[index]

# start the program with
main()

"""
# FINAL DATA EXAMPLE:
[{'sdev': 1.9021599999999999, 'min': 8.61, 'importance': 0.325, 'ip': ['96.120.65.101'], 'address': u'Mashpee, Barnstable County, Massachusetts, 02649, United States of America', 'times': [8.61, 9.332, 9.738, 13.184, 13.195], 'host': ['96.120.65.101'], 'max': 13.195, 'lat': 41.6162, 'lng': -70.4931, 'avg': 10.8118}, {'sdev': 0.3321599999999997, 'min': 13.0, 'importance': 0.325, 'ip': ['68.87.154.77'], 'address': u'Mashpee, Barnstable County, Massachusetts, 02649, United States of America', 'times': [14.038, 13.0, 13.0, 13.0, 13.0], 'host': ['te-9-5-ur02.mashpee.ma.boston.comcast.net'], 'max': 14.038, 'lat': 41.6162, 'lng': -70.4931, 'avg': 13.2076}, {'sdev': 1.7760800000000014, 'min': 13.302, 'importance': 0.325, 'ip': ['68.85.37.93'], 'address': u'Mashpee, Barnstable County, Massachusetts, 02649, United States of America', 'times': [19.768, 15.097, 15.059, 13.413, 13.302], 'host': ['be-113-ar01.needham.ma.boston.comcast.net'], 'max': 19.768, 'lat': 41.6162, 'lng': -70.4931, 'avg': 15.327800000000002}, {'sdev': 0.13567999999999927, 'min': 24.019, 'importance': 0.325, 'ip': ['68.86.90.217'], 'address': u'Mashpee, Barnstable County, Massachusetts, 02649, United States of America', 'times': [24.019, 24.214, 24.455, 24.155, 24.369], 'host': ['be-7015-cr01.newyork.ny.ibone.comcast.net'], 'max': 24.455, 'lat': 41.6162, 'lng': -70.4931, 'avg': 24.242399999999996}, {'sdev': 0.20208000000000012, 'min': 28.687, 'importance': 0.325, 'ip': ['68.86.85.25'], 'address': u'Mashpee, Barnstable County, Massachusetts, 02649, United States of America', 'times': [28.866, 29.203, 29.153, 28.718, 28.687], 'host': ['be-10102-cr02.ashburn.va.ibone.comcast.net'], 'max': 29.203, 'lat': 41.6162, 'lng': -70.4931, 'avg': 28.925400000000003}, {'sdev': 2.1282400000000004, 'min': 21.644, 'importance': 0.325, 'ip': ['68.86.85.70'], 'address': u'Mashpee, Barnstable County, Massachusetts, 02649, United States of America', 'times': [26.493, 28.149, 28.519, 28.839, 21.644], 'host': ['he-0-14-0-0-pe07.ashburn.va.ibone.comcast.net'], 'max': 28.839, 'lat': 41.6162, 'lng': -70.4931, 'avg': 26.7288}]
"""

"""
# Do a Wikipedia Lookup Based on geolocation (Cape Cod, MA) http://api.geonames.org/findNearbyWikipedia?lat=41.618116&lng=-70.485361&username=demo
wikihtml = GET_REQUEST("http://api.geonames.org/findNearbyWikipedia?lat="+ str(lat) +"&lng="+ str(lng) + "&username=asolr")
wiki = ET.fromstring(wikihtml) # if you need the xml data type
print ET.tostring(wiki)
"""
