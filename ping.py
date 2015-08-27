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
    host= "boston.com" # should be located in Germany about 100 ms from USA


# ping: to see the total time along the route
pnum = 5 # number of pings to test
pingtext = ""
ping = subprocess.Popen(
    ["ping", "-c", str(pnum), host],
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE
)

# read the process line by line
while True:
  line = ping.stdout.readline()
  pingtext += line;
  if line != '':
    #the real code does filtering here
    print line.rstrip()
  else:
    break

# matcher for speeds (min,avg,max,mdev)
matcher = re.compile("(\d+.\d+)/(\d+.\d+)/(\d+.\d+)/(\d+.\d+)")
# save the speeds for the ping test
speeds = matcher.search(pingtext).groups()

# the ping times are for the FULL traceroute
trace = {"ip" : host, # TODO ask Todd maybe has ideas?
        "host": host,
        "min" : speeds[0],
        "avg" : speeds[1],
        "max" : speeds[2],
        "dev" : speeds[3]
        }

print trace # verify all the timings are correct for the trace

# traceroute: to collect timing info along this route

tnum = 5
traceroute = subprocess.Popen(
    ["traceroute", "-q", str(tnum), host],
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE
)

# read the traceroute process line by line
tracetext = ""
while True:
  # TODO if you we see "* * *" quit the loop regex
  line = traceroute.stdout.readline()
  tracetext += line;
  # if we see 3 or more *'s in a row break
  if line != '' and (re.search('(\* ){3,}', line) is None):
    #the real code does filtering here
    print line.rstrip() # remove return at end of line
  else:
    break

# get all the ip address for the route
matcher = re.compile("(?<=\()\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?=\) )")
ips = matcher.findall(tracetext)
print ips #print tracetext

# get all the timing information for the route
matcher = re.compile("\d{1,3}\.\d{1,3}(?= ms)")
times = matcher.findall(tracetext)
print times

# get all the text domain names for the route
matcher = re.compile("(?<=  )[a-zA-Z0-9\-\.]+\.[a-zA-Z0-9]{1,5}(?= \()")
hosts = matcher.findall(tracetext)
print hosts

# Todd: We would like to do something like this...
route = []
for index, ip in enumerate(ips):

    ping = {"ip" : ip,
        "host" : hosts[index]
        #"min" : min,
        #"avg" : avg,
        #"max" : max,
        #"dev" : dev,
        #"address" : address,
        #"lat" : lat,
        #"lng" : lng
        }

    route.append(ping)

print route
