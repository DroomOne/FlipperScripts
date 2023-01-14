import serial 
from hexdump import hexdump
from colorama import init
from termcolor import cprint

init()
flipper = serial.Serial("COM3", timeout=1)
flipper.baudrate = 230400
flipper.flushOutput()
flipper.flushInput()

flipper.timeout = None

flipper.read_until(b'>: ')
flipper.write(b"storage read /ext/tama_p1/save.bin\r")
flipper.read_until(b'\n')
flipper.readline()

'''
>: storage read /ext/tama_p1/save.bin
Size: 68
Ķ ▒▒▒▒0▒▒▒▒▒ Q ▒▒▒▒▒ ▒W
                      ▒' ▒▒▒▒▒▒▒▒
>: PuTTY
'''

line = flipper.read_until(b'\x0D\x0A\x0D\x0A')[0:-4]
hexdump(line)
flipper.read_until(b'>: ')