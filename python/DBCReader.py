# this file is used to read in a dbc file
# therefore the data that gets send over can can be interpreted with this file
import re
import time

# select a dbcfile and a datalogging file

def read_dbc(file = "CANoe_C23.dbc"):
    print("dbc reader")
    with open(file,"r",errors='ignore') as dbc_handle:
        dbc_file = dbc_handle.read()
    print(dbc_file)
    print("test")
   

    frames = {}
    frame_counter = 0
    current_frame = None
    current_frame_id = None
    signal_counter = 0 
    current_signal_name = None
    print(dbc_file)
    #iterate through each line in DBC file
    for dbc_line in dbc_file.split("\n"):
        print(dbc_line)
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
        print("signal {}".format(signal))
        start_bit=int(signal.get("start_bit"))
        length=int(signal.get("length"))
        scale=float(signal.get("scale"))
        offset=float(signal.get("offset"))
        unit=str(signal.get("unit"))
        endinanes = str(signal.get("endinanes"))
        print("Signal parameter {},{},{},{}".format(start_bit,length,scale,offset,unit,endinanes))

        if endinanes == "1":
            #@1-> little endinanes/intel
            real_bit_start = start_bit
        else:
            #@0 -> big endinanes/motorla
            real_bit_start = start_bit-length

       # print("stat:{}, length :{}, scale:{}, offset:{}, unit:{}, data:{}".format(start_bit,length,scale,offset,unit,data))
        #get the concrete values of each signal
                   
        #create a bitmask while shifting with 1 and orring with
        bitmask=0
        print("real bit start {}".format(real_bit_start))
        for i in range(length):
            bitmask=(bitmask<<1)|1

        for i in range(real_bit_start):
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
        #print(value)
        return value



def map_data_to_frame(frame, data):
    #print("MAP data {},to frame{}".format(data,frame))
    decoded_frame = {}
    #convert hex data to integer
    data = data.replace(" ","") 
    #print("hex ", data)
    data = int(str(data),16)
    #print("dec ", data)
    #iterate through all signals in this frame
    for signal in frame.get("signals"):

        print("signal {}".format(signal))
        mapped_data = map_data_to_signal(frame.get("signals").get(signal), data)
        #print(signal,mapped_data
        decoded_signal = {
                "data" : mapped_data,
               "unit" : frame.get("signals").get(signal).get("unit")
        }

        decoded_frame.update({
            signal : decoded_signal
            })
    #print(decoded_frame)
    return decoded_frame



def map_log_file(file_name,dbc):
    
    
    decoded_string = ""
    log_file = open(file_name)
    #iterate through data file
    for line_number, logfile_line in enumerate(log_file):
        if line_number == 0:
            pass
        else:
            print(line_number)
            print("----------line------------")
            print(logfile_line) 
            logfile_line = re.sub("\n","",str(logfile_line))
            print(logfile_line)
            log_data = logfile_line.split(";")
            print(log_data)
            #read in the information of the logged msg
            timestamp= log_data[1]
            canID = log_data[0]
            direction = log_data[2]
            msg_type = log_data[3] 
            dlc = log_data[4]
            data = str(log_data[5])
            print(data)
            diff = log_data[6]
            frame= dbc.get(str(canID))
            decoded_frame = map_data_to_frame(frame, data)

            decoded_string+=logfile_line+"<<<<"
            for signal_name in decoded_frame:
                data = decoded_frame.get(signal_name).get("data")
                unit = decoded_frame.get(signal_name).get("unit")
                decoded_string += "{"+signal_name+":"+str(data)+":"+unit+"}"
            decoded_string+="\n"
            print(decoded_string)

            with open("files/testdbc_map.txt","w") as dbc_map_file:
                dbc_map_file.write(decoded_string)










############################################
###########################################
##########################################

##read dbc in dicct
#dbc_structure = read_dbc("files/CANoe_C23.dbc")
#print(dbc_structure)
#map_log_file("files/20230412_174933_DATA_0.txt",dbc_structure)

   


