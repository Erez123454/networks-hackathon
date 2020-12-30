from socket import *
import select
import sys
import struct
from scapy.all import get_if_addr
import time
import sys, tty, termios, fcntl
import getch

def getChar():
    fd = sys.stdin.fileno()

    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)

    oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

    c = sys.stdin.read(1)

    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
    return c


TCP_PORT = 0

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
#wait to offer mode
inputCorrect = False
while inputCorrect == False:
    print(bcolors.UNDERLINE + bcolors.HEADER + bcolors.BOLD + 'please choose your virtual network:' + bcolors.ENDC)
    print(bcolors.HEADER + 'press 1 for dev network (eth1 - 172.1.0/24)' + bcolors.ENDC)
    print(bcolors.HEADER + 'press 2 for dev network (eth2 - 172.99.0/24)' + bcolors.ENDC)
    inputNetwork = input()
    if (inputNetwork == '1') | (inputNetwork == '2'):
        inputCorrect = True
    else:
        print(bcolors.FAIL + 'ERROR : you can only press 1 or 2, please try again' + bcolors.ENDC)
        
client = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP) 
client.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
client.setsockopt(SOL_SOCKET, SO_REUSEADDR , 1)

###################client.bind((get_if_addr('eth'+inputNetwork), 13117)) #UDP PORT is 13117
client.bind(('', 13117))
print (bcolors.WARNING + 'Client started , listening for offer requests...' + bcolors.ENDC)

while 1:
    rightServer = False
    
    while rightServer == False:
        try:
            message, (serverAddress,port) = client.recvfrom(2048)
            TCP_PORT = struct.unpack('I B H', message)[2]
            print(bcolors.OKGREEN + 'Recieved offer from ',serverAddress, ', attempting to connect...' + bcolors.ENDC)
            print(serverAddress, TCP_PORT)
            #connect to the TCP mode
            if serverAddress == '172.18.0.91':
                print(serverAddress, TCP_PORT)
                clientSocket = socket(AF_INET, SOCK_STREAM)
                clientSocket.connect((serverAddress,TCP_PORT))
                teamName = 'EOE'
                clientSocket.send(teamName.encode())
                rightServer=True
        except:
            pass

    #Game mode
    welcomeMessage = clientSocket.recv(2048)
    print(bcolors.OKCYAN + welcomeMessage.decode() + bcolors.ENDC)
    startTime = time.time()
    while 1: 
        try:
            #if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            #c= getChar()
                #c=str(c)+'\0'
                #print (bcolors.HEADER + c + bcolors.ENDC)   
            c = getch.getch()
            print(str(c))
            clientSocket.send(str(c).encode())
            if time.time() - startTime > 10:
                print(bcolors.WARNING + 'Server disconnected, listening for offer requests...' + bcolors.ENDC)
                break
                
        except:
            print(bcolors.WARNING + 'Server disconnected, listening for offer requests...' + bcolors.ENDC)
            break

client.close()
clientSocket.close()