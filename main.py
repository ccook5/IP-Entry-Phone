#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import subprocess
import atexit

def setup_linphone():
	print("Seting up Linphone");
	subprocess.call(["linphonecsh", "init"])
	subprocess.call(["linphonecsh", "register", 
			"--host",       "192.168.0.106",
			"--username",   "101",
			"--password",   "password"])

def unregister():
	print("Unregistering")
	subprocess.call(["linphonecsh", "unregister"])

def make_call():
	print("Button Pressed");
	subprocess.call(["linphonecsh", "generic", 
			'"call sip:100@192.168.0.100"'])


input_pin = 4

GPIO.setmode(GPIO.BCM)

GPIO.setup(input_pin, GPIO.IN)

atexit.register(unregister)
setup_linphone()

while True:
	if not GPIO.input(input_pin):
		make_call()
		while not GPIO.input(input_pin):
			time.sleep(0.1)
		
