import os
from urllib2 import urlopen
class Config:
    def __init__(self,configFile="config.ini"):
        self.serverURL = ""
        self.sponsorDir = ""
        self.configFile = configFile
        self.LoadConfig(self.configFile)
        
    def LoadConfig(self,fileName="config.ini"):
        if os.path.exists(fileName):
            self.configFile = fileName
            configFile = open(fileName,"r")
            rawData = configFile.read().splitlines()
            self.serverURL = rawData[0].replace('\n','')
            self.sponsorDir = rawData[1].replace('\n','')

    def SaveConfig(self,fileName="config.ini"):
        saveFile = open(fileName,"w")
        saveFile.write(self.serverURL + "\n")
        saveFile.write(self.sponsorDir + "\n")
        saveFile.close()

    def TestServer(self,server):
        response = -1
        testServer = server.replace("http://","").replace("https://","").split("/")[0]
        testServer = testServer[0:testServer.find(":")]
        
        try:
            data = urlopen(server).read().decode('utf-8')
            self.serverURL = server
            self.SaveConfig(self.configFile)
            return True
        except Exception as ex:
            return False

        
##        if os.name == "nt":#windows
##            response = os.system("ping " + testServer)
##        elif os.name == "posix":
##            response = os.system("ping -c 4 " + testServer)
##
##        if response == 0:
##            self.serverURL = server
##            self.SaveConfig(self.configFile)
##            return True
##        else:
##            return False


