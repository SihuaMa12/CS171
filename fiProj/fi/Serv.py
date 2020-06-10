#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


# In[ ]:


def getInt():
    while True:
        x = input()
        try:
            x = int(x)
        except ValueError:
            print("Not an integer")
            continue
        
        return x


# In[44]:


class State:
    def __init__(self):
        self.balance = 100
        self.blockChain = []
        self.queue = []
        self.ballot = paxos_pb2.BallotNum()


# In[37]:


# with open("stes.txt", "wb") as f:
#     pickle.dump(tested, f)


# In[39]:


# with open("stes.txt", "rb") as f:
#     tested = pickle.load(f)


# In[41]:


# tested.balance
# tested.blockChain[0].SerializePartialToString()


# In[45]:


procNo = 0

print("Please specify the server id")
x = getInt()
if x in [1,2,3,4,5]:
    procNo = x

states = State()
if path.isfile("State_" + str(procNo)):
    with open("State_" + str(procNo)) as f:
        states = pickle.load(f)


# In[48]:


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

# failed = False
# enough = threading.Condition()
ballot = paxos_pb2.BallotNum()
ballot.num = states.ballot.num
ballot.pid = procNo
ballot.depth = len(states.blockChain)

acceptBallot = paxos_pb2.BallotNum()
acceptCount = 0

acceptingPromise = False

acceptingAcced = False

started = False


recvConds = {}

for i in range(5):
    socks[i + 1] = -1
    sockLocks[i + 1] = threading.Lock()
    recvConds[i + 1] = threading.Condition()
    
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



# In[38]:


# te = paxos_pb2.Block()
# te.hash = "11"


# In[39]:


# hashlib.sha256(te.SerializeToString()).hexdigest()


# In[2]:


def lisAndAcc(sock):
    global socks, ports
    while True:
        soc, addr = sock.accept()
        print("Accepted link")
        le = safeRec(soc, 2)
        le = unpack(">H", le)[0]
        ini = safeRec(soc, le)
        sr = paxos_pb2.Init()
        sr.ParseFromString(ini)
        srcc = sr.src
        socks[srcc] = soc
        linkSuc[srcc - 1] = True
        threading.Thread(target = recvAndSet, args = (soc, srcc, )).start()
                
                


# In[2]:


def getLocalQCount():
    global states, procNo
    count = 0
    for ite in states.queue:
        if ite[0] == procNo:
            count += 1
            
    return count


# In[3]:


def waitSend(sock, mes):
    time.sleep(5)
    helpSend(sock, mes)


# In[5]:


def addToBlockChain(mes):
    global states
    states.blockChain.insert(mes.depth, mes.Block)


# In[52]:


