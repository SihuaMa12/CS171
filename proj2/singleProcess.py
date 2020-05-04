#!/usr/bin/env python
# coding: utf-8

# In[1]:


import socket
import sys
import time
import threading
import concurrent.futures
import proj2_pb2 as proj2
import struct
from struct import pack, unpack


# In[2]:


balance = 10
clock = 0
quela = []

clockLock = threading.Lock()

addLock = threading.Lock()
popLock = threading.Lock()
qLock = threading.Lock()
blockQueue = []
blockLock = threading.Lock()
# localQueue = {}
# localLock = threading.Lock()

incrementLock = threading.Lock()

wakeUp = threading.Condition()
sendLock = threading.Lock()

balanceLock = threading.Lock()


# In[4]:


def byteHelp(mes):
    fir = mes.SerializeToString()
    a = pack(">H", len(fir))
    return a + fir


# In[ ]:


# def waitOnRep(sock):
#     global incrementLock

#     re = safeRec(sock, 2)
#     le = unpack(re)[0]
#     re = safeRec(sock, le)
#     then = proj2.Reply()
#     then.ParseFromString(re)
#     if then.type == 2:
#         for it in quela:
#             if then.id == it.id and then.dest == it.ori:
#                 incrementLock.acquire()
#                 it.count += 1
#                 incrementLock.release()

#     return


# In[ ]:


def recvEvent(sock):
    global x
    global incrementLock
    global qLock
    global wakeUp
    while True:
        le = safeRec(sock, 2)
        le = unpack(">H", le)[0]
        re = safeRec(sock, le)
        more = proj2.Request()
        more.ParseFromString(re)
        if more.type == 1:  # Request received

            th = proj2.Request()
            th.ParseFromString(re)
            addClock(th.clock + 1)
            
            priorityAdd([more.ori, more.clock, 0])
            sendReply(sock, more.ori)
            

        elif more.type == 2:  # Reply received
            th = proj2.Reply()
            th.ParseFromString(re)
            addClock(th.clock + 1)

            for it in quela:
                if it[0] == x:
                    incrementLock.acquire()
                    it[2] += 1
                    incrementLock.release()
                    if it[2] == 2 and it == quela[0] and it[0] == x:
                        # criticSeciton()
                        wakeUp.acquire()
                        wakeUp.notifyAll()
                        wakeUp.release()

            

        elif more.type == 4:  # release received
            th = proj2.Release()
            th.ParseFromString(re)

            if th.ori == quela[0][0]:
                qLock.acquire()
                quela.pop(0)
                qLock.release()
                
            addClock(th.clock + 1)
            
            if len(quela) == 0:
                continue
                
            if quela[0][0] == x and quela[0][2] == 2:
                wakeUp.acquire()
                wakeUp.notifyAll()
                wakeUp.release()

            

        elif more.type == 5:  # BroadCast received
            th = proj2.Broadcast()
            th.ParseFromString(re)
            addBalance(th)
            addBlock(th)
            addClock(th.clock + 1)


# In[14]:


def sendReply(sock, serNo):
    global clock
    global sendLock
    
    th = proj2.Reply()
    th.type = 2
    th.clock = clock
    th.dest = serNo
    sendLock.acquire()
    sock.sendall(byteHelp(th))
    sendLock.release()
    addClock(-1)


# In[ ]:


def addBalance(ite):
    global balance
    global x
    if ite.dest == x:
        balanceLock.acquire()
        balance += ite.amt
        balanceLock.release()

    return


# In[11]:


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


# In[12]:


def addToQ(ind, it):
    global quela
    global qLock
    qLock.acquire()
    quela.insert(ind, it)
    qLock.release()


# In[ ]:


def addBlock(it):
    global blockQueue
    global blockLock
    blockLock.acquire()
    blockQueue.append([it.ori, it.dest, it.amt])
    blockLock.release()


# In[ ]:

def printBlock():
    global blockQueue
    print("(", end='')
    for it in blockQueue:
        print("[P" + str(it[0]) + ", P" + str(it[1]) + ", $" + str(it[2]) + "]", end='')
        if it != blockQueue[-1]:
            print(", ", end='')

    print(")")


