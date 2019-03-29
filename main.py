
import sys

import serialWindow    as     sw
from   PyQt5           import QtCore,QtWidgets
from   PyQt5.QtWidgets import QApplication, QMainWindow

from logg import Log


class MainWindow(QMainWindow, sw.Ui_MainWindow):
    """
    Main window for the Python Arduino serial monitor
    ...

    Attributes
    ----------
    SDevice : object
        Object governing the serial device the window is using. Use this.

    serial_device : object
        Literal serial device instance. Don't use this.
    
    serialOutput : list
        Text that is displayed on the output window. 

    Methods
    -------
    update_display
        Update the output display

    clear_display
        Clear the output display

    send_message
        Send message via serial comms

    check messages
        Check for messages on the serial buffer

    """
    def __init__(self,max_message_legth=250):
        self.__log__         = Log().logger
        self.__maxlen__      = max_message_legth

        self.__log__.debug("Initializing the Main Window")
        super(MainWindow,self).__init__()
        self.setupUi(self)
        self.__imports__()

        self.__log__.debug("Initializing Serial Comms")
        self.serialOutput  = []
        self.SDevice       = self.SerialDeviceLib()
        self.serial_device = self.SDevice.serial_device

        self.__log__.debug("Setting GUI hooks")
        self.__set_hooks__()
        self.__log__.debug("Done hooking")

    def __imports__(self):
        try        : from serial_comms import SDevice
        except     : self.SerialDeviceLib = None
        else       : self.SerialDeviceLib = SDevice

        try        : import scipy
        except     : self.scipy = None
        else       : self.scipy = scipy

    def __set_hooks__(self,pollIntervalMS=150,barUpdateInvervalMS=500):
        self.__log__.debug("Setting up callback on return-key press for message line")
        self.messageLine.returnPressed.connect(self.send_message)
        self.__log__.debug("Setting up callback on send button press for message line")
        self.sendButton.pressed.connect(self.send_message)
        
        self.__log__.debug("Firing off a timer for polling the serial buffer")
        self.poll_timer = QtCore.QTimer()
        self.poll_timer.timeout.connect(self.check_messages)
        self.poll_timer.start(pollIntervalMS)

        self.__log__.debug("Firing off a timer for updating the status bar")
        self.bar_timer = QtCore.QTimer()
        self.bar_timer.timeout.connect(self.update_status_bar)
        self.bar_timer.start(barUpdateInvervalMS)

        self.__log__.debug("Hooking drop-down menu items to their respective functions")
        self.actionClear_Output.triggered.connect(self.clear_display)
        self.actionQuit.triggered.connect(self.close)
        
        PORTS          = self.SDevice.get_active_ports()
        
        BAUD           = [300*2**i for i in range(7)] ; lastBinaryBAUD = BAUD[-1]
        for i in range(1,7) : BAUD.append(lastBinaryBAUD*i)

        _translate     = QtCore.QCoreApplication.translate
        
        self.BAUDItems = []
        for rate in BAUD:
            widget = QtWidgets.QAction(self)
            label  = f"{rate}" 
            self.BAUDItems.append(widget)
            self.BAUDItems[-1].setObjectName(label)
            self.menuBAUD.addAction(self.BAUDItems[-1])
            self.BAUDItems[-1].setText(_translate("MainWindow", label))
            self.BAUDItems[-1].triggered.connect\
                 (lambda x,rate=rate : self.SDevice.update_baud(  rate ))

        self.PORTItems = []
        for port in PORTS:
            widget = QtWidgets.QAction(self)
            label  = f"{port}" 
            self.PORTItems.append(widget)
            self.PORTItems[-1].setObjectName(label)
            self.menuPORT.addAction(self.PORTItems[-1])
            self.PORTItems[-1].setText(_translate("MainWindow",label))
            self.PORTItems[-1].triggered.connect\
                (lambda x,port=port : self.SDevice.update_port(port.device))


    def update_status_bar(self):
        message = f'PORT:{self.serial_device.name} BAUD:{self.serial_device.baudrate}'
        self.statusbar.showMessage(message)

    def update_display(self,line):
        self.serialOutput.append(line)
        display_text = "\n".join(self.serialOutput)
        self.serialDisplay.setText(display_text)
        self.serialDisplay.verticalScrollBar().setValue(\
            self.serialDisplay.verticalScrollBar().maximum())

    def clear_display(self):
        self.serialOutput = []
        self.update_display('')

    def send_message(self):
        self.__log__.debug("Woohoo input detected! Reading message")
        message = self.messageLine.text()
        
        self.__log__.debug("Message read, clearing input box")
        self.messageLine.clear()

        if len(message) : 
            self.__log__.debug(f"Message read was {message}. Sending it out")
            #self.SDevice.send_message(message)
            self.send_data(message,'text')
            self.__log__.debug("Done. Updating display now")
            self.update_display(message)
        else : 
            self.__log__.debug("False alarm, nothing read :(")

    def check_messages(self):
        try    : 
            lines = self.SDevice.poll_serial()
        except : 
            self.__log__.warning("Incorrect settings for serial comms used!!")
            lines = []
            
        if lines : 
            for line in lines:
                self.__log__.debug(f"Found {line} on serial buffer")
                self.update_display(line)

    def send_data(self,data,file_name):
        bdata        = list(map(ord,data))
        total_chunks = self.scipy.ceil(len(bdata)/self.__maxlen__).astype(self.scipy.uint32)
        unique_ID    = self.__get_unique_id__()
        ftype        = self.__send_type__(file_name)
        low          = total_chunks & 0x0000ff
        med          = total_chunks & 0x00ff00
        high         = total_chunks & 0xff0000
        header       = f"{ftype}{unique_ID}{high}{med}{low}"
        print(header)
        #self.SDevice.send_message(header)
        return 0
    
    def __send_type__(self,file_name):
        if file_name == 'text' : return chr(0)
        else                   : return chr(2)

    def __get_unique_id__(self):
        ranNum = 255*self.scipy.random.random()
        return self.scipy.array(ranNum).astype(self.scipy.uint8)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
