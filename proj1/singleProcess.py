#!/usr/bin/env python
# coding: utf-8

# In[1]:


import socket
import sys
import time
import threading
import concurrent.futures
import more_pb2 as more
import struct 
from struct import pack, unpack


# In[ ]:



    
quela = []
firstPri = 0
addLock = threading.Lock()


# In[ ]:


def byteHelp(mes):
    fir = mes.SerializeToString()
    a = pack(">H", len(fir))
    return a+fir


# In[ ]:


def safeRec(sock, n):
    lef = n
    res = []
    closed = False
    while lef > 0:
        then = sock.recv(lef)
        if then == b'':
            closed = True
            break
            
            
        lef -= len(then)
        res.append(then)
        
    if not closed:
        return b''.join(res)
    
    print("netProcess closed connection")
    
    sys.exit()
    
    return False


# In[ ]:


def addToQ(ev, clock):
    global quela
    global firstPri
    global addLock
    addLock.acquire()
    firstPri = max(clock, firstPri) + 1
    quela.append((firstPri, ev))
    addLock.release()
    


# In[ ]:


def comTask(sock):
    global quela
    global firstPri
    global addLock
    
    while True:
        newone = more.Event()
        le = safeRec(sock, 2)
        le = unpack(">H", le)[0]
        mes = safeRec(sock, le)
        newone.ParseFromString(mes)
        if newone.type != 1:
            continue
            
        print("Received event "+newone.mess + " from server " + str(newone.ori))
        addToQ(newone.mess, newone.clock)


# In[ ]:


def sendEvent(sock, mes, des):
    global x
    global firstPri
    me = more.Event()
    me.type = 1
    me.ori = x
    me.dest = des
    me.clock = firstPri
    me.mess = mes
    sock.sendall(byteHelp(me))
    addToQ("Send", 0)


# In[ ]:


def printClocks():
    global quela
    global x
    print("Clocks:", end = " ")
    print([i[0] for i in quela])


# In[ ]:


def askForEvent():
    print("Please enter an event")
    x = input()
    addToQ(x, 0)
        


# In[ ]:


def mainPrompt(sock):
    while True:
        print("Please enter the type of event, 1 for local event and 2 for send event. Enter 3 to print clock values")
        x1 = input()
        try:
            x1 = int(x1)
        except ValueError:
            print("Wrong type, please enter again!")
            continue
            
        if x1 == 1:
            askForEvent()
        elif x1 == 2:
            print("Please specify the server number to send the message to")
            sn = input()
            try:
                sn = int(sn)
            except ValueError:
                print("Invalid ID!")
                continue
                
            if sn not in [1,2,3]:
                print("Invalid ID! Please choose between 1, 2 and 3")
                continue
                
            print("Please specify the message to send")
            y = input()
            sendEvent(sock, y, sn)
            print("Event sent successfully!")
        elif x1 == 3:
            printClocks()
        else:
            print("Invalid event number!")
            continue
            


# In[7]:



le = len(sys.argv)
if le != 2:
    print("Usage: python3 singleProcess.py [process ID]")
    sys.exit()
    
try:
    x = int(sys.argv[1])
except ValueError:
    print("Not an integer, invalid usage")
    sys.exit()


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

net_address = ('localhost', 10000)
sock.connect(net_address)

ini = more.Initi()
ini.type = 2
ini.ori = x

sock.sendall(byteHelp(ini))

# Proceed to event phase
t = threading.Thread(target = comTask, args=(sock,))
t.start()
mainPrompt(sock)


# In[9]:


a = pack(">H",2)
a


# In[ ]:




