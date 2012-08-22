IP-Entry-Phone
==============

An open source ip entry phone. Uses Raspberry pi, a usb sound card, and an analog entry phone panel. The actual SIP connection is handled by linphone. We use a bit of simple electronics and a python script hosted here to glue it all together.

Installation
------------

// update linux to latest version
// this might be best left to the admin?
sudo apt-get update
sudo apt-get upgrade

// install python-dev
sudo apt-get install python-dev


//download RPI.GPIO + install
wget http://pypi.python.org/packages/source/R/RPi.GPIO/RPi.GPIO-0.3.1a.tar.gz#md5=1588ebc23872ce281b846a9f01d389af

tar -zxvf RPi.GPIO-0.3.1.tar.gz
cd RPi.GPIO-0.3.1a
python setup.py install

// install linphone
sudo apt-get install linphone