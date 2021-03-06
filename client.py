from socket import *
import select
import sys
import struct
from scapy.all import get_if_addr
import time
import sys, tty, termios, fcntl
import getch
import ipaddress

#global variables
TCP_PORT = 0 
network_eth1 = '172.1.0.0/16'
network_eth2 = '172.99.0.0/16'
clientUdpPort = 13117

#all the colors in the code
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
    
#print the selection network API
inputCorrect = False
while inputCorrect == False:
    print(bcolors.UNDERLINE + bcolors.HEADER + bcolors.BOLD + 'please choose your virtual network:' + bcolors.ENDC)
    print(bcolors.HEADER + 'press 1 for dev network (eth1 - ' + network_eth1 + ')' + bcolors.ENDC)
    print(bcolors.HEADER + 'press 2 for dev network (eth2 - ' + network_eth2 + ')' + bcolors.ENDC)
    inputNetwork = input()
    if (inputNetwork == '1') | (inputNetwork == '2'):
        inputCorrect = True
    else:
        print(bcolors.FAIL + 'ERROR : you can only press 1 or 2, please try again' + bcolors.ENDC) 

#get the relevant state (network)      
if inputNetwork == '1':
    network = get_if_addr('eth1')+'/16'
elif inputNetwork == '2':
    network = get_if_addr('eth2')+'/16'       


#open the client UDP socket and start listening for game offers
client = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP) 
client.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
client.setsockopt(SOL_SOCKET, SO_REUSEADDR , 1)
ip = str(ipaddress.ip_network(network,False).broadcast_address)
client.bind((ip, clientUdpPort))
print(bcolors.WARNING +"Client started, listening for offer requests..." + bcolors.ENDC)

#main loop
while 1:
    try:
        #waiting for server pucket message
        message, (serverAddress,port) = client.recvfrom(2048)

        #the tcp port is in the sacond place in the pucket
        TCP_PORT = struct.unpack('I B H', message)[2]
        print(serverAddress, TCP_PORT)
        print(bcolors.OKGREEN + 'Recieved offer from ',serverAddress, ', attempting to connect...' + bcolors.ENDC)
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverAddress,TCP_PORT))
        teamName = 'EOE'
        
        #sending the team name
        clientSocket.send(teamName.encode())
        welcomeMessage = clientSocket.recv(2048)
        print(bcolors.OKCYAN + welcomeMessage.decode() + bcolors.ENDC)
    except:
        pass

    #Game mode!!!
    #100 sec loop of getting chars from client keyboard
    startTime = time.time()
    while 1: 
        try:
            c = getch.getch()
            print(str(c))
            clientSocket.sendall(str(c).encode())

            #check if 10 sec pass
            if time.time() - startTime > 10:
                print(bcolors.WARNING + 'Server disconnected, listening for offer requests...' + bcolors.ENDC)
                break
        except Exception as e:
            print(bcolors.WARNING + 'Server disconnected, listening for offer requests...' + bcolors.ENDC)
            break

client.close()
clientSocket.close()