from .. import TinyCan as tiny_can


def connect_api(can_driver,baudrate, snr=None, attempts=5):
    current_attempt=0
    while(current_attempt<attempts):
        status = can_driver.OpenComplete(canSpeed=baudrate, snr=snr)
        #if status is None no error 
        if status:
            current_attempt+=1
        else:
            return 1
    return -1

def connect_tiny_can(baudrate,reconnect_attemps):
    #initalize CanDriver
    can_driver=tiny_can.mhsTinyCanDriver.MhsTinyCanDriver()
    status = connect_api(can_driver,baudrate,attempts=reconnect_attemps)
    can_driver.CanSetUpEvents(PnPEventCallbackfunc=PnPEventCallback,
                          StatusEventCallbackfunc=StatusEventCallback,
                          RxEventCallbackfunc=RxEventCallback)

