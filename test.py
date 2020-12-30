from socket import *
import select
import sys
import struct
from scapy.all import get_if_addr
import time
import sys, tty, termios
import getch

def getChar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch
print('start')
c = getch.getch()
print (c)
c = getch.getch()
print (c)
c = getch.getch()
print (c)