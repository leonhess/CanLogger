import os
import modules
import DBCReader

init_mhs = 1

#settings for can
baudrate = 1000
snr = None
reconnect_attemps=10

new_can_msg_rx =0
current_frame_nr =0
DBC_data={}


def main():
    global current_frame_nr
    global DBC_data
    #check if the folder for log files exist
    if os.path.isdir("LOGS") ==0:
        os.mkdir("LOGS")

    #check if there is can device here
    modules.can_logger.top_level_can_logger.connect_tiny_can(baudrate,reconnect_attemps)
    DBC_data=DBCReader.read_dbc()

    #if init_mhs==1:
    #    can_driver=modules.tiny_can.MhsTinyCanDriver()
    #    if can_driver !=1:
    #        print("Tiny Can not found\n")
    #write logging

    try:
        while True:
            while modules.can_logger.top_level_can_logger.newData()==1:
                dat =  modules.can_logger.top_level_can_logger.read_buffered_can_frame_dicct_by_nr(current_frame_nr) 
                if dat:
                    #print(dat)
                    # print()
                    DBCReader.convert_can_frame_to_signals(dat)
                    current_frame_nr+=1
            if new_can_msg_rx:
                pass
    except KeyboardInterrupt:
        modules.logFileManager.logEvent("Keyboard")



if __name__ =="__main__":
    main()


