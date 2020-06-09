#!/usr/bin/env python
# coding: utf-8

# In[2]:


import socket
import hashlib
import random
import string
import paxos_pb2
import threading
import pickle
import socket
import time
import sys
from os import path
from struct import pack, unpack

# I decide to divide sending and receiving into two threads, and with receving wake up the sending thread when
# received proper message


# In[3]:


class State:
    def __init__(self):
        self.balance = 100
        self.blockChain = []
        self.queue = []
        self.ballot = paxos_pb2.BallotNum()


# In[36]:


# tested = State()
# tested.balance = 1000
# newla = paxos_pb2.Accept()
# newla.type = 2
# tested.blockChain.append(newla)


# In[37]:


# with open("stes.txt", "wb") as f:
#     pickle.dump(tested, f)


# In[38]:


# tested.balance = 100


# In[39]:


# with open("stes.txt", "rb") as f:
#     tested = pickle.load(f)


# In[41]:


# tested.balance
# tested.blockChain[0].SerializePartialToString()


# In[4]:

procNo = 3

states = State()
if path.isfile("State_" + str(procNo)):
    with open("State_" + str(procNo)) as f:
        states = pickle.load(f)


# In[5]:


# print("This is stub")

# tes = hashlib.sha256("nihao".encode("utf-8")).hexdigest()
# print(findNonce(tes))
ports = {1: 10001, 2:10002, 3:10003, 4:10004, 5:10005}
socks = {}
sockLocks = {}
responded = []
myVal = paxos_pb2.Block()
acceptVals = []
promiseCount = 1
PCLock = threading.Lock()
countLock = threading.Lock()

recvThreads = {}

# failed = False
# enough = threading.Condition()
ballot = paxos_pb2.BallotNum()
ballot.num = states.ballot.num
ballot.pid = procNo
ballot.depth = len(states.blockChain)

acceptBallot = paxos_pb2.BallotNum()
acceptCount = 0

started = False

mesSlot = {}

recvConds = {}

for i in range(5):
    socks[i + 1] = -1
    sockLocks[i + 1] = threading.Lock()
    recvConds[i + 1] = threading.Condition()
    recvThreads[i + 1] = 0
    mesSlot[i + 1] = 0

linkSuc = [False] * 5
activeFailed = [False] * 5

promiseVal = [0] * 5

acceptNum = paxos_pb2.BallotNum()
acceptVal = paxos_pb2.Block()


# In[7]:


tempBlock = paxos_pb2.Block()


# In[17]:


decideCond = threading.Condition()


# In[8]:


proposed = False


# In[9]:


myBlock = paxos_pb2.Block()


# In[6]:


acceptSlot = []
acceptCond = threading.Condition()
acceptCount = 0
promiseSlot = []
promiseCond = threading.Condition()


# In[ ]:


leader = True


# In[38]:


# te = paxos_pb2.Block()
# te.hash = "11"


# In[39]:


# hashlib.sha256(te.SerializeToString()).hexdigest()


# In[14]:


def lisAndAcc(sock):
    global socks, ports
    while True:
        soc, addr = sock.accept()
        for ite in ports:
            if ports[ite] == addr[1]:
                socks[ite] = soc
                linkSuc[ite - 1] = True
                threading.Thread(target = recvAndSet, args = (soc, ite, ))




# In[7]:


def getLocalQCount():
    global states, procNo
    count = 0
    for ite in states.queue:
        if ite[0] == procNo:
            count += 1

    return count


# In[ ]:


def waitSend(sock, mes):
    time.sleep(5)
    helpSend(sock, mes)


# In[ ]:


# def sendForRecovery(start, finish):
#     for i in range(start, finish):



# In[3]:


# def addToBlockChain(mes):
#     global states
#     states.blockChain.insert(mes.depth, mes.Block)


# In[1]:


