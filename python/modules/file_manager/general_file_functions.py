import os
import time as t
from datetime import datetime


def create_file(filename):
    try:
        with open(filename,'x') as f:
            pass
    except FileExistsError:
        pass
    




def timestamp(format_=None):
     time = datetime.now()
     if format_=="file":
        time=time.strftime("%Y%m%d_%H%M%S")
     else:
        time=time.strftime("%H:%M:%S:%f")     
     return time



def safe_write(msg, filename, mirror_terminal=0):
    #check if file exist
    if os.path.isfile("./"+filename) == False:
        create_file("LOGS/{}".format(filename))
    #try writingwith
    with open("LOGS/{}".format(filename),'a') as f:
        f.write("{}\n".format(msg))

    if mirror_terminal==1:
        print("{}".format(msg))

