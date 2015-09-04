import multiprocessing
import time
from enum import Enum

class LogType(Enum):
    """ Enum for log types

    Reference with LogType.type
    """
    notice = 1
    stat = 2
    error = 3
    debug = 4


class Log:
    """ Data structure for logs
    """
    def __init__(self, log_type, module, log_time, data):
        """
        log_type: Enum log type
        module: Name of logged module
        log_time: Time of log
        data:   Dictionary of logged attributes
        """
        self.log_type = log_type
        self.module = module
        self.log_time = log_time
        self.data = data

    def __str__(self):
        out_str = time.strftime("%d/%m/%y %X", self.log_time) + " " + self.module + "[" + self.log_type.name + "] "
        for k,v in self.data.iteritems():
            out_str += k + ":" + str(v) +" "
        return out_str

class Logging(multiprocessing.Process):
    """ Module to distribute logging from the uav modules

    Logs will be writen to the registered queues depending on which types
    they wish to observe
    """
    def __init__(self, log_q, outputs):
        """
        :param log_q: incoming logs from modules
        :param outputs: tuple of log file, external interface logs and the log types to listen to
        """
        super(Logging, self).__init__()
        self.log_q = log_q
        log_file, self.file_log_types, self.ilog_q, self.ilog_types = outputs
        self.log_file = open(log_file, 'w', 0)
        self.module_name = self.__class__.__name__

    def run(self):
        while True:
            log = self.log_q.get()

            # Write to outputs that have registered to listen to this log type
            if log.log_type in self.file_log_types:
                self.log_file.write(str(log) + '\n')
            if log.log_type in self.ilog_types:
                self.ilog_q.put(log)

        self.log_file.close()