def recvAndSet(sock, i):
    global mesSlot, recvConds, ballot, myVal, procNo, acceptNum, acceptVal, states
    global activeFailed, linkSuc
    global queue
    global acceptBallot
    global acceptSlot, acceptCond
    global promiseSlot, promiseCond
    global myBlock, tempBlock
    global leader
    global decideCond
    while True:
        le = safeRec(sock, 2)
        le = unpack(">H", le)[0]
        mes = safeRec(sock, le)
        newone = paxos_pb2.Prepare()
        newone.ParseFromString(mes)
        # getting Prepare, set the ballot number if greater and return promise
        if newone.type == 1:
            if (newone.ballot.num > ballot.num or (newone.ballot.num == ballot.num and newone.ballot.pid >= procNo)) and newone.ballot.depth >= len(ballot.blockChain):
                ballot.num = newone.ballot.num
                leader = False
                if newone.ballot.depth > ballot.depth:

                    sendForRecovery(ballot.depth, newone.ballot.depth)
                    ballot.depth = newone.ballot.depth

                returned = paxos_pb2.Promise()
                returned.type = 3
                returned.ballot.CopyFrom(newone.ballot)
                returned.acceptNum.CopyFrom(acceptNum)
                returned.acceptVal.CopyFrom(acceptVal)
                threading.Thread(target = waitSend, args = (sock, returned,)).start()


        elif newone.type == 3:
            if len(promiseSlot) <= 2:
                newone = paxos_pb2.Promise()
                newone.ParseFromString(mes)
                promiseSlot.append((i, newone))
                if len(promiseSlot) == 2:
                    promiseCond.acquire()
                    promiseCond.notifyAll()
                    promiseCond.clear()
                    promiseCond.release()

                    # promiseSlot to be cleared


        elif newone.type == 4:
            newone = paxos_pb2.Accept()
            newone.ParseFromString(mes)
            if (newone.myVal.num > ballot.num or (newone.myVal.num == ballot.num and newone.myVal.pid > ballot.pid)) and newone.myVal.depth >= len(states.blockChain):
                leader = False
                insi = newone.myVal.trans
                states.queue.append((i, insi))
                then = paxos_pb2.Accepted()
                then.type = 5
                acceptNum = newone.ballot
                acceptVal = newone.myVal
                then.ballot.CopyFrom(newone.ballot)
                then.acceptVal.CopyFrom(newone.myVal)

                threading.Thread(target = waitSend, args = (sock, then, )).start()

            continue

        elif newone.type == 5:
            if len(acceptSlot) < 2:

                newone = paxos_pb2.Accepted()
                newone.ParseFromString(mes)
                if newone.ballot == acceptBallot:
                    acceptSlot.append(newone)

            elif len(acceptSlot) == 2:
                acceptCond.acquire()
                acceptCond.notifyAll()
                acceptSlot.clear()
                acceptCond.release()

            # acceptSlot to be cleared


        elif newone.type == 6:
            newone = paxos_pb2.Decide()
            newone.ParseFromString(mes)
            if newone.val not in states.blockChain:
                states.blockChain.append(newone.val)
                if newone.val.trans.rcvr == procNo:
                    states.balance += newone.val.trans.amt

            ballot.depth = len(states.blockChain)
            clearQueue(i)
            leader = True
            tempBlock = paxos_pb2.Block()
            decideCond.acquire()
            decideCond.notifyAll()
            decideCond.release()


        elif newone.type == 7:
            newone = paxos_pb2.Recover()
            newone.ParseFromString(mes)
            if newone.depth < ballot.depth:
                then = paxos_pb2.RepRecover()
                then.type = 8
                then.depth = newone.depth
                then.block.CopyFrom(states.blockChain[depth])
                waitSend(sock, then)


        elif newone.type == 8:
            newone = paxos_pb2.RepRecover()
            newone.ParseFromString(mes)
            addToBlockChain(newone)
            continue



# In[60]:


