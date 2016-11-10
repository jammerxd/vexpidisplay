from time import gmtime,strftime
import os
class Debugger:
    def __init__(self,logFile=False):
        if os.name == "nt":
            self.logName = os.path.join("logs",strftime("%Y-%m-%d %H-%M-%S", gmtime()) + ".log")
        elif os.name == "posix":
            self.logName = "./logs/" + strftime("%Y-%m-%d %H-%M-%S", gmtime()) + ".log"
        self.logFile = False
        if logFile != False:
            self.logName = logFile

    def log(self,txt):
        self.logFile = open(self.logName,"w")
        self.logFile.write("[" + strftime("%H:%M:%S",gmtime()) + "]    " + txt)
        self.logFile.close()
