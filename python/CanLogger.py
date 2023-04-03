#!/usr/bin/python

import os
import sys
import time
import mhsTinyCanDriver as CanDriver
from baseOptionParser import BaseOptionParser




def timestamp(format_=None):
     time = datetime.now()
     match format_:
         case "file":
            time=time.strftime("%Y%m%d_%H%M%S")
         case others:
            time=time.strftime("%H:%M:%S:%f")
     return time


def createNewFilename(name,ending):
    fileNumber=0
    while(exists(name+"_"+str(fileNumber)+"."+ending)):
        fileNumber+=1
    return name+"_"+str(fileNumber)+"."+ending

def connect(baudrate, snr=None, attemps=5):
    current_attempt=0
    while(current_attempt<attemps):
        status = can_driver.OpenComplete(canSpeed=baudrate, snr=snr)

        #if status is None no error 
        if status:
            current_attempt+=1
        else:
            return 1
    return -1


#######################################################################
#######################################################################
#####start#############################################################
#######################################################################


#settings for can bus
baudrate=1000
snr=None
reconnect_attemps=10


#initalize CanDriver
can_driver=CanDriver.MhsTinyCanDriver()

#open the can initerface
status = connect(baudrate, snr=snr, attemps=reconnect_attemps)
if status < 0:
    #if the result of the connect function is negative a errer has occured
    sys.exit(status)


