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

"""
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
route = {"ip" : host, # TODO ask Todd maybe has ideas?
        "host": host,
        "min" : speeds[0],
        "avg" : speeds[1],
        "max" : speeds[2],
        "dev" : speeds[3]
        }

print route # verify all the timings are correct for the trace
"""
# traceroute: to collect timing info along this route

# function for calculating standard deviation
def sdev(data, avg):
    tdev = 0
    for dev in data:
        tdev += abs(dev-avg)
    return tdev/len(data)

# Todd: We would like to do something like this...
trace = []
def append_trace(ip, host, times):
    minimum = min(times)
    maximum = max(times)
    average = sum(times)/len(times)
    variance = sdev(times, average)

    ping = {"ip" : ip,
        "host" : host,
        "times": times,
        "min" : minimum,
        "avg" : average,
        "max" : maximum,
        "sdev" : variance
        #"address" : address,
        #"lat" : lat,
        #"lng" : lng
        }
    trace.append(ping)

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
        print ip
        print host
        print times
        append_trace(ip, host, times)

# now run a trace route since all the functions are setup
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
    parse_trace(line)
    print line.rstrip() # remove return at end of line
  else:
    break

print trace
