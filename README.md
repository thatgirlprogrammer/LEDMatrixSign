This project is based on Henner Zeller's fantastic project to control LED matrices https://github.com/hzeller/rpi-rgb-led-matrix.  We bought most of the materials from Adafruit, except we found an Adafruit kit that Arrow Electronics had added a free Raspberry pi 3, so we went with that.

We decided to start with the python samples since they looked pretty simple, and even when we extended them, the performance seemed OK, so for now we're sticking with that.  We also stuck with the same structure as the samples, but we wanted to be able to specify graphics and text to display outside the program so we didn't have to change the code every time.  A quick way to get that feature was just to read the info from a file.  We plan to move the info to a database and maybe have a web server running on the pi that allows us to edit the data, but for right now we're still using the file.

#Getting Started

Start by setting up your pi with the latest version of Raspian.

###Fix mouse problem
	https://www.raspberrypi.org/forums/viewtopic.php?f=28&t=84999
###Raspian Config
```
sudo raspi-config
	expand filesystem
	change password
	optional - set boot option console or GUI
	internationalization options
		change locale - en_US.UTF-8 UTF-8
			change default locale
		keyboard layout
		change timezone
	advanced options
		SSH
```
###Update the System
plug in ethernet cable
```
sudo apt-get update
sudo apt-get upgrade - takes a while
```
config wifi
	sometimes the GUI just works, but if not:
	pi@raspberrypi:~ $ sudo nano /etc/wpa_supplicant/wpa_supplicant.conf 
		ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
		update_config=1
		country=US

		network={
				ssid="ASUS"
				psk="passwordHere"
				key_mgmt=WPA-PSK
		}

	sudo service networking restart
	sudo ifup wlan0

You should now have a nice working pi.

#Install the RGB matrix library

Follow the instructions at https://github.com/hzeller/rpi-rgb-led-matrix.
Run some samples and make sure the library is working.

#Install Sign Code

To work with the matrix library, we want to install the sign code in the python directory.  

	cd rpi-rgb-led-matrix/python
	git clone github.com/thatgirlprogramer/LEDMatrixSign.git

	cd LEDMatrixSign

	sudo python sign2.py -c 5

This is for a chain of 5 panels.


