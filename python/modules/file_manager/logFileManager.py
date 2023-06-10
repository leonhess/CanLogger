import os
from datetime import datetime
from . import general_file_functions as fhelp

log_file_name = "testLog.txt"







def logEvent(msg):
    msg = "{}: event = {}".format(fhelp.timestamp(),msg)
    fhelp.safe_write(msg,log_file_name)