def recvAndSet(sock, i):
    global recvConds, ballot, myVal, procNo, acceptNum, acceptVal, states
    global activeFailed, linkSuc
    global acceptBallot
    global acceptSlot, acceptCond
    global promiseSlot, promiseCond
    global myBlock, tempBlock
    global decideCond
    global acceptingPromise
    global acceptingAcced
    while True:
        le = safeRec(sock, 2)
        if le == b'':
            socks[i] = -1
            linkSuc[i-1] = False
            return
        le = unpack(">H", le)[0]
        mes = safeRec(sock, le)
        newone = paxos_pb2.Prepare()
        newone.ParseFromString(mes)
        # getting Prepare, set the ballot number if greater and return promise
        if newone.type == 1:
            print("Prepared")
            print(newone.ballot)
            print(ballot)
            if newone.ballot.depth > ballot.depth or (newone.ballot.depth == ballot.depth and newone.ballot.num > ballot.num) or (newone.ballot.depth == ballot.depth and newone.ballot.num == ballot.num and newone.ballot.pid >= ballot.pid):
                ballot.CopyFrom(newone.ballot)
                #if newone.ballot.depth > ballot.depth:
                    
                 #   sendForRecovery(ballot.depth, newone.ballot.depth)
                  #  ballot.depth = newone.ballot.depth
                
                returned = paxos_pb2.Promise()
                returned.type = 3
                returned.ballot.CopyFrom(newone.ballot)
                returned.acceptNum.CopyFrom(acceptNum)
                returned.acceptVal.CopyFrom(acceptVal)
                print("Sending")
                threading.Thread(target = waitSend, args = (sock, returned,)).start()
                
            
            
        elif newone.type == 3:
            print("Promised")
            newone = paxos_pb2.Promise()
            newone.ParseFromString(mes)
            if newone.ballot == ballot and acceptingPromise:
                print("Still in phase")
                print("Length: ", len(promiseSlot))
                if len(promiseSlot) < 2:
                    print("Going on")
                    promiseSlot.append((i, newone))
                    if len(promiseSlot) == 2:
                        print("Here")
                        promiseCond.acquire()
                        promiseCond.notifyAll()
                        acceptingPromise = False
                        # promiseSlot.clear()
                        promiseCond.release()
                    # else:
                    #     print("Debug: promiseSlot not equal 2 ", promiseSlot)
                # else:
                #     print("Debug: promiseSlot ", promiseSlot)
            # else:
            #     print("Promised, newone.ballot ", newone.ballot)
            #     print("Promised, ballot ", ballot)
            #         # promiseSlot to be cleared, not here
            
            
        elif newone.type == 4:
            print("Got accept from " + str(i))
            newone = paxos_pb2.Accept()
            newone.ParseFromString(mes)
            if newone.ballot.depth > ballot.depth or (newone.ballot.depth == ballot.depth and newone.ballot.num > ballot.num) or (newone.ballot.depth == ballot.depth and newone.ballot.num == ballot.num and newone.ballot.pid >= ballot.pid):
                print("Sending back accepted")
                then = paxos_pb2.Accepted()
                then.type = 5
                acceptNum.CopyFrom(newone.ballot)
                acceptVal.CopyFrom(newone.myVal)
                then.ballot.CopyFrom(newone.ballot)
                then.acceptVal.CopyFrom(newone.myVal)
                
                threading.Thread(target = waitSend, args = (sock, then, )).start()
            else:
                print("Did not accept")
                print("newone.ballot ", newone.ballot)
                print("local ballot: ", ballot)

                
        elif newone.type == 5:
            print("Accepted from " + str(i))
            if len(acceptSlot) < 2:

                newone = paxos_pb2.Accepted()
                newone.ParseFromString(mes)
                if newone.ballot == acceptBallot:
                    acceptSlot.append(newone)
                
                if len(acceptSlot) == 2:
                    acceptCond.acquire()
                    acceptCond.notifyAll()
                    acceptingAcced = False
                    acceptSlot.clear()
                    acceptCond.release()
                
            # acceptSlot to be cleared
                
        
        elif newone.type == 6:
            newone = paxos_pb2.Decide()
            newone.ParseFromString(mes)
            if newone.val not in states.blockChain:
                states.blockChain.append(newone.val)
                for ite in newone.val.trans:
                    if ite.rcvr == procNo:
                        states.balance += ite.amt
                
            ballot.depth = len(states.blockChain)
            
            if newone.val == myBlock:
                print("cleaning myBLock")
                myBlock = paxos_pb2.Block()
            if newone.val == tempBlock :
                print("cleaning tempBlock and acceptVal")
                tempBlock = paxos_pb2.Block()

            if newone.val == acceptVal:
                print("cleaning acceptVal")
                acceptVal = paxos_pb2.Block()
            else:
                print("Error: ")
                print(newone.val)
                print(acceptVal)
                


            decideCond.acquire()
            decideCond.notifyAll()
            decideCond.release()
            
            
        # elif newone.type == 7:
        #     newone = paxos_pb2.Recover()
        #     newone.ParseFromString(mes)
        #     if newone.depth < ballot.depth:
        #         then = paxos_pb2.RepRecover()
        #         then.type = 8
        #         then.depth = newone.depth
        #         then.block.CopyFrom(states.blockChain[depth])
        #         waitSend(sock, then)
            
            
        elif newone.type == 8:
            newone = paxos_pb2.RepRecover()
            newone.ParseFromString(mes)
            addToBlockChain(newone)
            continue
            


# In[7]:


# def clearQueue(src):
#     global states
    
#     for ite in states.queue:
#         if ite[0] == src:
#             states.queue.remove(ite)
            


# In[8]:


def failLink():
    global linkSuc, procNo
    print("Please enter the pid of the link to be failed")
    x = getInt()
    if x not in [1,2,3,4,5] or x == procNo:
        print("Invalid pid")
        return
    
    linkSuc[x - 1] = False


