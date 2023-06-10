
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

