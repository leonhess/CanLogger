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

#import loraModul as LoraExample
import sx126x as LoraLib
log_file_name = None
data_file_name = None
dynamic_file_path="files/"
node = None


def log(msg, f_print=0):
    with open(log_file_name,"a") as log_file:
        event_msg=timestamp()+": event = "+ str(msg)+"\n"
        if f_print==0:
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
#####data formatting###################################################
#######################################################################

def formatMessage(message):
    time=timestamp()
    message = message.split("   ")
    info = message[0].split(" ")
    direction = info[0]
    ID = info[1]
    type_ = info[2]
    data=message[1].strip(" ")
    dlc=data[0]
    payload=data[1:].replace(" ","")
    
    string = time+";"+ID+";"+direction+";"+type_+";"+dlc+";"+payload+"\n"
    return string


def save_cached_msgs(msgs):
    data_string=""
    for msg in msgs:
        Id = msg
        msg = msgs.get(msg)
        s =["tTime", "direction", "format", "dlc", "data","diff" ]
        
        #s =[time, Id, direction, data,diff ]
        data_string+="\n"+Id
        for part in s:
            data_string+=";"+str(msg.get(part))

    with open(data_file_name ,"a") as loggingFile:
        loggingFile.write(data_string)

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
        time.sleep(0.500)
        connect(baudrate)


def StatusEventCallback(index,deviceStatusPointer):
    deviceStatus = deviceStatusPointer.contents
    #log(can_driver.FormatCanDeviceStatus(deviceStatusPointer, deviceStatusPointer.CanStatus,deviceStatusPointer.FIfoStatus))


compare_msgs= {}



def get_diff_time(msg_Id, msg):
    t_old=None

    if compare_msgs.get(msg_Id):
        t_old= compare_msgs.get(msg_Id).get("time")
    else:
        t_old={
        "Sec":0,
        "USec":0}
        compare_msgs.update({
        msg_Id : msg})
    
    
    compare_msgs[msg_Id]["time"] = msg.get("time")
    compare_msgs[msg_Id]["data"]=msg.get("data")
    compare_msgs[msg_Id]["diff"]=(msg["time"]["Sec"] - t_old["Sec"])*1000000
    compare_msgs[msg_Id]["diff"]+=(msg["time"]["USec"] - t_old["USec"])
    compare_msgs[msg_Id]["diff"]/=1000


    msg["diff"]=compare_msgs.get(msg_Id).get("diff")
    return msg


def RxEventCallback(index, DummyPointer, count):
    #log("RxEvent Index{0}".format(index))
    num_msg, raw_msgs = can_driver.CanReceive(count = 500)
    cached_msgs={} 
    if num_msg>0:       
        msgs = can_driver.FormatMessages(raw_msgs)
        dataArray=[]
        
        for raw_msg in raw_msgs:
            sec = raw_msg.Sec
            usec = raw_msg.USec
            dlc = raw_msg.Flags.FlagBits.DLC
            tTime = sec*1000000+usec

            #frame format
            if raw_msg.Flags.FlagBits.RTR and raw_msg.Flags.FlagBits.EFF:
                f_format = "EFF/RTR"
            elif raw_msg.Flags.FlagBits.EFF:
                f_format = "EFF"
            elif raw_msg.Flags.FlagBits.RTR:
                f_format = "STD/RTR"
            else:
                f_format = "STD"

            #data direction
            if raw_msg.Flags.FlagBits.TxD:
                direction = "TX"
            else:
                direction = "RX"

                
            #data
            data =""
            for i in range(dlc):
                d = raw_msg.Data[i]
                hexD = hex(d)[2:]
                if d <16:
                    data="0"+hexD+" "+data
                else:
                    data=hexD+" "+data

            Id = hex(raw_msg.Id)[2:]
            #print("- {}--{}.{}   {}".format(Id,str(sec),usec,data))
            #string=formatMessage(msg)
            #dataArray.append(string)

            cached_msg = {
            "tTime" : tTime,
            "dlc" :dlc,
            "data":data,
            "format" :f_format,
            "direction":direction,
            "diff":0,
            "time":{
                "Sec":sec,
                "USec":usec}
            }

            cached_msg=get_diff_time(Id, cached_msg)
            
            cached_msgs.update({
            Id : cached_msg
            })
        
        save_cached_msgs(cached_msgs)
        for s in dataArray:
            m = s.split(";")
            #print(m[1])
    else:
        if res[0] < 0:
            log(canDriver.FormatError(res, 'CanReceive'))
            #return -1
    #return 0


#######################################################################
#######################################################################
#####LORA#############################################################
#######################################################################

def init_Lora():   
    node = sx126x.sx126x(serial_num = "/dev/ttSerial0",freq=868,addr=0,power=22,rssi=True,air_speed=2400,relay=False)
    



def sendLoraFrame(ID_can_frame,data):
    id_int=int(ID_can_frame,16)
    print(data)
    data = data.split(" ")
    data_int=[]
    print("loop")
    for i in data:
        print(i)
        if i is not "":
            data_int.append(int(i,16))
          #  print("test{}".format(i)) 
    print(data_int)


#######################################################################
#######################################################################
#####start#############################################################
#######################################################################


#settings for can bus
baudrate=1000
snr=None
reconnect_attemps=10

#logging and date files
if not exists(dynamic_file_path):
    mkdir(dynamic_file_path)

start_time=timestamp("file")


log_file_name=create_new_filename(dynamic_file_path+start_time+"_LOG","txt")
data_file_name=create_new_filename(dynamic_file_path+start_time+"_DATA","txt")

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

#loraModul
init_Lora()

try:
    while True:
        time.sleep(0.100)
        data_string = ""
        for msg in compare_msgs:
            m = compare_msgs.get(msg)
            diff = m.get("diff")
            data = m.get("data")
            data_string+="{}:{}  {}\n".format(msg,diff,data)
            sendLoraFrame(msg,data) 
        print(data_string)
except KeyboardInterrupt:
    log("[KeyboardInterrupt]")

can_driver.CanSetEvents(0)
time.sleep(0.5)
can_driver.so=None
log("[DONE]")





