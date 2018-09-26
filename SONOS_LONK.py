#!/usr/bin/env python

import os
import sys
import time
import socket
import struct

from urllib.parse import quote


from envirophat import analog
import soco
from soco.discovery import by_name, discover

def write(line):
    sys.stdout.write(line)
    sys.stdout.flush()

def detect_ip_address():
    """Return the local ip-address"""
    # Rather hackish way to get the local ip-address, recipy from
    # https://stackoverflow.com/a/166589
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address

def play_a_file(speaker, file):
    speaker.play_uri('http://{}:{}/{}'.format(detect_ip_address(), httpserverport, file))

def test_if_files_are_playing():
    # if it's not playing a file, play it now!
    if speaker1.get_current_transport_info()['current_transport_state'] != 'PLAYING':
        play_a_file(speaker1, file1)
    

### VARIABLES
httpserverport = 8000
file1 = 'mpthreetest.mp3'
file2 = ''
file3 = ''
file4 = ''
prev_a0 = 0
prev_a1 = 0
prev_a2 = 0
prev_a3 = 0
test_after_x_count = 0

### MAIN

print(detect_ip_address())

write("--- Trying to connect to Sonos speakers ---" + '\n')
speaker1 = by_name("speaker1")
print("found: ", speaker1.player_name, speaker1)

time.sleep(2)

write("--- Reading analog sensors ---" + '\n')

try:
    while True:
        analog_values = analog.read_all()
        a0 = int((analog_values[0]/5)*100)
        a1 = int((analog_values[1]/5)*100)
        a2 = int((analog_values[2]/5)*100)
        a3 = int((analog_values[3]/5)*100)
        
        if a0 != prev_a0:
            prev_a0 = a0
            speaker1.volume = a0
            print("A0:", a0)

##        if a1 != prev_a1:
##            prev_a1 = a1
##            speaker2.volume = a1
##            print("A1:", a1)
##
##        if a2 != prev_a2:
##            prev_a2 = a2
##            speaker3.volume = a2
##            print("A2:", a2)
##
##        if a3 != prev_a3:
##            prev_a3 = a3
##            speaker4.volume = a3
##            print("A3:", a3)

        test_after_x_count += 1
        if test_after_x_count > 50:
            test_after_x_count = 0
            test_if_files_are_playing()
            
        time.sleep(0.01)
        
except KeyboardInterrupt:
    speaker1.pause()
##    speaker2.pause()
##    speaker3.pause()
##    speaker4.pause()
    
    pass
