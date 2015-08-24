# command.py

import sys
from subprocess import Popen

if len(sys.argv) < 2:
    print 'Usage: command.py "command to watch"'
    sys.exit(1)

cmd_line = sys.argv[1:]

p = Popen(cmd_line)
p.communicate()[0]
