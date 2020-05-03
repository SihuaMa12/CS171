#!/usr/bin/env python
# coding: utf-8

# In[11]:


import socket
import sys
import time
import threading
import random
import concurrent.futures
import proj2_pb2 as more
import struct
from struct import pack, unpack


# In[12]:


# a = pack(">H",2)
# a


# In[ ]:


# In[13]:


def SerE(sock, mes):
    me = more.SerError()
    me.type = 3
    me.error = mes
    then = me.SerializeToString()
    first = len(then)
    first = pack(">H", first)
    sock.sendall(first + then)


# In[14]:


def endSock(sock):
    sock.close()
    sys.exit()

    return False


# In[15]:


def delaySome():
    time.sleep(random.uniform(1, 5))


# In[ ]:


def newSend(ne, mes):
    delaySome()
    ne[1].acquire()
    ne[0].sendall(mes)
    ne[1].release()

    return


# In[16]:

def mereRec(sock, n):
    lef = n
    res = []
    while lef > 0:
        then = sock.recv(lef)
        if then == b'':
            break

        lef -= len(then)
        res.append(then)

    return b''.join(res)


def safeRec(sock, n, serNo):
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

    del sers[serNo]
    sock.close()
    sys.exit()

    return False


# In[17]:


def newMes(sock, address):
    # Expecting initial message from processes
    global sers
    ini = more.Initi()
    le = mereRec(sock, 2)
    le = unpack(">H", le)[0]
    res = mereRec(sock, le)
    ini.ParseFromString(res)
    if ini.type == 2:
        sers[ini.ori] = [sock, threading.Lock()]
    else:
        SerE(sock, "Expected initial message, not receiving right")
        endSock(sock)

    # Continue to event sending phase
    while True:
        le = safeRec(sock, 2, ini.ori)
        le = unpack(">H", le)[0]
        res = safeRec(sock, le, ini.ori)
        newone = more.Request()
        newone.ParseFromString(res)

        if newone.type == 1:         # request
            then = more.Request()
            then.ParseFromString(res)
            for it in sers:
                if it != then.ori:
                    ne = sers[it]
                    first = pack(">H", len(res))
                    hreading.Thread(target=newSend, args=[ne, first + res]).start()

        if newone.type == 2:         # Reply
            then = more.Reply()
            then.ParseFromString(res)
            ne = sers[then.dest]
            first = pack(">H", len(res))
            hreading.Thread(target=newSend, args=[ne, first + res]).start()

        if newone.type == 4:         # Release
            then = more.Release()
            then.ParseFromString(res)
            for it in sers:
                if it != then.ori:
                    ne = sers[it]
                    first = pack(">H", len(res))
                    hreading.Thread(target=newSend, args=[ne, first + res]).start()

        if newone.type == 5:         # Broadcast
            then = more.Broadcast()
            then.ParseFromString(res)
            for it in sers:
                if it != then.ori:
                    ne = sers[it]
                    first = pack(">H", len(res))
                    hreading.Thread(target=newSend, args=[ne, first + res]).start()

    return False


# In[ ]:
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ('localhost', 10000)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)

sock.listen()

sers = {}

while True:
    socks, address = sock.accept()
    t = threading.Thread(target=newMes, args=(socks, address,))
    t.start()

sock.close()
