import sys
import subprocess
import re

# TRACE ROUTE and PING analyzer

# REGULAR EXPRESSIONS
# (?=foo)	Lookahead
# (?<=foo)	Lookbehind
# (?!foo)	Negative Lookahead
# (?<!foo)	Negative Lookbehind

# get a command line address to trace/ping
if(len(sys.argv) > 1):
    host = sys.argv[1]
else:
    host= "centos.com" # should be located in Germany about 100 ms from USA

# ping: to see the total time along the route
pnum = 10
ping = subprocess.Popen(
    ["ping", "-c", str(pnum), host],
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE
)

print "Ping Millisecond Study of (" + host + ")" +  ") Tests: " + str(pnum)
print "(fastest, average, max, deviation)"
pingtext, error = ping.communicate()
# matcher for speeds (min,avg,max,mdev)
matcher = re.compile("(\d+.\d+)/(\d+.\d+)/(\d+.\d+)/(\d+.\d+)")
speeds = matcher.search(pingtext).groups()
print speeds #print pingtext

# traceroute: to collect timing info along this route

tnum = 5
traceroute = subprocess.Popen(
    ["traceroute", "-q", str(tnum), host],
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE
)

print "TraceRoute Millisecond Study of (" + host + ") Tests Per Node: " + str(tnum)
tracetext, error = traceroute.communicate()

# get all the ip address for the route
matcher = re.compile("(?<=\()\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?=\) )")
ips = matcher.findall(tracetext)
print ips #print tracetext

# get all the timing information for the route
matcher = re.compile("\d{1,3}\.\d{1,3}(?= ms)")
timeslist = matcher.findall(tracetext)
times = []
for time in timeslist:
    for test = 0; test < tnum; test++
print times

# get all the text domain names for the route
matcher = re.compile("(?<=  )[a-zA-Z0-9\-\.]+\.[a-zA-Z0-9]{1,5}(?= \()")
urls = matcher.findall(tracetext)
print urls
