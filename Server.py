import socket
import threading
import time
import itertools
import struct
import random
import copy
import ipaddress


chars = []
chars = [0 for i in range(128)] 
random.seed(1)
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


def getMostCommonChar():
    maxChar = max(chars)
    result = []
    for i in range(len(chars)):
        if chars[i] == maxChar:
            result.append(chr(i))
    return [result,maxChar]

def printStatistics(maxTapsfun):
    if maxTapsfun > 0:
        print(bcolors.OKGREEN + bcolors.BOLD + bcolors.UNDERLINE + "Statistic:" + bcolors.ENDC)
        [commonCharacter , numberOfChars] = getMostCommonChar()
        print(bcolors.OKGREEN + 'The most common pressed chars are :',commonCharacter,'-', numberOfChars, ' times!' + bcolors.ENDC)
        val1=max(next(copy.copy(counterG1)),0)
        val2=max(next(copy.copy(counterG2)),0)
        maxVal =  max(val1,val2)
        if maxTapsfun < maxVal:
            maxTapsfun = maxVal
    print(bcolors.OKGREEN + 'Best group ever tapped: ' + str(maxTapsfun) + ' taps! can you beat them?\n' + bcolors.ENDC)
    return maxTapsfun



def thread_udp(inputNetwork):
    if inputNetwork == '1':
        network = '172.18.0.0/16'
    elif inputNetwork == '2':
        network = '172.99.0.0/16'
    
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server.settimeout(0.2)
    message = struct.pack('I B H', 0xfeedbeef, 0x2, TCP_PORT)
    i=0
    print (bcolors.WARNING + 'Server started listening on ip address 172.1.0.91' + bcolors.ENDC)
    ip = str(ipaddress.ip_network(network,False).broadcast_address)
    while 1:
        server.sendto(message, (ip, 13117)) ################## change to variable 'network
        i+=1
        if(i==10):
            break
        time.sleep(1)
    server.close()

def thread_tcp():
    serverSocket.settimeout(10)
    connections=[]
    teams=[]
    while 1:
        try:
            connectionSocket, addr = serverSocket.accept()
            teamName = connectionSocket.recv(2048)
            teams.append(teamName.decode())
            connections.append(connectionSocket)

        except :
            startGame(teams,connections)
            break
    print (bcolors.WARNING + '\nGame over, sending out offer requests...' + bcolors.ENDC)  

def startGame(teams, connections):
    group1 = []
    group2 = []
    groupNumbers=[]
    for team in teams :
        if random.random() > 0.5:
            group1.append(team)
            groupNumbers.append(1)
        else:
            group2.append(team)
            groupNumbers.append(2)
    welcomeMessage='Welcome to Keyboard Spamming Battle Royale.\nGroup 1: \n==\n'
    for g in group1:
        welcomeMessage+=str(g) + '\n'
    welcomeMessage+='\nGroup 2: \n==\n'
    for g in group2:
        welcomeMessage+=str(g) + '\n'
    welcomeMessage+='\nStart pressing keys on your keyboard as fast as you can!!\n'
    
    threads=[]
    for i in range(len(connections)):
        thread= threading.Thread(target=listenToClient,args=(teams[i],connections[i],groupNumbers[i],welcomeMessage))
        threads.append(thread)
        thread.start()
     
        
    for thread in threads:
        thread.join()

    val1=max(next(copy.copy(counterG1)),0)
    val2=max(next(copy.copy(counterG2)),0)

    print (bcolors.WARNING + bcolors.BOLD + '\nGame over!' + bcolors.ENDC)
    print (bcolors.FAIL + 'Group 1 typed in ',val1, ' characters. Group 2 typed in ',val2, 'characters.' + bcolors.ENDC)
    if (val1 >val2):
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


def listenToClient(teamName,connection, groupNumber,welcomeMessage):
    teamCounter = 0
    connection.settimeout(10)
    connection.send(welcomeMessage.encode())
    curr= time.time()
    while time.time()<curr+10: 
        try:
            charTyped = connection.recv(1024)
            charTyped = charTyped.decode()
            chars[ord((str(charTyped)[1:])[1])]+=1
            if groupNumber == 1:
                next(counterG1)
            else:
                next(counterG2)
            teamCounter+=1
        except:
            break
    connection.close()

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', 0))
serverSocket.listen(1)
TCP_PORT = serverSocket.getsockname()[1]

inputCorrect = False
inputNetwork = ''
while inputCorrect == False:
    print(bcolors.UNDERLINE + bcolors.HEADER + bcolors.BOLD + 'please choose your virtual network:' + bcolors.ENDC)
    print(bcolors.HEADER + 'press 1 for dev network (eth1 - 172.1.0/24)' + bcolors.ENDC)
    print(bcolors.HEADER + 'press 2 for dev network (eth2 - 172.99.0/24)' + bcolors.ENDC)
    inputNetwork = input()
    if (inputNetwork == '1') | (inputNetwork == '2'):
        inputCorrect = True
    else:
        print(bcolors.FAIL + 'ERROR : you can only press 1 or 2, please try again' + bcolors.ENDC)

maxTappsPerGroup = 0

while 1: 
    try:              
        counterG1 =itertools.count()
        counterG2 = itertools.count()
        tcp = threading.Thread(target=thread_tcp)
        udp = threading.Thread(target=thread_udp, args=(inputNetwork)) ################### check input network
        tcp.start()
        udp.start()
        tcp.join()
        udp.join()
        maxTaps = printStatistics(maxTappsPerGroup)
        maxTappsPerGroup = maxTaps
    except:
        pass

    

