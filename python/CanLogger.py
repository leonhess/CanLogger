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
dynamic_file_path="files/"


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


def connect(baudrate, snr=None, attempts=5):
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
#####tiny_can_lib Callbacks############################################
#######################################################################
def PnPEventCallback(index, status):
    if status:
        canDriver.canDeviceOpen(index)
        canDriver.startCanBus(index)
        log("[Device connected]")
    else:
        log("[Device Disconnected]")
        log("[reconnecting...]")
        connect(baudrate)


def StatusEventCallback(index,deviceStatusPointer):
    deviceStatus = deviceStatusPointer.contents
    log(canDriver.FormatCanDeviceStatus(deviceStatus, deviceStatus.CanStatus, deviceStatus.FIfoStatus))


def RxEventCallback(index, DummyPointer, count):
    log("RxEvent Index{0}".format(index))
    res = canDriver.CanReceive(count = 500)
    
    if res[0]>0:       
        msgs = canDriver.FormatMessages(res[1])
        dataArray=[]
        for msg in msgs:
            string=formatMessage(msg)
            dataArray.append(string)
        saveMessageArray(dataArray)
    else:
        if res[0] < 0:
            log(canDriver.FormatError(res, 'CanReceive'))
            #return -1
    #return 0







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


log_file_name=create_new_filename(dynamic_file_path+start_time+"_LOG","txt")
data_file_name=create_new_filename(dynamic_file_path+"start_time"+"_DATA","txt")

log("[START]")



#initalize CanDriver
can_driver=CanDriver.MhsTinyCanDriver()

#open the can initerface
status = connect(baudrate, snr=snr, attempts=reconnect_attemps)
if status < 0:
    #if the result of the connect function is negative a errer has occured
    sys.exit(status)

#register callbacks
can_driver.CanSetUpEvents(PnPEventCallbackfunc=PnPEventCallback,
                          StatusEventCallbackfunc=StatusEventCallback,
                          RxEventCallbackfunc=RxEventCallback)
log("callbacks registered")






