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
        ACTIVATE GOOGLE API KEY: https://console.developers.google.com/project
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
    host = "www.whoi.edu" #"boston.com" #"www.google.com" #"facebook.com" #"mit.edu" #"harvard.edu" #"wit.edu" #"capecod.edu"

def main ():
    # ping = parse_ping(pyprocess("ping", "-c", str(pnum), host))
    pyprocess("traceroute", "-q", str(tnum), host)
    me = traceroute.pop(0) #the first address is localhost and it needs to be removed
    geocode_traceroute(traceroute)
    address_traceroute(traceroute)
    print traceroute

def pyprocess(proc, flag, num, iphost):
    total_failed = 2
    failed = 0
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
      if re.search('(\* ){3,}', line):
        failed += 1
      elif line:
        failed = 0
        if proc == "traceroute":
            parse_trace(line) #print line.rstrip()
        else: # ping type?
            print line.rstrip()
      else:
        break
      if failed > total_failed:
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
    else:
        print line # print the bad traceroute case to the screen

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
    distance = average*5000

    minimum = round(minimum, 2)
    maximum = round(maximum, 2)
    average = round(average, 2)
    variance = round(variance, 2)
    distance = round(distance, 2)

    trace = {"ip" : ip,
       # "host" : host,
       # "times": times,
       # "min" : minimum,
        "avg" : average,
        "dist" : distance,
       # "max" : maximum,
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
    latlng = matcher.search(geohtml).group()
    latlng = latlng.replace("lat","\"lat\"")
    latlng = latlng.replace("lng","\"lng\"")
    latlng = json.loads(latlng) 
    return latlng

def geocode_traceroute(traceroute):
    # blacklist = {"lng": "lat"}
    # wichita maybe okay: "-97.2251" : "37.7083"
    # "-0.071389" : "-75.250973" = Antarctica
    blacklist = {"-6.2597" : "53.3478", "-97.0" : "38.0", "-97.2251" : "37.7083", "-0.071389" : "-75.250973"}
    for index in range(len(traceroute)):
        latlng = ip_geocode(traceroute[index]["ip"])
        lat = latlng["lat"]
        lng = latlng["lng"]
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
    lat = latlng["lat"] 
    lng = latlng["lng"]
    if(lat != "" and lng != ""):
        googlegeo = GET_REQUEST("https://maps.googleapis.com/maps/api/geocode/json?latlng="+str(lng)+","+ str(lat)+"&sensor=false&key=AIzaSyCLXuFbu3C5ekOorvP9mib_NX4g4gsh-8I")
        return json.loads(googlegeo)
    else:
        return ""

def open_geocode(latlng):
    lat = latlng["lat"] 
    lng = latlng["lng"]
    if(lat != "" and lng != ""):
        opengeo = GET_REQUEST("http://nominatim.openstreetmap.org/search?q=us+"+ str(lat) +","+ str(lng) + "&format=json&addressdetails=1")
        return json.loads(opengeo)
    else:
        return ""

def address_traceroute(traceroute):
    for index in range(len(traceroute)):
        latlng = {"lng" : traceroute[index]["lng"], "lat" : traceroute[index]["lat"]}
        if(try_google):
            gaddress = google_geocode(latlng)
            traceroute[index]["address"] = gaddress
        if(try_openstreetmap):
            oaddress = open_geocode(latlng)
            traceroute[index]["address"] = oaddress
        print traceroute[index]

# add time stamp

# start the program with
main()

"""
# Do a Wikipedia Lookup Based on geolocation (Cape Cod, MA) http://api.geonames.org/findNearbyWikipedia?lat=41.618116&lng=-70.485361&username=demo
wikihtml = GET_REQUEST("http://api.geonames.org/findNearbyWikipedia?lat="+ str(lat) +"&lng="+ str(lng) + "&username=asolr")
wiki = ET.fromstring(wikihtml) # if you need the xml data type
print ET.tostring(wiki)
"""
