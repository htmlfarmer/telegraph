import urllib
import urllib2
import socket # needed for timeout

# POST REQUEST

# timeout in seconds
timeout = 60
socket.setdefaulttimeout(timeout)

url = 'http://localhost'
port = 9999
address = url + ":" + str(port)

user_agent = 'Python (Linux; CentOS)'
values = {'name' : 'Asher Martin',
          'location' : 'Cape Cod',
          'phone' : '773-321-9191' }
headers = { 'User-Agent' : user_agent }

# If you do not pass the data argument, urllib2 uses a GET request
data = urllib.urlencode(values)
req = urllib2.Request(address, data, headers)
response = urllib2.urlopen(req)
the_page = response.read()
print the_page
