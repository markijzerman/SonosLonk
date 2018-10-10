# SonosLonk

Software used for installation of Studio LONK in collaboration with FRAME magazine as well as SONOS, for the Dutch Design Week 2018.

## Libraries
Needs python3 on Stretch, the Soco library to talk to Sonos speakers, as well as ADCPi library from ABElectronics. (github.com/abelectronicsuk/ABElectronics_Python_Libraries.git

## Startup
On startup the pi runs the two systemd files which are included.
These can be checked with systemctl status *.service.
start_sonoslonk.service starts the http server after the network is up.
start_sonoslonk_main.service waits for this http server, and then starts the rest.
The script waits for all speakers to be connected.
