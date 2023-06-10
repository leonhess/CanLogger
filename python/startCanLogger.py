import os
import modules


#settings for can
baudrate = 1000
snr = None
reconnect_attemps=10




if __name__ =="__main__":
  main()


def main(self):
    #check if the folder for log files exist
    if os.path.isdir("LOGS") == 0:
        os.mkdir("LOGS")

    #check if there is can device here
    can_driver=CanDriver.MhsTinyCanDriver()

