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



#######################################################################
#######################################################################
#####start#############################################################
#######################################################################


#settings for can bus
baudrate=1000
snr=None


#initalize CanDriver
canDriver=CanDriver.MhsTinyCanDriver()

#open the can initerface


