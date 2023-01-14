import serial 
import os 
from colorama import init
from termcolor import cprint

init()
flipper = serial.Serial("COM3", timeout=1)
flipper.baudrate = 230400
flipper.flushOutput()
flipper.flushInput()

flipper.timeout = None

flipper.read_until(b'>: ')

flipper.write(b"log\r")
flipper.read_until(b'\n')
 
while flipper.is_open: 
    line = flipper.readline().rstrip()
    strline = line.decode('utf-8')

    cprint(strline)
    if 'Finished Writing' in strline:
        break
