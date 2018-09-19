#!/usr/bin/env python

import sys
import time

from envirophat import analog
import soco

def write(line):
    sys.stdout.write(line)
    sys.stdout.flush()


write("--- Trying to connect to Sonos speakers ---" + '\n')
sonos1 = soco.discovery.any_soco()
# sonos1.volume += 10
write("--- NO SONOS SPEAKERS FOUND... continuing... ---" + '\n')

time.sleep(2)

write("--- Reading analog sensors ---" + '\n')



try:
    while True:
        analog_values = analog.read_all()
        a0 = analog_values[0]
        a1 = analog_values[1]
        a2 = analog_values[2]
        a3 = analog_values[3]

        print("%s %s %s %s " % (a0, a1, a2, a3))
        time.sleep(0.01)
        
except KeyboardInterrupt:
    pass
