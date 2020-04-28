import socket
import time
import threading
import random
from queue import Queue
HEADERSIZE = 10
def initializeSocket(portNum, socketAddresses):
    p1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP socket
    p1.bind((socket.gethostname(), portNum))
    p1.listen(5)
    clientsocket1, address1 = p1.accept()
    print("Connection from {} has been established!".format(address1))
    if portNum==1235:
        socketAddresses[0] = p1
        socketAddresses[1] = clientsocket1
    elif portNum==1236:
        socketAddresses[2] =p1
        socketAddresses[3] = clientsocket1
    elif portNum==1237:
        socketAddresses[4] =p1
        socketAddresses[5] = clientsocket1


def listen(p1, clientsocket1, q):
    while True:
        try:
            #Receive data in small chunks
            full_msg = ''
            new_msg = True
            while True: #Buffers data
                msg = clientsocket1.recv(16) #Determines chunk size
                if new_msg:
                    print(f"new message length: {msg[:HEADERSIZE]}")
                    msglen = int(msg[:HEADERSIZE])
                    new_msg = False

                full_msg += msg.decode("utf-8")

                if len(full_msg) - HEADERSIZE == msglen:
                    print("full msg received!")
                    print(full_msg[HEADERSIZE:])
                    x = full_msg[HEADERSIZE:].split(',')
                    sendObject = []
                    sendObject.append(int(x[0]))
                    sendObject.append(int(x[1]))
                    sendObject.append(x[2])
                    print(sendObject)
                    #Sleep Time
                    time.sleep(1)
                    q.put(sendObject)

                    new_msg = True
                    full_msg = ''

        finally:
            p1.close()

def main():
    #Shared Queue
    q = Queue()
    socketAddresses = [0]*6
    #Stores clientSockets
    connection1= threading.Thread(target=initializeSocket, args=(1235, socketAddresses))
    connection2= threading.Thread(target=initializeSocket, args=(1236, socketAddresses))
    connection3= threading.Thread(target=initializeSocket, args=(1237, socketAddresses))
    connection1.start()
    connection2.start()
    connection3.start()

    connection1.join()
    connection2.join()
    connection3.join()
    #Creates 3 Connections which will listen to
    #Communication Threads
    p1 = threading.Thread(target=listen, args=(socketAddresses[0],socketAddresses[1],q, ))
    p2 = threading.Thread(target=listen, args=(socketAddresses[2],socketAddresses[3],q, ))
    p3 = threading.Thread(target=listen, args=(socketAddresses[4],socketAddresses[5],q, ))
    p1.start()
    p2.start()
    p3.start()
    while True:
        if not q.empty():
            sendEvent = q.get()
            rec = sendEvent[1]
            sendMsg = str(sendEvent[0]) +"," +str(sendEvent[1]) + "," + sendEvent[2]
            sendMsg = f'{len(sendMsg):<{HEADERSIZE}}' + sendMsg
            if rec == 1235:
                socketAddresses[1].send(bytes(sendMsg, "utf-8"))
            elif rec == 1236:
                socketAddresses[3].send(bytes(sendMsg, "utf-8"))
            elif rec == 1237:
                socketAddresses[5].send(bytes(sendMsg, "utf-8"))



main()
