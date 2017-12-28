import subprocess
import sys

import random
import time

def system(cmd, text):
    process = subprocess.Popen(
        [cmd, text],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print output.strip()
    rc = process.poll()
    return rc

domain = "ai.org"

system("whois", "ai.org")

delay = 3
timeDelay = random.randrange(0, delay)
print "delay " + str(timeDelay)
time.sleep(timeDelay)
