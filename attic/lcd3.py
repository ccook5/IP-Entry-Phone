#!/usr/bin/python

import lcd2

if __name__ == '__main__':

    lcd = lcd2.HD44780()
    print('test')
    lcd.message("I'm a Raspberry Pi\n  Take a byte!")