def clearQueue(src):
    global states

    for ite in states.queue:
        if ite[0] == src:
            states.queue.remove(ite)



# In[ ]:


def failLink():
    global linkSuc, procNo
    print("Please enter the pid of the link to be failed")
    x = getInt()
    if x not in [1,2,3,4,5] or x == procNo:
        print("Invalid pid")
        return

    linkSuc[x - 1] = False


# In[ ]:


def fixLink():
    global linkSuc
    print("Please enter the pid of the link to be fixed")
    x = getInt()
    if x not in [1,2,3,4,5]:
        print("Invalid pid")
        return

    linkSuc[x-1] = True


# In[11]:


def getInt():
    while True:
        x = input()
        try:
            x = int(x)
        except ValueError:
            print("Not an integer")
            continue

        return x


# In[14]:


def helpSend(sock, ite):
    it = ite.SerializeToString()
    le = len(it)
    le = pack(">H", le)
    sock.send(le + it)


# In[ ]:


def failProcess():
    global procNo, states
    with open("State_" + str(procNo), "wb") as f:
        pickle.dump(states, f)

    print("Failing")
    sys.exit()


# In[ ]:


def printChain():
    global states
    print(states.blockChain)


# In[ ]:


def printBalance():
    global states
    print(states.balance)


# In[ ]:


def printQueue():
    global states
    print(states.queue)


# In[ ]:


# def comOther()


# In[ ]:


def conAndListen(sock, port):
    sock.connect(("localhost", port))
    server_address = ("localhost", ports[procNo])


# In[67]:


def randStr():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))


# In[69]:


# randStr()


# In[3]:


def findNonce(inp):
    while True:
        st = randStr()
        te = inp + st
        te = te.encode("utf-8")
        ans = hashlib.sha256(te).hexdigest()
        if ans[-1] in ['0', '1', '2', '3', '4']:
            return st


# In[44]:


# te = paxos_pb2.Block()
# te2 = paxos_pb2.Transaction()
# te2.src = 2
# te.trans.append(te2)
# transHash(te.trans)


# In[46]:


# b2 = "2"
# b2 = b2.encode()
# b2


# In[48]:





# In[49]:





# In[45]:


def transStr(trans):
    st = b''
    for ite in trans:
        st = st + ite.SerializeToString()

    return st


# In[51]:


def setNonce(block):

    while True:
        block.nonce = randStr()
        res = hashlib.sha256(block.SerializeToString()).hexdigest()
        if res[-1] in ['0', '1', '2', '3', '4']:
            break
#     nonc = findNonce(block.trans, block.hash)
#     block.nonce = nonc


# In[47]:


def findNonce(trans, has):
    while True:
        nonc = randStr()
        te = transStr(trans) + nonc + has.encode()
        ans = hashlib.sha256(te).hexdigest()
        if ans[-1] in ['0', '1', '2', '3', '4']:
            return nonc


# In[ ]:


def incrementCount():
    countLock.acquire()
    count += 1
    countLock.release()


# In[7]:


def timedRec(sock, n, ti):
    mes = []
    count = n
    now = time.time()

    try:

        while count > 0:
            a = sock.recv(count)
            mes.append(mes)
            le = len(a)
            count -= le

            if time.time() - now > ti:
                return False

    except:
        print("Connection closed")

        return False

    return b''.join(mes)


# In[ ]:


def safeRec(sock, n):
    mes = []
    count = n
    while count > 0:
        a = sock.recv(count)
        mes.append(mes)
        le = len(a)
        count -= le

    return b''.join(mes)


# In[12]:


def sendDecide():
    global procNo
    global ballot
    global tempBlock
    global myBlock
    global acceptBallot
    de = paxos_pb2.Decide()
    de.type = 6
    de.src = procNo
    de.ballot.CopyFrom(acceptBallot)
    if tempBlock != paxos_pb2.Block():
        de.val.CopyFrom(tempBlock)
    else:
        de.val.CopyFrom(myBlock)
    for ite in socks:
        if linkSuc[ite - 1] == True:
            threading.Thread(target = waitSend, args = (socks[ite], de,)).start()




