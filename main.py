#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

def setup_linphone():
	print("Seting up Linphone");

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
		
