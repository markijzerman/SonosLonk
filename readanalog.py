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
        a0 = int((analog_values[0]/5)*100)
        a1 = int((analog_values[1]/5)*100)
        a2 = int((analog_values[2]/5)*100)
        a3 = int((analog_values[3]/5)*100)

        print("%s %s %s %s " % (a0, a1, a2, a3))
        time.sleep(0.01)
        
except KeyboardInterrupt:
    pass
