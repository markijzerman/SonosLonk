#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals

import os
import sys
import time
import socket
import struct

from urllib.parse import quote

import soco
from soco.discovery import by_name, discover

from ADCPi import ADCPi

adc = ADCPi(0x68, 0x69, 12)

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
    try:
        if speaker1.get_current_transport_info()['current_transport_state'] != 'PLAYING':
            play_a_file(speaker1, file1)
    except:
        print("speaker1 does not exist so unable to play file")
    pass

    try:
        if speaker2.get_current_transport_info()['current_transport_state'] != 'PLAYING':
            play_a_file(speaker2, file2)
    except:
        print("speaker2 does not exist so unable to play file")
    pass

    try:
        if speaker3.get_current_transport_info()['current_transport_state'] != 'PLAYING':
            play_a_file(speaker3, file3)
    except:
        print("speaker3 does not exist so unable to play file")
    pass

    try:
        if speaker4.get_current_transport_info()['current_transport_state'] != 'PLAYING':
            play_a_file(speaker4, file4)
    except:
        print("speaker4 does not exist so unable to play file")
    pass

    try:
        if speaker5.get_current_transport_info()['current_transport_state'] != 'PLAYING':
            play_a_file(speaker5, file5)
    except:
        print("speaker5 does not exist so unable to play file")
    pass
    

### VARIABLES
httpserverport = 8000
file1 = 'FORESTGREEN.mp3'
file2 = 'FORESTGREEN.mp3'
file3 = 'VIVIDRED.mp3'
file4 = 'PALEYELLOW.mp3'
file5 = 'BABYPINK.mp3'
prev_a1 = 0
prev_a2 = 0
prev_a3 = 0
prev_a4 = 0
prev_a5 = 0
test_after_x_count = 0

### MAIN

print(detect_ip_address())

write("--- Trying to connect to Sonos speakers ---" + '\n')

try:
    speaker1 = by_name("speaker1")
    print("found: ", speaker1.player_name, speaker1)
except:
    print("speaker1 was not found")
pass

try:
    speaker2 = by_name("speaker2")
    print("found: ", speaker2.player_name, speaker2)
except:
    print("speaker2 was not found")
pass

try:
    speaker3 = by_name("speaker3")
    print("found: ", speaker3.player_name, speaker3)
except:
    print("speaker3 was not found")
pass

try:
    speaker4 = by_name("speaker4")
    print("found: ", speaker4.player_name, speaker4)
except:
    print("speaker4 was not found")
pass

try:
    speaker5 = by_name("speaker5")
    print("found: ", speaker5.player_name, speaker5)
except:
    print("speaker5 was not found")
pass

time.sleep(2)

write("--- Reading analog sensors ---" + '\n')

try:
    while True:
        a1 = int((adc.read_voltage(1)/5)*100)
        a2 = int((adc.read_voltage(2)/5)*100)
        a3 = int((adc.read_voltage(3)/5)*100)
        a4 = int((adc.read_voltage(4)/5)*100)
        a5 = int((adc.read_voltage(5)/5)*100)

        try:
            if a1 != prev_a1:
                prev_a1 = a1
                speaker1.volume = a1
                print("A1:", a1)
        except:
            print("speaker1 did not exist so not able to set volume")
        pass

        try:
            if a2 != prev_a2:
                prev_a2 = a2
                speaker2.volume = a2
                print("A2:", a2)
        except:
            print("speaker2 did not exist so not able to set volume")
        pass

        try:
            if a3 != prev_a3:
                prev_a3 = a3
                speaker3.volume = a3
                print("A3:", a3)
        except:
            print("speaker3 did not exist so not able to set volume")
        pass

        try:
            if a4 != prev_a4:
                prev_a4 = a4
                speaker4.volume = a4
                print("A4:", a4)
        except:
            print("speaker4 did not exist so not able to set volume")
        pass

        try:
            if a5 != prev_a5:
                prev_a5 = a5
                speaker5.volume = a5
                print("A5:", a5)
        except:
            print("speaker5 did not exist so not able to set volume")
        pass

##        print(a1, " ", a2, " ", a3, " ", a4, " ", a5)



        test_after_x_count += 1
        if test_after_x_count > 20:
            print("test if files are all playing")
            test_after_x_count = 0
            test_if_files_are_playing()
            
        time.sleep(0.01)
        
except KeyboardInterrupt:
    try:
        speaker1.pause()
    except:
        print("speaker1 does not exist so can not pause it.")
    pass
        
    try:
        speaker2.pause()
    except:
        print("speaker2 does not exist so can not pause it.")
    pass

    try:
        speaker3.pause()
    except:
        print("speaker3 does not exist so can not pause it.")
    pass

    try:
        speaker4.pause()
    except:
        print("speaker4 does not exist so can not pause it.")
    pass

    try:
        speaker5.pause()
    except:
        print("speaker5 does not exist so can not pause it.")
    pass