# In[ ]:


def sendPrepare(sock, sno):
    global ports, procNo, states, promiseCount, responded
    pMes = paxos_pb2.Prepare()
    pMes.type = 1
    pMes.ballot.depth = len(states.blockChain)
    pMes.ballot.pid = procNo

    waitSend(sock, pMes)


# In[ ]:


def getPromise(sock, sno):
    global promiseCount, responded, PCLock
    res = timedRec(sock, 2, 7)
    if res == False:
        return False
    le = unpack(">H", res)[0]
    res = safeRec(sock, le)



    PCLock.acquire()
    promiseCount += 1
    PCLock.release()

    if len(responded) < 3:
        reponded.append(sno)

    return True


# In[ ]:


def askForPromise(i):
    global ports, linkSuc, socks
    global promiseCond, promiseCount
    if linkSuc[i] == False:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ("localhost", ports[i])
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(server_address)
        try:
            sock.connect(server_address)
        except Exception:
            print("Connection failed for server " + str(i))
            return

        socks[i] = sock
        linkSuc[i-1] = True
        threading.Thread(target = recvAndSet, args = (sock, i, ))

    sendPrepare(socks[i], i)




#     getPromise(socks[i], i)

#     t = threading.Thread(target = sendPrepare, args = (socks[i], i, ))
#     t.start()
#     t.join()







# In[ ]:


def maxOf(li):
    fir = li[0][1]
    for ite in li:
        if ite[1].acceptNum.depth > fir.acceptNum.depth:
            fir = ite[1]
        elif ite[1].acceptNum.depth == fir.acceptNum.depth:
            if ite[1].acceptNum.num > fir.acceptNum.num:
                fir = ite[1]
            elif ite[1].acceptNum.num == fir.acceptNum.num:
                if ite[1].acceptNum.pid > fir.acceptNum.pid:
                    fir = ite[1]

    return fir


# In[15]:


# I still need to decide if the returned promise indicate that we lagged behind in the process
def ElectAsLeader():
    global procNo, enough, promiseCount, activeFailed, responded
    global tempBlock
    global promiseSlot
    global states
    responded.append(procNo)


    quq = []
    ballot.num += 1
    ballot.pid = procNo
    ballot.depth = len(states.blockChain)
    for i in [1,2,3,4,5]:
        if i != procNo and activeFailed[i] == False:
            t = threading.Thread(target = askForPromise, args = (i,))
            t.start()
            quq.append(t)
    for ite in quq:
        ite.join()


    promiseCond.acquire()
    res = promiseCond.wait(6)
    promiseCond.release()


#     if promiseCount < 3:
    if res == False:
        print("Getting promise failed, not enough servers")
        return False


    tempBlock = maxof(promiseSlot)




#     promiseCount = 1






# In[ ]:


def sendAccept(sock, i):
    global ballot, states
    global acceptBallot
    global procNo
    global myBlock
    global tempBlock
    newone = paxos_pb2.Accept()
    newone.type = 4
    newone.ballot.CopyFrom(ballot)

    if tempBlock != paxos_pb2.Block():


        qualified = [ite[1] for ite in states.queue if ite[0] == procNo]
    #     qualified = []
    #     for ite in states.queue:
    #         if ite[0] == procNo:
    #             qualified.append(ite[1])

        newone.myVal.trans.extend(qualified)
        if len(states.blockChain) == 0:
            newone.myVal.hash = hashlib.sha256('').hexdigest()
        else:
            newone.myVal.hash = hashlib.sha256(states.blockChain[-1].SerializeToString()).hexdigest()

        setNonce(newone.myVal)
        clearQueue(procNo)
        myBlock.CopyFrom(newone.myVal)

    else:
        newone.myVal.CopyFrom(tempBlock)



