from .. import TinyCan as tiny_can
from .. import file_manager as fman

can_driver =None
data_file_name ="dataFile.txt"


def save_cached_msgs(msgs):
    global data_file_name
    data_string=""
    for msg in msgs:
        Id = msg
        msg = msgs.get(msg)
        s =["tTime", "direction", "format", "dlc", "data","diff" ]
        
        #s =[time, Id, direction, data,diff ]
        data_string+="\n"+Id
        for part in s:
            data_string+=";"+str(msg.get(part))
    fman.general_file_functions.safe_write(data_string,data_file_name,mirror_terminal=1)

    with open(data_file_name ,"a") as loggingFile:
        loggingFile.write(data_string)


#####################
#######calbacks######
#####################

def PnPEventCallback(index, status):
    global can_driver
    if status:
        can_driver.canDeviceOpen(index)
        can_driver.startCanBus(index)
        log("[Device connected]")
    else:
        log("[Device Disconnected]")
        log("[reconnecting...]")
        time.sleep(0.500)
        connect(baudrate)


def StatusEventCallback(index,deviceStatusPointer):
    deviceStatus = deviceStatusPointer.contents
    #log(can_driver.FormatCanDeviceStatus(deviceStatusPointer, deviceStatusPointer.CanStatus,deviceStatusPointer.FIfoStatus))


def RxEventCallback(index, DummyPointer, count):
    #log("RxEvent Index{0}".format(index))
    global can_driver
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

            #cached_msg=get_diff_time(Id, cached_msg)
            
            cached_msgs.update({
            Id : cached_msg
            })
        
        save_cached_msgs(cached_msgs)
        for s in dataArray:
            m = s.split(";")
            #print(m[1])
    else:
        if res < 0:
            log(canDriver.FormatError(res, 'CanReceive'))
            #return -1
    #return 0







###################
##setup############
###################
def connect_api(can_driver,baudrate, snr=None, attempts=5):
    current_attempt=0
    while(current_attempt<attempts):
        status = can_driver.OpenComplete(canSpeed=baudrate, snr=snr)
        #if status is None no error 
        if status:
            current_attempt+=1
        else:
            return 1
    return -1

def connect_tiny_can(baudrate,reconnect_attemps):
    #initalize CanDriver
    global can_driver
    can_driver=tiny_can.mhsTinyCanDriver.MhsTinyCanDriver()
    status = connect_api(can_driver,baudrate,attempts=reconnect_attemps)
    can_driver.CanSetUpEvents(PnPEventCallbackfunc=PnPEventCallback,
                          StatusEventCallbackfunc=StatusEventCallback,
                          RxEventCallbackfunc=RxEventCallback)

