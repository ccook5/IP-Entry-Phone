#!/usr/bin/python
#
# HD44780 LCD Test Script for
# Raspberry Pi
#
# Author : Matt Hawkins
# Site   : http://www.raspberrypi-spy.co.uk
# 
# Date   : 26/07/2012
#
# Modified by Chris Cook to use gpio program, so we don't need to be run as root
#

# The wiring for the LCD is as follows:
# 1 : GND
# 2 : 5V
# 3 : Contrast (0-5V)*
# 4 : RS (Register Select)
# 5 : R/W (Read Write)       - GROUND THIS PIN
# 6 : Enable or Strobe
# 7 : Data Bit 0             - NOT USED
# 8 : Data Bit 1             - NOT USED
# 9 : Data Bit 2             - NOT USED
# 10: Data Bit 3             - NOT USED
# 11: Data Bit 4
# 12: Data Bit 5
# 13: Data Bit 6
# 14: Data Bit 7
# 15: LCD Backlight +5V**
# 16: LCD Backlight GND

#import
import time
import subprocess

def setup_pin(pin_no, dir):
	subprocess.call(['gpio', '-g', 'mode', str(pin_no), dir])
  
def gpio_output(pin_no, value):
	if value == False or value == 0:
		value = 0
	elif value == True or value == 1:
		value = 1
	else:
		# we should throw an exception
		return -1
	subprocess.call(['gpio', '-g', 'write', str(pin_no), str(value)])
	
def gpio_input(pin):
        return subprocess.check_output(['gpio', '-g', 'read', str(pin)])

	
class LCD:
	def __init__(self, width=16, enable=8, reg_sel=7, d4=25, d5=24, d6=25, d7=18):
		self.width   = width
		self.enable  = enable
		self.reg_sel = reg_sel
		self.d4      = d4
		self.d5      = d5
		self.d6      = d6
		self.d7      = d7
		
# Define some device constants
		self.LCD_WIDTH = 16    # Maximum characters per line
		self.LCD_CHR = True
		self.LCD_CMD = False

		self.LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
		self.LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line 

		# Timing constants
		self.E_PULSE = 0.00005
		self.E_DELAY = 0.00005
		
		setup_pin(self.enable,  'out') # E
		setup_pin(self.reg_sel, 'out') # RS
		setup_pin(self.d4,      'out') # DB4
		setup_pin(self.d5,      'out') # DB5
		setup_pin(self.d6,      'out') # DB6
		setup_pin(self.d7,      'out') # DB7

	# Initialise display
		self.lcd_init()


	def lcd_init(self):
		# Initialise display
		self.lcd_byte(0x33,self.LCD_CMD)
		self.lcd_byte(0x32,self.LCD_CMD)
		self.lcd_byte(0x28,self.LCD_CMD)
		self.lcd_byte(0x0C,self.LCD_CMD)  
		self.lcd_byte(0x06,self.LCD_CMD)
		self.lcd_byte(0x01,self.LCD_CMD)  


	def lcd_byte(self, bits, mode):
		# Send byte to data pins
		# bits = data
		# mode = True  for character
		#        False for command

		gpio_output(self.reg_sel, mode) # RS

		# High bits
		gpio_output(self.d4, False)
		gpio_output(self.d5, False)
		gpio_output(self.d6, False)
		gpio_output(self.d7, False)
		if bits&0x10==0x10:
			gpio_output(self.d4, True)
		if bits&0x20==0x20:
			gpio_output(self.d5, True)
		if bits&0x40==0x40:
			gpio_output(self.d6, True)
		if bits&0x80==0x80:
			gpio_output(self.d7, True)

		# Toggle 'Enable' pin
		time.sleep(self.E_DELAY)    
		gpio_output(self.enable, True)  
		time.sleep(self.E_PULSE)
		gpio_output(self.enable, False)  
		time.sleep(self.E_DELAY)      

		# Low bits
		gpio_output(self.d4, False)
		gpio_output(self.d5, False)
		gpio_output(self.d6, False)
		gpio_output(self.d7, False)

		if bits&0x01==0x01:
			gpio_output(self.d4, True)
		if bits&0x02==0x02:
			gpio_output(self.d5, True)
		if bits&0x04==0x04:
			gpio_output(self.d6, True)
		if bits&0x08==0x08:
			gpio_output(self.d7, True)

		# Toggle 'Enable' pin
		time.sleep(self.E_DELAY)    
		gpio_output(self.enable, True)  
		time.sleep(self.E_PULSE)
		gpio_output(self.enable, False)  
		time.sleep(self.E_DELAY)   

	def lcd_string(self, message, line):
		# Send string to display

		message = message.ljust(self.LCD_WIDTH," ")  

		if (line == 1):
			self.lcd_byte(self.LCD_LINE_1, self.LCD_CMD)
		else:
			self.lcd_byte(self.LCD_LINE_2, self.LCD_CMD)
		
		for i in range(self.LCD_WIDTH):
			self.lcd_byte(ord(message[i]),self.LCD_CHR)
	
def main():
	# Main program block

	lcd = LCD()
	
	# Send some test
	lcd_string("Rasbperry Pi", 1)
	lcd_string("Model B", 2)

	time.sleep(3) # 3 second delay

	# Send some text
	lcd_string("Raspberrypi-spy", 1)
	lcd_string(".co.uk", 2)

	time.sleep(20)


if __name__ == '__main__':
	main()