# In[9]:


def fixLink():
    global linkSuc
    print("Please enter the pid of the link to be fixed")
    x = getInt()
    if x not in [1,2,3,4,5]:
        print("Invalid pid")
        return
    
    linkSuc[x-1] = True


# In[10]:


def getInt():
    while True:
        x = input()
        try:
            x = int(x)
        except ValueError:
            print("Not an integer")
            continue
        
        return x


# In[11]:


def helpSend(sock, ite):
    it = ite.SerializeToString()
    le = len(it)
    le = pack(">H", le)
    sock.send(le + it)


# In[12]:


def failProcess():
    global procNo, states
    with open("State_" + str(procNo), "wb") as f:
        pickle.dump(states, f)
        
    print("Failing")
    sys.exit()


# In[13]:


def printChain():
    global states
    print(states.blockChain)


# In[14]:


def printBalance():
    global states
    print(states.balance)


# In[15]:


def printQueue():
    global states
    print(states.queue)


# In[17]:


def conAndListen(sock, port):
    sock.connect(("localhost", port))
    server_address = ("localhost", ports[procNo])


# In[18]:


def randStr():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))


# In[19]:


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


# In[20]:


def transStr(trans):
    st = b''
    for ite in trans:
        st = st + ite.SerializeToString()
        
    return st


# In[21]:


def setNonce(block):
    
    while True:
        block.nonce = randStr()
        res = hashlib.sha256(block.SerializeToString()).hexdigest()
        if res[-1] in ['0', '1', '2', '3', '4']:
            break
#     nonc = findNonce(block.trans, block.hash)
#     block.nonce = nonc


# In[22]:


def findNonce(trans, has):
    while True:
        nonc = randStr()
        te = transStr(trans) + nonc + has.encode()
        ans = hashlib.sha256(te).hexdigest()
        if ans[-1] in ['0', '1', '2', '3', '4']:
            return nonc



# In[24]:


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


# In[39]:


def safeRec(sock, n):
    mes = []
    count = n
    while count > 0:
        a = sock.recv(count)
        if a == b'':
            return a
        
        mes.append(a)
        le = len(a)
        count -= le
        
    return b''.join(mes)


# In[26]:


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
            
    


# In[27]:


def sendPrepare(sock, sno):
    print("Sending promise to " + str(sno))
    global ports, procNo, states, promiseCount, responded
    global ballot
    pMes = paxos_pb2.Prepare()
    ballot.depth = len(states.blockChain)
    pMes.type = 1
    pMes.ballot.CopyFrom(ballot)
    
    
    waitSend(sock, pMes)


# In[28]:


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


# In[50]:


def askForPromise(i):
    global ports, linkSuc, socks
    global procNo
    print("Asking for promise from " + str(i))
    if linkSuc[i-1] == False:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ("localhost", ports[i])
        try:
            sock.connect(server_address)
        except Exception:
            print("Connection failed for server " + str(i))
            return False
        
        # Send procNo
        ini = paxos_pb2.Init()
        ini.src = procNo
        helpSend(sock, ini)
        
        
        socks[i] = sock
        linkSuc[i-1] = True
        threading.Thread(target = recvAndSet, args = (sock, i, )).start()
        
    sendPrepare(socks[i], i)
    
    
    
    
#     getPromise(socks[i], i)
    
#     t = threading.Thread(target = sendPrepare, args = (socks[i], i, ))
#     t.start()
#     t.join()
    
    
    
    
    


# In[31]:


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
                    
    return fir.acceptVal


# In[3]:


# I still need to decide if the returned promise indicate that we lagged behind in the process
def ElectAsLeader():
    global procNo, promiseCount, activeFailed, responded
    global tempBlock
    global promiseSlot
    global states
    global acceptingPromise
    responded.append(procNo)
    
    
    quq = []
    acceptingPromise = True
    for i in [1,2,3,4,5]:
        if i != procNo and activeFailed[i-1] == False:
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
        print("Returning False")
        return False
    
    
    tempBlock = maxOf(promiseSlot)
    if tempBlock != paxos_pb2.Block():
        print("promoseSlot with temp", promiseSlot, tempBlock)
    

    print("Length before cleared ", len(promiseSlot))
    promiseSlot.clear()
    print("Length after cleared ", len(promiseSlot))

    return True
    
    
    
