import socket
import threading
import time
import itertools
import struct
import random
import copy
import ipaddress
from scapy.all import get_if_addr


mostCharsTaps = []
mostCharsTaps = [0 for i in range(128)] 
random.seed(1)
TCP_PORT = 0
network_eth1 = '172.1.0.0/16'
network_eth2 = '172.99.0.0/16'


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

 #statistics
def getMostCommonChar():   
    try:
        maxChar = max(mostCharsTaps)
        result = []
        for i in range(len(mostCharsTaps)):
            if mostCharsTaps[i] == maxChar:
                #for each result check if max
                result.append(chr(i))   
        return [result,maxChar]
    except:
        return [0,' ']


def printStatistics(maxTapsfun):
    try:
        #get the max value from the last game
        val1=max(next(copy.copy(counterG1)),0)
        val2=max(next(copy.copy(counterG2)),0)
        maxVal =  max(val1,val2)
        print(bcolors.OKGREEN + bcolors.BOLD + bcolors.UNDERLINE + "Statistic:" + bcolors.ENDC)
        if (maxTapsfun < maxVal):
            #get the max char
            maxTapsfun = maxVal 
        if(maxTapsfun > 0 ):
            [commonCharacter , numberOfChars] = getMostCommonChar()
            print(bcolors.OKGREEN + 'The most common pressed chars are :',commonCharacter,'-', numberOfChars, ' times!' + bcolors.ENDC)
        print(bcolors.OKGREEN + 'Best group ever tapped: ' + str(maxTapsfun) + ' taps! can you beat them?\n' + bcolors.ENDC)
    except:
        pass
    return maxTapsfun


#thread that responsible for the udp connection and broadcasting
def thread_udp(inputNetwork):
    try:
        if inputNetwork == '1':
            network = network_eth1
        elif inputNetwork == '2':
            network = network_eth2
        
        #define and open server udp broadcast socket
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        server.settimeout(0.2)
        message = struct.pack('I B H', 0xfeedbeef, 0x2, TCP_PORT)    
        #check if in regular state or test state
        if inputNetwork == '1':
            print (bcolors.WARNING + 'Server started listening on ip address 172.1.0.91' + bcolors.ENDC)
        elif inputNetwork == '2':
            print (bcolors.WARNING + 'Server started listening on ip address 172.99.0.91' + bcolors.ENDC)
        
        #get the relevant ip for the current state
        ip = str(ipaddress.ip_network(network,False).broadcast_address) 

        # i is index for 10 seconds
        i=0

        while 1:
            #broadcasting for all the clients
            server.sendto(message, (ip, 13117))    
            i+=1
            #after 10 seconds stop
            if(i==10):  
                break   
            time.sleep(1)
    except:
        pass
    server.close()

#thread that responsible for the tcp connection and the client sockets
def thread_tcp():
    serverSocket.settimeout(10)
    connections=[]
    teams=[]
    while 1:
        try:
            #get new socket for new client
            connectionSocket, addr = serverSocket.accept() 
            #save the team name
            teamName = connectionSocket.recv(2048)  
            print(teamName.decode())
            teams.append(teamName.decode())
            connections.append(connectionSocket)    
        except :
            #after 10 seconds start the game
            startGame(teams,connections)    
            break
    print (bcolors.WARNING + '\nGame over, sending out offer requests...' + bcolors.ENDC)  

