# this file is used to read in a dbc file
# therefore the data that gets send over can can be interpreted with this file
import re
import time

# select a dbcfile and a datalogging file

def read_dbc(file = "CANoe_C23.dbc"):
    with open(file,"r") as dbc_handle:
        dbc_file = dbc_handle.read()

   

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
    return frames



def map_data_to_signal(signal, data):
        #print("signal {}".format(signal))
        start_bit=int(signal.get("start_bit"))
        length=int(signal.get("length"))
        scale=float(signal.get("scale"))
        offset=float(signal.get("offset"))
        unit=str(signal.get("unit"))
        print("stat:{}, length :{}, scale:{}, offset:{}, unit:{}, data:{}".format(start_bit,length,scale,offset,unit,data))
        #get the concrete values of each signal
                   
        #create a bitmask while shifting with 1 and orring with
        bitmask=0
        for i in range(length):
            bitmask=(bitmask<<1)|1

        for i in range(start_bit):
            bitmask=bitmask<<1
        print("Maks",bin(data))
        print("MASK",bin(bitmask))

        masked_value=data&bitmask
        backshifted_value =masked_value>>start_bit
        print("maskedvalue", bin(masked_value))
        print("maskedvalue", bin(backshifted_value))
        #scale value and offset

        value=backshifted_value*scale+offset

        #print(signal)
        signal_container = {
                "value":value,
                "unit":unit}
        #print(signal_container)
        #signal_containers.update({
        #    signal_name:signal_container
        #    })
        print(value)
        return value



def map_data_to_frame(frame, data):
    decoded_frame = {}
    #convert hex data to integer
    data = data.replace(" ","") 
    print("hex ", data)
    data = int(str(data),16)
    print("dec ", data)
    #iterate through all signals in this frame
    for signal in frame.get("signals"):
        print(signal)
        mapped_data = map_data_to_signal(frame.get("signals").get(signal), data)
        print(signal,mapped_data)
        time.sleep(1)
        decoded_signal = {
                "data" : mapped_data,
               "unit" : frame.get("signals").get(signal).get("unit")
        }

        decoded_frame.update({
            signal : decoded_signal
            })
    #print(decoded_frame)
    return decoded_frame







############################################
###########################################
##########################################

#read dbc in dicct
dbc_structure = read_dbc("PDB_C2021.dbc")
#print(dbc_structure)
log_file = open("20230407_153701_DATA_0.txt","r")


#iterate through data file
for line_number, logfile_line in enumerate(log_file):
    
    logfile_line = re.sub("\n","",str(logfile_line))
    log_data = logfile_line.split(";")
    #read in the information of the logged msg
    timestamp= log_data[1]
    canID = log_data[0]
    direction = log_data[2]
    msg_type = log_data[3] 
    dlc = log_data[4]
    data = str(log_data[5])
    print(data)
    diff = log_data[6]
    frame= dbc_structure.get(str(canID))
    decoded_frame = map_data_to_frame(frame, data)
    #print(decoded_frame)
   


