import os
import modules


init_mhs = 1

#settings for can
baudrate = 1000
snr = None
reconnect_attemps=10

new_can_msg_rx =0



def main():
    #check if the folder for log files exist
    if os.path.isdir("LOGS") ==0:
        os.mkdir("LOGS")

    #check if there is can device here
    if init_mhs==1:
        can_driver=modules.tiny_can.MhsTinyCanDriver()
        if can_driver !=1:
            print("Tiny Can not found\n")
    #write logging

    try:
        while True:
            if new_can_msg_rx:
                pass
    except KeyboardInterrupt:
        modules.logFileManager.logEvent("Keyboard")

if __name__ =="__main__":
  main()


