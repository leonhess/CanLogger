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
