

class SDevice:
    def __init__(self,port='',baud='',noDevice=False):
        self.__imports__()
        self.__log__     = Log().logger
        self.noDevice = noDevice

        if not port and not noDevice: #automatically assign one
            try               :
                self.device   = self.get_active_ports()[0].device
                self.__log__.debug(f"Found device at : {self.device}")
            except IndexError :self.noDevice = True
        else        : self.device  = port

        if self.noDevice : 
            self.__log__.warning("NO DEVICE DETECTED")
            self.device        = -1
            self.port          = -1
            self.serial_device = -1
        else:
            if not baud : self.baud    = '57600'
            else        : baud         = baud

            self.__log__.debug(f"Initializing Serial Comms on Port:{self.device} at BAUD:{self.baud}")
            self.serial_device = self.connect(self.device,self.baud)
            self.__log__.debug(f"Comms setup complete")

    def __imports__(self):
        try     : import serial as s
        except  : self.s = None
        else    : self.s = s

        try     : from serial.tools import list_ports as lp
        except  : self.list_ports  = None
        else    : self.list_ports  = lp

        try     : import logging
        except  : self.logging = None
        else    : self.logging = logging

    def get_active_ports(self):
        if self.noDevice : return 0
        active_ports = self.list_ports.comports()
        return active_ports
    
    def poll_serial(self):
        if self.noDevice : return 0
        lines = []
        if self.serial_device.in_waiting : 
            line = self.serial_device.readline().decode().strip("\n").strip("\r")
            lines.append(line)
        return 
        
    def connect(self,device,baud):
        if self.noDevice : return 0
        connection = self.s.Serial(self.device,self.baud)
        return connection

    def disconnect(self):
        if self.noDevice : return 0
        self.serial_device.close()

    def send_message(self,message):
        if self.noDevice : return 0
        serial_message = message.encode()
        self.serial_device.write(serial_message)

    def update_baud(self,baud):
        self.__log__.debug(f"Updating to BAUD: {baud}")
        if self.noDevice : return 0
        self.disconnect()
        self.baud = baud
        self.connect(self.device,self.baud)