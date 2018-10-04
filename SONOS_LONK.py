#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals

import os
import sys
import time
import socket
import struct
import threading

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


class test_if_files_are_playing(threading.Thread):
    def __init__(self):
        self.running = False
        super(test_if_files_are_playing, self).__init__()
        
    def start(self):
        self.running = True
        super(test_if_files_are_playing, self).start()

    def run(self):
        while self.running:
            try:
                for speakerName, speakerAddress in sonosList.items():
                    
                    port = 8000 + (int(speakerName[-1:]))
                    file = files[(int(speakerName[-1:])-1)]

                    if speakerAddress.get_current_transport_info()['current_transport_state'] != 'PLAYING':
                        print("Add URI to queue on " + speakerName)
                        for x in range (10):
                            speakerAddress.add_uri_to_queue('http://{}:{}/{}'.format(detect_ip_address(), port, file))
                        time.sleep(0.5)
                        speakerAddress.play()
                        print("Playing back on " + speakerName)
                        time.sleep(0.5)

                    else:
                        print(speakerName, " was already playing...")
                        time.sleep(2)

            except:
                pass

    def stop(self):
        self.running = False


### VARIABLES
sonosAmt = 5
sonosList = {}
http_port = 8000
files = ['GREEN.mp3', 'GREY.mp3', 'YELLOW.mp3', 'RED.mp3', 'PINK.mp3']
prev_a1 = 0
prev_a2 = 0
prev_a3 = 0
prev_a4 = 0
prev_a5 = 0
test_after_x_count = 0

### MAIN

print(detect_ip_address())

write("--- Trying to connect to Sonos speakers ---" + '\n')

# add sonos speakers to dict sonosList
try:
    for x in range(1, sonosAmt+1):
        sonosList['speaker{}'.format(x)] = by_name("speaker"+str(x))
except TypeError:
    print("one or more speakers are not available")

# available speakers are:
print(sonosList)

time.sleep(1)

write("--- Turning crossfade on, clearing queues, setting play mode ---" + '\n')

# for all speakers, stop them, set crossfade to true, clear the queue and set play mode to repeat all
for speakerName, speakerAddress in sonosList.items():
    try:
        print(speakerAddress)
        speakerAddress.stop()
        speakerAddress.cross_fade = True
        speakerAddress.clear_queue()
        speakerAddress.play_mode = 'REPEAT_ALL'
    except AttributeError:
        print("a speaker seems to be missing")
    time.sleep(0.5)

write("--- Starting audio check & play thread ---" + '\n')

# make a thread of the checking of the playing
checkPlayingThread = test_if_files_are_playing()
checkPlayingThread.daemon = True
checkPlayingThread.start()


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
                sonosList['speaker1'].volume = a1
                print("A1:", a1)
        except:
            print("speaker1 did not exist so not able to set volume")
        pass

        try:
            if a2 != prev_a2:
                prev_a2 = a2
                sonosList['speaker2'].volume = a2
                print("A2:", a2)
        except:
            print("speaker2 did not exist so not able to set volume")
        pass

        try:
            if a3 != prev_a3:
                prev_a3 = a3
                sonosList['speaker3'].volume = a3
                print("A3:", a3)
        except:
            print("speaker3 did not exist so not able to set volume")
        pass

        try:
            if a4 != prev_a4:
                prev_a4 = a4
                sonosList['speaker4'].volume = a4
                print("A4:", a4)
        except:
            print("speaker4 did not exist so not able to set volume")
        pass

        try:
            if a5 != prev_a5:
                prev_a5 = a5
                sonosList['speaker5'].volume = a5
                print("A5:", a5)
        except:
            print("speaker5 did not exist so not able to set volume")
        pass

            
        time.sleep(0.01)
        
except KeyboardInterrupt:
    print("quitting...")
    checkPlayingThread.stop()
    time.sleep(0.5)
    for speakerName, speakerAddress in sonosList.items():
        if speakerAddress.get_current_transport_info()['current_transport_state'] == 'PLAYING':
            speakerAddress.pause()
            speakerAddress.clear_queue()
            print("pausing & clearing " + speakerName)
        else:
            print(speakerName + " is already paused")



