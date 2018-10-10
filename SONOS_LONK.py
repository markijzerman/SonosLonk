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
                        for x in range (50):
                            speakerAddress.add_uri_to_queue('http://{}:{}/{}'.format(detect_ip_address(), port, file))
                        time.sleep(0.5)
                        speakerAddress.play_from_queue(1)
                        print("Playing back on " + speakerName)
                        time.sleep(0.5)

                    else:
                        print(speakerName, " was already playing...")
                        time.sleep(10)

            except Exception as e:
                print("something went wrong when sending URI to speaker:" + str(e))
                pass

    def stop(self):
        self.running = False


### VARIABLES
sonosAmt = 5
sonosList = {}
http_port = 8000
files = ['GREEN.mp3', 'GREY.mp3', 'YELLOW.mp3', 'RED.mp3', 'PINK.mp3']
analog = [0,0,0,0,0]
prev_analog = [0,0,0,0,0]
counter = 0
logarithmicScaling = 1
potRange = 1.48
x = 1


### MAIN

print(detect_ip_address())

write("--- Trying to connect to Sonos speakers ---" + '\n')

# add sonos speakers to dict sonosList
##try:
##    for x in range(1, sonosAmt+1):
##        sonosList['speaker{}'.format(x)] = by_name("speaker"+str(x))
##except TypeError:
##    print("one or more speakers are not available")

# add sonos speakers to dict sonosList
while len(sonosList) <= sonosAmt:
    try:
        sonosList['speaker{}'.format(x)] = by_name("speaker"+str(x))
        print(sonosList)
        if sonosList['speaker{}'.format(x)] != None:
            if x < sonosAmt:
                x = x+1
        sleep(0.5)
    except:
        print("still looking for more speakers...")
        time.sleep(2)

time.sleep(2)

print("all speakers found")

# available speakers are:
print(sonosList)

time.sleep(1)

write("--- Turning crossfade on, clearing queues, setting play mode, turn queue on ---" + '\n')

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

        for speakerName, speakerAddress in sonosList.items():
            try:
                curAnalogPortVoltage = adc.read_voltage(int(speakerName[-1:]))
                analog[(int(speakerName[-1:])-1)] = (curAnalogPortVoltage / 1.48) * 100
            except:
                print("something went wrong when setting the analog value")

            try:
                if analog[(int(speakerName[-1:])-1)] != prev_analog[(int(speakerName[-1:])-1)]:
                    prev_analog[(int(speakerName[-1:])-1)] = analog[(int(speakerName[-1:])-1)]
                    speakerAddress.volume = analog[(int(speakerName[-1:])-1)]

            except:
                print("not able to set volume on " + speakerName)

            pass

        counter += 1

        if counter > 5:
            print(analog)
            counter = 0
   
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



