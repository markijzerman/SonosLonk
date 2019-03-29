# SonosLonk

Software used for installation of Studio LONK in collaboration with FRAME magazine as well as SONOS, for the Dutch Design Week 2018.
Latest updates are for the Wonderspaces 6-speaker version.

## Libraries
Needs:
* python3 on Stretch
* the Soco library to talk to Sonos speakers
* ADCPi library from ABElectronics. (github.com/abelectronicsuk/ABElectronics_Python_Libraries.git)

## Status & Shutdown
A status LED is connected to pin 8 (BCM14). uart is enables in /boot/config.txt:
	# Enable UART for status light on pin 8 (BCM14).
	enable_uart=1

Shutdown button is BCM21 and is watched in the Python code. After long press, it will turn off.

## Startup
* On startup the pi runs the two systemd files which are included.
* These can be checked with systemctl status *.service
* start_sonoslonk.service starts the http server after the network is up.
* start_sonoslonk_main.service waits for this http server, and then starts the rest.
* The script waits for all speakers to be connected.