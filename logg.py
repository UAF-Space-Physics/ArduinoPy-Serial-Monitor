

class Log :
    """
    Class to instantiate a homogeneous python logger
    ...

    Attributes
    ----------
    logger : object
        This is the instantiated logger. Use it.

    Methods
    -------
    None

    """
    def __init__(self,name='Log9000'):
        self.__imports__()
        self.__setup_logger__(name)

    def __imports__(self):
        try    : import logging
        except : self.logging = None
        else   : self.logging = logging

    def __setup_logger__(self,name):
        log_format  = self.logging.Formatter('%(asctime)s %(levelname)s %(processName)s : %(message)s')
        log_handler = self.logging.StreamHandler()
        log_handler.setFormatter(log_format)

        self.logger = self.logging.getLogger(name)
        self.logger.setLevel  (   "DEBUG")

        if not self.logger.handlers:
            self.logger.addHandler(log_handler)
