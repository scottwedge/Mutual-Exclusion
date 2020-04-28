import socket
import sys
import threading
from queue import Queue
HEADERSIZE = 10
balance = 10
#ll is filler for linkedlist
ll = 0
def initializeSocket(portNum):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP socket
    s.connect((socket.gethostname(), portNum))
    return s

def receive(s, q):
    while True:
        full_msg = ''
        new_msg = True
        while True: #Buffers data
            msg = s.recv(16) #Determines chunk size
            if new_msg:
                print(f"new message length: {msg[:HEADERSIZE]}")
                msglen = int(msg[:HEADERSIZE])
                new_msg = False

            full_msg += msg.decode("utf-8")

            if len(full_msg) - HEADERSIZE == msglen:
                print("full msg received!")
                print(full_msg[HEADERSIZE:])
                full_msg = "receive," + full_msg[HEADERSIZE:]
                q.put(full_msg)
                new_msg = True
                full_msg = ''


        print(full_msg)#Byte SOCK_STREAM

def processingThread(q, lamportClock, s, processID):
    while True:
        if not q.empty():
            #Messgae format is S,R,AMT
            msg = q.get()
            events = msg.split(',')
            if events[0] == "send":
                sendMsg = events[1] + "," + events[2] + "," + events[3]
                sendMsg = f'{len(sendMsg):<{HEADERSIZE}}' + sendMsg
                s.send(bytes(sendMsg, "utf-8"))
            elif events[0] == "receive":
                print("{0} receive event: receive message(\"{1}\") from {2}".format(processID, events[3], events[2]))

def main():
    #Initial LamportClock State
    lamportClock = []
    q = Queue()
    #Gets port number from command line
    portNum = int(sys.argv[1])
    s = initializeSocket(portNum)
    #Creates communication thread
    communication = threading.Thread(target=receive, args=(s,q ))
    communication.start()
    #Connection Message
    processing = threading.Thread(target=processingThread, args=(q, lamportClock, s, portNum))
    processing.start()

    while True:
        x = int(input('1 for Transfer Event, 2 Print Balance, and 3 for Print Blockchain: '))
        if x == 1:
            amt, rec = input(str(portNum) + ' transfer event: Input amount and receiver ').split()
            msg = 'send,' + str(portNum) + ',' + rec + ',' + amt
            q.put(msg)
        if x == 2:
            print(balance)
        if x == 3:
            print(ll)



main()