#     promiseCount = 1
    
    
    




# In[49]:


def sendAccept(sock, i, passed):
    global ballot, states
    global acceptBallot
    global procNo
    global myBlock
    global tempBlock
    

    
    
    
    
    
    
    
    waitSend(sock, newone)
#     time.sleep(5)
    
#     helpSend(sock, newone)
    
    
    


# In[35]:


def transPrepare():
    global procNo, responded, states, socks
    global linkSuc
    global acceptCond
    global acceptingAcced
#     toSent = paxos_pb2.Block()
#     toSent.trans.extend(states.queue)
    
#     if len(states.blockChain) == 0:
#         toSent.hash = ""
#     else:
#         toSent.hash = 

    newone = paxos_pb2.Accept()
    newone.type = 4
    newone.ballot.CopyFrom(ballot)

    if tempBlock != paxos_pb2.Block():
        newone.myVal.CopyFrom(tempBlock)

    elif myBlock != paxos_pb2.Block():
        newone.myVal.CopyFrom(myBlock)

    else:
    
        acceptBallot.CopyFrom(newone.ballot)

        newone.myVal.trans.extend(states.queue.copy())
    # print("newone.myVal.trans: ", newone.myVal.trans)
    # print("states.queue: " , states.queue.copy())
        if len(states.blockChain) == 0:
            newone.myVal.hash = hashlib.sha256(b'').hexdigest()
        else:
            newone.myVal.hash = hashlib.sha256(states.blockChain[-1].SerializeToString()).hexdigest()  

        setNonce(newone.myVal)
            
        states.queue.clear()
        
        myBlock.CopyFrom(newone.myVal)
        print("myblock: ", myBlock)


    
    quq = []
    for ite in socks:
        if ite != procNo and linkSuc[ite - 1] == True:
            t = threading.Thread(target = waitSend, args = (socks[ite], newone,  ))
            quq.append(t)
            t.start()
            
    for ite in quq:
        ite.join()

    acceptingAcced = True
            
    acceptCond.acquire()
    res = acceptCond.wait(7)
    acceptCond.release()
    
    return res
        
    
    
    


# In[36]:


def randomVal():
    return random.uniform(6,9)


# In[37]:


def oneRound():
    global states, procNo
    global myBlock
    global acceptVal, acceptNum
#     global proposed
    global tempBlock
    global started
    global decideCond
    started = True
    
    
    while len(states.queue) > 0 or myBlock != paxos_pb2.Block() or tempBlock != paxos_pb2.Block():
        time.sleep(randomVal())
        ballot.num += 1
        ballot.pid = procNo
        ballot.depth = len(states.blockChain)
        res = ElectAsLeader()

        if res == True:
            print("Starting as leader")
            res = transPrepare()
            if res == True:
                print("Second phase")
                if tempBlock == paxos_pb2.Block():
                    sendDecide()
                    if myBlock not in states.blockChain:
                        states.blockChain.append(myBlock)
                        for ite in myBlock.trans:
                            states.balance -= ite.amt


                    myBlock = paxos_pb2.Block()
                else:
                    print("Waiting for decision 0")
                    print("Tempblock: ", tempBlock)
                    decideCond.acquire()
                    decideCond.wait(7)
                    decideCond.release()
                
                
            else:
                # Wait on decision to be made
                print("Waiting on decision 1")
                decideCond.acquire()
                decideCond.wait(14)
                decideCond.release()
#                 print("Accepting phase failed or not original value")
        else:
            # Wait on decision to be made
            print("Waiting on decision 2")
            decideCond.acquire()
            decideCond.wait(21)
            decideCond.release()
#             print("Failed to become leader")
    
    
    started = False
    
#     nwBlo = paxos_pb2.Block()
#     trans = []
#     for ite in states.queue:
        
#         if ite[0] == procNo
            
#             trans.append(ite[1])
            
#     nwBlo.trans.extend(trans)
    
    
#     return True


# In[38]:


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
    
    
    states.queue.append(newTrans)
    if not started:
        threading.Thread(target = oneRound).start()
    


# In[10]:



    

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ("localhost", ports[procNo])
sock.bind(server_address)
sock.listen()

threading.Thread(target=lisAndAcc, args = (sock,)).start()

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




