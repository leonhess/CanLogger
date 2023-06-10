import os
from datetime import datetime

log_file_name = "testLog.txt"

def timestamp(format_=None):
     time = datetime.now()
     if format_=="file":
        time=time.strftime("%Y%m%d_%H%M%S")
     else:
        time=time.strftime("%H:%M:%S:%f")     
     return time




def create_file(filename):
    with open(filename,'x') as f:
        pass



def log(msg,filename, mirror_terminal=0):
    if os.path.isfile == False:
        create_file("LOGS/{}".format(filename))
    
    with open("LOGS/{}".format(filename),'a') as f:
        f.write("{}\n".format(msg))

    if mirror_terminal==1:
        print("{}".format(msg))



def logEvent(msg):
    msg = "{}: event = {}\n".format(timestamp(),msg)
    log(msg,log_file_name)



