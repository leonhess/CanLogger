#!/usr/bin/python

import os
import sys
sys.path.append("tiny_can_driver")

import time
import tiny_can_driver.mhsTinyCanDriver as CanDriver
from baseOptionParser import BaseOptionParser
#import uselogging

from datetime import datetime
from os.path import exists

log_file_name = None
data_file_name = None



def log(msg):
    with open(log_file_name,"a") as log_file:
        event_msg=timestamp()+": event = "+ str(msg)+"\n"
        print(event_msg)
        log_file.write(event_msg)


def timestamp(format_=None):
     time = datetime.now()
     if format_=="file":
        time=time.strftime("%Y%m%d_%H%M%S")
     else:
        time=time.strftime("%H:%M:%S:%f")
     
     return time


def create_new_filename(name,ending):
    fileNumber=0
    while(exists(name+"_"+str(fileNumber)+"."+ending)):
        fileNumber+=1
    return name+"_"+str(fileNumber)+"."+ending


def connect(baudrate, snr=None, attemps=5):
    current_attempt=0
    while(current_attempt<attempts):
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

#logging and date files
start_time=timestamp("file")


log_file_name=create_new_filename(start_time+"_LOG","txt")
data_file_name=create_new_filename(start_time+"_data","txt")

log("[START]")



#initalize CanDriver
can_driver=CanDriver.MhsTinyCanDriver()

#open the can initerface
status = connect(baudrate, snr=snr, attemps=reconnect_attemps)
if status < 0:
    #if the result of the connect function is negative a errer has occured
    sys.exit(status)