# In[ ]:


# I decide to have ite[0] as the server number and ite[1] as the server time
def priorityAdd(ite):
    global quela
    inserted = False
    for i in range(len(quela)):
        if ite[1] == quela[i][1]:
            if ite[0] < quela[i][0]:
                addToQ(i, ite)
                inserted = True
                break

        if ite[1] < quela[i][1]:
            addToQ(i, ite)
            inserted = True
            break

    if not inserted:
        addToQ(len(quela), ite)


# In[9]:


# def comTask(sock):

    # In[ ]:


def addClock(ano):
    global clock
    global clockLock
    clockLock.acquire()
    clock = max(ano, clock) + 1
    clockLock.release()


# In[ ]:


def sendReq(sock):
    global x
    global clock
    global sendLock
    
    newone = proj2.Request()
    newone.type = 1
    newone.ori = x
    newone.clock = clock
    sendLock.acquire()
    sock.sendall(byteHelp(newone))
    priorityAdd([x, clock, 0])
    sendLock.release()
    addClock(-1)


# In[ ]:


def drawBalance(amt):
    global balance
    global balanceBlock
    balanceLock.acquire()
    balance -= amt
    balanceLock.release()
    if balance < 0:
        print("Balance Error!")

    return


# In[ ]:


def broadCastBlock(sock, dest, amt):
    global sendLock
    global x
    global clock

    th = proj2.Broadcast()
    th.type = 5
    th.ori = x
    th.dest = dest
    th.amt = amt
    th.clock = clock
    sendLock.acquire()
    sock.sendall(byteHelp(th))
    sendLock.release()
    addClock(-1)


# In[ ]:


def releaseBlock(sock):
    global sendLock
    global x
    global clock
    th = proj2.Release()
    th.type = 4
    th.ori = x
    th.clock = clock
    sendLock.acquire()
    sock.sendall(byteHelp(th))
    sendLock.release()
    addClock(-1)


# In[ ]:


def trans(amt, des, sock):
    global wakeUp
    global x
    global quela
    global qLock

    sendReq(sock)
    wakeUp.acquire()
    wakeUp.wait()
    drawBalance(amt)
    broadCastBlock(sock, des, amt)
    releaseBlock(sock)
    qLock.acquire()
    quela.pop(0)
    qLock.release()
    blockLock.acquire()
    blockQueue.append([x, des, amt])
    blockLock.release()
    print("Transaction completed!")
    wakeUp.release()

    return


# In[ ]:


def transferEvent(sock):
    global balance
    addClock(-1)
    print("Please enter the balance you want to transfer")
    x1 = input()
    try:
        x1 = int(x1)
    except ValueError:
        print("Invalid type!")
        return
    if x1 < 0:
        print("Invalid number!")
        return
    if x1 > balance:
        print("Failed since balance not enough!")
        return

    print("Please enter the server number you want to transfer balance to:")
    des = input()
    try:
        des = int(des)
    except ValueError:
        print("Invalid type!")
        return

    if des not in (1, 2, 3):
        print("Invalid number!")
        return

    trans(x1, des, sock)

    return


# In[ ]:


def printBalance():
    global balance
    print("Current Balance: " + "$" + str(balance))
    return


# In[ ]:


def mainPrompt(sock):
    while True:
        print("""Please specify the event you want:
            Press 1 to transfer
            Pess 2 to print balance
            Press 3 to print blockchain""")
        x1 = input()
        try:
            x1 = int(x1)
        except ValueError:
            print("Wrong type, please enter again!")
            continue

        if x1 == 1:
            transferEvent(sock)
        elif x1 == 2:
            printBalance()
        elif x1 == 3:
            printBlock()
        else:
            print("Invalid option!")


# In[ ]:


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

ini = proj2.Initi()
ini.type = 0
ini.ori = x

sock.sendall(byteHelp(ini))

# Proceed to event phase
t = threading.Thread(target=recvEvent, args=(sock,))
t.start()
mainPrompt(sock)
