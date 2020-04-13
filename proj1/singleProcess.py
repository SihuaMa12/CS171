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


len = len(sys.argv)
if len != 2:
    print("Usage: python3 singleProcess.py [process number]")
    sys.exit()
    
try:
    x = int(sys.argv[1])
except ValueError:
    print("Not an integer, invalid usage")
    sys.exit()
    

