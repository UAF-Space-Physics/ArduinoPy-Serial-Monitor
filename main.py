
import sys

import serialWindow    as     sw
from   PyQt5           import QtCore
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
    def __init__(self):
        self.__log__         = Log().logger

        self.__log__.debug("Initializing the Main Window")
        super(MainWindow,self).__init__()
        self.setupUi(self)

        self.__log__.debug("Initializing Serial Comms")
        self.serialOutput  = []
        self.SDevice       = self.SDevice()
        self.serial_device = self.SDevice.serial_device

        self.__log__.debug("Setting GUI hooks")
        self.__set_hooks__()
        self.__log__.debug("Done hooking")

    def __imports__(self):
        try        : from serial_comms import SDevice
        except     : self.SDevice = None
        else       : self.SDevice = SDevice

    def __set_hooks__(self,pollIntervalMS=150):
        self.__log__.debug("Setting up callback on return-key press for message line")
        self.messageLine.returnPressed.connect(self.send_message)
        self.__log__.debug("Setting up callback on send button press for message line")
        self.sendButton.pressed.connect(self.send_message)
        
        self.__log__.debug("Firing off a timer for polling the serial buffer")
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.check_messages)
        self.timer.start(pollIntervalMS)

        self.__log__.debug("Hooking drop-down menu items to thei respective functions")
        self.actionClear_Output.triggered.connect(self.clear_display)
        self.actionQuit.triggered.connect(self.close)

        #This should be cleaned up into a soft-coded for-loop eventually
        self.BAUD300.triggered.connect   (lambda : self.SDevice.update_baud(    300))
        self.BAUD1200.triggered.connect  (lambda : self.SDevice.update_baud(   1200))
        self.BAUD2400.triggered.connect  (lambda : self.SDevice.update_baud(   2400))
        self.BAUD4800.triggered.connect  (lambda : self.SDevice.update_baud(   4800))
        self.BAUD9600.triggered.connect  (lambda : self.SDevice.update_baud(   9600))
        self.BAUD19200.triggered.connect (lambda : self.SDevice.update_baud(  19200)) 
        self.BAUD38400.triggered.connect (lambda : self.SDevice.update_baud(  38400))
        self.BAUD57600.triggered.connect (lambda : self.SDevice.update_baud(  57600))
        self.BAUD115200.triggered.connect(lambda : self.SDevice.update_baud( 115200))

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
            self.SDevice.send_message(message)
            self.__log__.debug("Done. Updating display now")
            self.update_display(message)
        else : 
            self.__log__.debug("False alarm, nothing read :(")

    def check_messages(self):
        lines = self.SDevice.poll_serial()
        if lines : 
            for line in lines:
                self.__log__.debug(f"Found {line} on serial buffer")
                self.update_display(line)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
