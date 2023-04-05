# this file is used to read in a dbc file
# therefore the data that gets send over can can be interpreted with this file

import re
# slect a dbcfile and a datalogging file
with open("CANoe_C23.dbc","r") as dbc_handle:
    dbc_file = dbc_handle.read()

dataFile = open("testlogging.txt","r")


#iterate through each line in DBC file
for dbc_line in dbc_file.split("\n"):
    dbc_line = dbc_line.lstrip()



    #detech new frame block
    if dbc_line.startswith("BO_ "):
        frame_array =dbc_line.split(" ")
        frame_item={
                "block_name" : frame_array[2],
                "dlc" : frame_array[-2],
                "signals" : {},
                }

        current_frame_id = int(dbc_line.split(" ")[1])
        current_frame_id = hex(current_frame_id)[2:]
        current_frame_id = current_frame_id.lstrip("0")

    #detect a signal
    elif dbc_line.startswith("SG_ "):
        #split the data line at ":" -> signal information start here
        #use the last index and remove spaces
        formatString = dbc_line.split(":")[-1].strip()
        #remove the following char [,], ( and )
        formatString=re.sub("\[|\]|\(|\)","",formatString)
        
       # formatString = formatString.split(" ")
        #replce "|" and "@" with ","
        formatString = re.sub("\||@",",",formatString)
        formatString = re.sub("\+ ",",",formatString)
        formatString = re.sub(" ",",", formatString)
        signal_data = formatString.split(",")
        print(signal_data)