def startGame(teams, connections):
    try:
        try:
            group1 = []
            group2 = []

            #divide the clients to 2 groups
            for i in range(len(teams)) :    
                if i % 2 == 0:
                    group1.append(teams[i])
                else:
                    group2.append(teams[i])

            #prepare the welcome messege
            welcomeMessage='Welcome to Keyboard Spamming Battle Royale.\nGroup 1: \n==\n'
            for g in group1:
                welcomeMessage+=str(g) + '\n'
            welcomeMessage+='\nGroup 2: \n==\n'
            for g in group2:
                welcomeMessage+=str(g) + '\n'
            welcomeMessage+='\nStart pressing keys on your keyboard as fast as you can!!\n'
        except:
            pass
        try:
            threads=[]
            for i in range(len(connections)):
                #each client open new thread
                thread= threading.Thread(target=listenToClient,args=(i,connections[i],welcomeMessage))
                threads.append(thread) 
                thread.start()
                
            for thread in threads:
                #main thread waits for all clients
                thread.join()       
        except:
            pass

        val1=max(next(copy.copy(counterG1)),0)
        val2=max(next(copy.copy(counterG2)),0)
        
        #prepare game over messege
        print (bcolors.WARNING + bcolors.BOLD + '\nGame over!' + bcolors.ENDC)
        print (bcolors.FAIL + 'Group 1 typed in ',val1, ' characters. Group 2 typed in ',val2, 'characters.' + bcolors.ENDC)
        
        #get the winner and print a message of him
        if (val1 > val2):
            print (bcolors.OKGREEN + bcolors.BOLD + bcolors.UNDERLINE + 'Group 1 wins!' + bcolors.ENDC)
            print()
            print (bcolors.OKGREEN + 'Congratulations to the winners:' + bcolors.ENDC)
            print (bcolors.OKGREEN + '==' + bcolors.ENDC)
            for g in group1:
                print (bcolors.OKGREEN + g + bcolors.ENDC)
        else: 
            print (bcolors.OKGREEN + bcolors.BOLD + bcolors.UNDERLINE + 'Group 2 wins!' + bcolors.ENDC)
            print()
            print (bcolors.OKGREEN + 'Congratulations to the winners:' + bcolors.ENDC)
            print (bcolors.OKGREEN + '==' + bcolors.ENDC)
            for g in group2:
                print (bcolors.OKGREEN + str(g) + bcolors.ENDC)
    except:
        pass

#each thread initilized with this function that listen to the client
def listenToClient(groupNumber,connection,welcomeMessage):
    try:
        connection.settimeout(10)
        connection.send(welcomeMessage.encode())

        # 10 sec loop of getting chars from the clinet
        curr= time.time()
        while time.time() < curr+10: 
            try:
                charTyped = connection.recv(2048)
                try:
                    charTypedDecode = charTyped.decode()
                    chars[ord(charTypedDecode)]+=1
                except:
                    if groupNumber == 1:
                        next(counterG1)
                    else:
                        next(counterG2)
                if groupNumber == 1:
                    next(counterG1)
                else:
                    next(counterG2)
            except :
                break
    except:
        pass
    connection.close()

#setting for the server socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', 0))
serverSocket.listen(1)
TCP_PORT = serverSocket.getsockname()[1]

inputCorrect = False
inputNetwork = ''
while inputCorrect == False:
    #get the relevant state (network)
    print(bcolors.UNDERLINE + bcolors.HEADER + bcolors.BOLD + 'please choose your virtual network:' + bcolors.ENDC)
    print(bcolors.HEADER + 'press 1 for dev network (eth1 - 172.1.0.0/24)' + bcolors.ENDC)
    print(bcolors.HEADER + 'press 2 for dev network (eth2 - 172.99.0.0/24)' + bcolors.ENDC)
    inputNetwork = input()
    if (inputNetwork == '1') | (inputNetwork == '2'):
        inputCorrect = True
    else:
        print(bcolors.FAIL + 'ERROR : you can only press 1 or 2, please try again' + bcolors.ENDC)

maxTappsPerGroup = 0

#main loop
while 1: 
    try:              
        counterG1 =itertools.count()
        counterG2 = itertools.count()
        tcp = threading.Thread(target=thread_tcp)
        udp = threading.Thread(target=thread_udp, args=(inputNetwork)) 
        tcp.start()
        udp.start()
        tcp.join()
        udp.join()
        #update the max tap and print statistics
        maxTappsPerGroup = printStatistics(maxTappsPerGroup)
    except:
        pass