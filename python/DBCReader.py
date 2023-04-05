# this file is used to read in a dbc file
# therefore the data that gets send over can can be interpreted with this file

import re
# slect a dbcfile and a datalogging file
with open("CANoe_C23.dbc","r") as dbc_handle:
    dbc_file = dbc_handle.read()

log_file = open("log2.txt","r")




frames = {}
frame_counter = 0
current_frame = None
current_frame_id = None

signal_counter = 0 


current_signal_name = None
#iterate through each line in DBC file
for dbc_line in dbc_file.split("\n"):
    dbc_line = dbc_line.lstrip()



    #detech new frame block
    if dbc_line.startswith("BO_ "):
        frame_array =dbc_line.split(" ")
        current_frame={
                "block_name" : frame_array[2],
                "amount_Signals" : frame_array[-2],
                "signals" : {},
                }

        current_frame_id = int(dbc_line.split(" ")[1])
        current_frame_id = hex(current_frame_id)[2:]
        current_frame_id = current_frame_id.lstrip("0")

    #detect a signal
    elif dbc_line.startswith("SG_ "):


        signal_name = dbc_line.split(":")[0]
        signal_name = signal_name. split(" ")[1]
    
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

        signal = {
                "start_bit" : signal_data[0],
                "length" : signal_data[1],
                "endinanes" : signal_data[2],
                "scale" : signal_data[3],
                "offset" : signal_data[4],
                "minima" : signal_data[5],
                "maxima" : signal_data[6],
                "unit" : signal_data[7],
                "extra_info" : signal_data[8]
                }

        current_signal_name = signal_data[-2]
        current_frame.get("signals").update({
            signal_name : signal
            })

        signal_counter += 1

    elif dbc_line.strip() =='' and current_frame:
        frames.update({
            current_frame_id : current_frame
            })
        current_frame = None
        current_frame_id = None
        frame_counter += 1


print("{} blocks have been read, with {} signals".format(frame_counter,signal_counter))


for line_number, logfile_line in enumerate(log_file):
    print(logfile_line)
    logfile_line = re.sub("\n","",str(logfile_line))
    log_data = logfile_line.split(";")
    print(log_data)
      #read in the information of the logged msg
    timestamp= log_data[0]
    canID = log_data[1].lstrip("0")
    direction = log_data[2]
    msg_type = log_data[3] 
    dlc = log_data[4]
    data = log_data[5]
   
    frame= frames.get(str(canID))
    print(frame)
   









