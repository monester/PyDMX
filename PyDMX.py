import serial
import time


class PyDMX:
    def __init__(self,COM='COM8',Cnumber=512,Brate=250000,Bsize=8,StopB=2,use_prev_data=False):
        #start serial
        self.channel_num = Cnumber
        self.data = [0] * (self.channel_num + 1)
        self.ser = serial.Serial(COM,baudrate=Brate,bytesize=Bsize,stopbits=StopB)
        self.sleepms = 50.0
        self.breakus = 176.0
        self.MABus = 16.0
        
    def set_data(self,id,data):
        self.data[id] = data

    def set_datalist(self, list_id, list_data):
        try:
            for id,data in zip(list_id, list_data):
                self.set_data(id, data)
        except:
            print('list of id and data must be the same size!')

    def send(self):
        # Send Break : 88us - 1s
        self.ser.break_condition = True
        time.sleep(self.breakus/1000000.0)
        
        # Send MAB : 8us - 1s
        self.ser.break_condition = False
        time.sleep(self.MABus/1000000.0)
        
        # Send Data
        self.ser.write(bytearray(self.data))
        
        # Sleep
        time.sleep(self.sleepms/1000.0) # between 0 - 1 sec

    def sendzero(self):
        self.data = [0] * (self.channel_num + 1)
        self.send()

    def __del__(self):
        print('Close serial server!')
        # close with preserving current DMX data, I guess you may not need to reset DMX signal in this option.
        self.sendzero()
        self.ser.close()
    


if __name__ == '__main__':
    dmx = PyDMX('COM11')

    dmx.send()
    
    del dmx
