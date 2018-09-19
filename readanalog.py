#!/usr/bin/env python

import sys
import time

from envirophat import analog

def write(line):
    sys.stdout.write(line)
    sys.stdout.flush()

write("--- Reading analog sensors ---")

try:
    while True:
        analog_values = analog.read_all()
        unit = unit,
        a0 = analog_values[0]
        a1 = analog_values[1]
        a2 = analog_values[2]
        a3 = analog_values[3]

        print(a0)
        time.sleep(1)
        
except KeyboardInterrupt:
    pass
