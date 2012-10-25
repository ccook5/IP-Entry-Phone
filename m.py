#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import subprocess
import atexit
import commands

def giveout_info(str):
	print(str)

def setup_linphone():
	giveout_info("Seting up Linphone");

	if not check_if_linphone_is_running():
		subprocess.call(["/usr/bin/linphonecsh", "init"])

	if check_if_registered():
		print('already registered');
	else:

		giveout_info('\nRegistering');

		subprocess.call(["/usr/bin/linphonecsh", "register", 
				"--host",       "192.168.0.100",
				"--username",   "101",
				"--password",   "password"])
	print('done...\n\n');

def check_if_linphone_is_running():
	giveout_info('checking if linphone is allready running')
	output = subprocess.check_output(["/bin/ps", "-A"])

	if 'linphonec' in output:
		return True
	else:
		return False

	return False

def check_if_registered():
	str = ""
	try:
		str = subprocess.check_output(["/usr/bin/linphonecsh", "status", "register"]);
	except subprocess.CalledProcessError:
		pass

	print str

def unregister():
	print("Unregistering")
	subprocess.call(["/usr/bin/linphonecsh", "unregister"])

def make_call():

	try:
		print("Button Pressed");
		subprocess.call(["/usr/bin/linphonecsh", "generic", 
				"call sip:100@192.168.0.100"])
		c = 0

		while c < 60:
			subprocess.call(['/usr/bin/linphonecsh', 'status', 'hook']);
			time.sleep(2)
			c += 1
	except KeyboardInterrupt:
		print('Hanging up.');
		subprocess.call(["/usr/bin/linphonecsh", "generic", "terminate"])
		raise
	finally:
		print('Hanging up.');
		subprocess.call(["/usr/bin/linphonecsh", "generic", "terminate"])

def read_ip(pin):
	return subprocess.check_output(['/usr/local/bin/gpio', '-g', 'read', str(pin)])


if __name__ == '__main__':
	input_pin = 4

	GPIO.setmode(GPIO.BCM)
	GPIO.setup(input_pin, GPIO.IN)


	subprocess.call(['whoami'])
	atexit.register(unregister)
	setup_linphone()

	while True:
		#print('.'+read_ip(input_pin)+'.');
		if read_ip(input_pin) == '1\n':
			make_call()
			while read_ip(input_pin) == '1\n':
				time.sleep(0.1)

		

