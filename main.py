#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

input_pin = 4

GPIO.setmode(GPIO.BCM)

GPIO.setup(input_pin, GPIO.IN)

while True:
	if not GPIO.input(input_pin):
		print("Button Pressed")
		while not GPIO.input(input_pin):
			time.sleep(0.1)
		