#         states.blockChain[-1].hash



    acceptBallot.CopyFrom(newone.ballot)






    waitSend(sock, newone)
#     time.sleep(5)

#     helpSend(sock, newone)





# In[ ]:


def transPrepare():
    global procNo, responded, states, socks
    global linkSuc
    global acceptCond
#     toSent = paxos_pb2.Block()
#     toSent.trans.extend(states.queue)

#     if len(states.blockChain) == 0:
#         toSent.hash = ""
#     else:
#         toSent.hash =

    for ite in socks:
        if ite != procNo and linkSuc[ite - 1] == True:
            t = threading.Thread(target = sendAccept, args = (socks[ite], ite, ))
            t.start()
            t.join()


    acceptCond.acquire()
    res = acceptCond.wait(6)
    acceptCond.release()

    return res






# In[70]:


def randomVal():
    return random.uniform(6,9)


# In[16]:


def oneRound():
    global states, procNo
    global myBlock
    global acceptVal, acceptNum
#     global proposed
    global tempBlock
    global started
    global leader
    global decideCond
    started = True


    while True:
        time.sleep(randomVal())
        res = ElectAsLeader()
        if res == True and leader == True:
            res = transPrepare()
            if res == True and leader == True:

                if tempBlock == paxos_pb2.Block():
                    sendDecide()
                    if myBlock not in states.blockChain:
                        states.blockChain.append(myBlock)
                        states.balance -= myBlock.amt

                    acceptVal = paxos_pb2.Block()
                    acceptNum = paxos_pb2.BallotNum()
                    myBlock = paxos_pb2.Block()
                    started = False
                    return True
                else:

                    acceptVal = paxos_pb2.Block()
                    acceptNum = paxos_pb2.BallotNum()
                    tempBlock = paxos_pb2.Block()



            else:
                # Wait on decision to be made
                print("Waiting on decision")
                decideCond.acquire()
                decideCond.wait()
                decideCond.release()
#                 print("Accepting phase failed or not original value")
        else:
            # Wait on decision to be made
            print("Waiting on decision")
            decideCond.acquire()
            decideCond.wait()
            decideCond.release()
#             print("Failed to become leader")




#     nwBlo = paxos_pb2.Block()
#     trans = []
#     for ite in states.queue:

#         if ite[0] == procNo

#             trans.append(ite[1])

#     nwBlo.trans.extend(trans)


#     return True


# In[ ]:


def moneyTransfer():
    global linkSuc, procNo, states, started
    print("Please specify the destination pid:")
    x = getInt()
    if x not in [1,2,3,4,5] or x == procNo:
        print("Not a valid pid")
        return False

    print("Please specify the amount to transfer:")
    y = getInt()
    if y < 0:
        print("Amount cannot be negative")
        return False
    elif y > states.balance:
        print("Balance not enough")
        return False

    newTrans = paxos_pb2.Transaction()
    newTrans.src = procNo
    newTrans.rcvr = x
    newTrans.amt = y


    states.queue.append((procNo, newTrans))
    if not started:
        threading.Thread(target = oneRound).start()



# In[10]:


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ("localhost", ports[procNo])
sock.bind(server_address)
sock.listen()

threading.Thread(target=lisAndAcc, args = (sock,))

while True:
    print("Please choose your options:")
    print("1. Money Transfer")
    print("2. Fail link")
    print("3. Fix link")
    print("4. Fail this process")
    print("5. Print block chain")
    print("6. Print balance")
    print("7. Print queue")
    x = getInt()
    if x not in [1,2,3,4,5,6,7]:
        print("Not an valid option!")
        continue

    if x == 1:
        moneyTransfer()
    elif x == 2:
        failLink()
    elif x == 3:
        fixLink()
    elif x == 4:
        failProcess()
    elif x == 5:
        printChain()
    elif x == 6:
        printBalance()
    elif x == 7:
        printQueue()


# In[ ]:




