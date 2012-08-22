#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import subprocess

def setup_linphone():
	print("Seting up Linphone");
	subprocess.call(["linphonecsh", "init"])
	subprocess.call(["linphonecsh", "register", 
			"--host",       "192.168.0.106",
			"--username",   "test",
			"--password",   "password"])

def make_call():
	print("Button Pressed");

input_pin = 4

GPIO.setmode(GPIO.BCM)

GPIO.setup(input_pin, GPIO.IN)

while True:
	if not GPIO.input(input_pin):
		make_call()
		while not GPIO.input(input_pin):
			time.sleep(0.1)
		
