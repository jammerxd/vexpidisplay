import time
import threading
import json
#from urllib.request import urlopen
import urllib2
#import urlib
#import urllib2

import os.path
import os
import sys
import glob
from array import array
from FieldSet import *
class Team(object):
    def __init__(self):
        self.number = ""
        self.name = ""
        self.location = ""
        self.school = ""

        self.rank = ""
        self.wins = ""
        self.losses = ""
        self.ties = ""
        self.wps = ""
        self.aps = ""
        self.sps = ""

        self.ranksStr = ""
class Match(object):
    def __init__(self):
        self.match = ""
        self.redTeams = []
        self.blueTeams = []
        self.redScore = ""
        self.blueScore = ""
        self.field = ""
        self.matchScored = False
        self.updated = False
        self.scoresUpdated = False
        self.time="N/A"
        self.onField = False
        self.onDeck = False
    def __eq__(self,other):
        if isinstance(other,Match):
            if (other.match == self.match and
                other.redTeams == self.redTeams and
                other.blueTeams == self.blueTeams and
                other.redScore == self.redScore and
                other.field == self.field and
                other.matchScored == self.matchScored ):
                return True
            else:
                return False
        else:
            return False
    def __ne__(self,other):
        if isinstance(other,Match):
            if (other.match == self.match and
                other.redTeams == self.redTeams and
                other.blueTeams == self.blueTeams and
                other.redScore == self.redScore and
                other.field == self.field and
                other.matchScored == self.matchScored):
                return False
            else:
                return True
        else:
            return True
    def debugString(self):
        print ("---------------------")
        print ("Match: " + self.match)
        print ("Red score " + self.redScore)
        print ("Blue score " + self.blueScore)
        print ("Red Teams: ")
        for team in self.redTeams:
            print (team)
        print ("Blue Teams: ")
        for team in self.blueTeams:
            print (team)
        print ("---------------------")
class UpdateInfo(object):
    def __init__(self,serverURL,sponsorDir=False):
        self.serverURL = serverURL
        self.eventName = ""
        self.teams = {}
        self.matches = {}
        self.ranks = {}
        self.rankTBs = {}
        self.rankHeight = 100
        self.localSponsors = []
        self.localSponsorIndex = -1
        self.maxTeamNameChars = 0
        self.maxRankChars = 0;
        self.rankAvail = False
        self.updatedMatches = []
        self.showMatches = {}
        self.dataUpdateSuccess = False
        self.matchesUnscored = False
        for i in range(8):
            self.showMatches[i] = None
        self.lastMatchScored = -1
	
        if sponsorDir != False:
            #print sponsorDir
            if os.path.isdir(os.path.join(sponsorDir)):
                self.localSponsors = glob.glob(os.path.join(sponsorDir,"*.png"))
        if len(self.localSponsors) > 0:
            self.localSponsorIndex = 0
        else:
            self.localSponsorIndex = -1
			
        self.fieldMatches = {}
        self.fieldOrder = {}
        #print(self.localSponsorIndex)

    
    def start(self):
        self.getEventName()
        self.getTeams()
        self.getRankings()
        self.getMatches()
    def getTeams_old(self):
        raw_html = self.getURL("/teams")
        if(raw_html != ""):
            tableBody = raw_html.split("<tbody>")[1]
            tableBody = tableBody.split("</tbody>")[0]
            index = 0
            for row in tableBody.split("<tr>"):  
                raw_data = row.replace("</tr>","").replace("<td>","").replace("</td>","").split('\n')
                if(len(raw_data) == 8):                    
                    tempTeam = Team()
                    tempTeam.number = str(raw_data[1])
                    tempTeam.name = raw_data[2]
                    tempTeam.location = raw_data[3]
                    tempTeam.school = raw_data[4]
                    self.teams[str(tempTeam.number)] = tempTeam
                    if self.maxTeamNameChars < len(tempTeam.name):
                        self.maxTeamNameChars = len(tempTeam.name)
                index+=1
        else:
            while(len(self.teams) == 0):
                if(len(self.teams) > 0):
                   break;
                else:
                    time.sleep(30)
                    self.getTeams()
    def getTeams(self):
        jsonStr = self.getURL("/teams",False)
        if(jsonStr != "" and jsonStr != None):
            jsonData = json.loads(jsonStr)["teams"]
            
            for data in jsonData:
                tempTeam = Team()
                tempTeam.number = data["number"]
                tempTeam.name = data["name"]
                tempTeam.school = data["school"]
                tempTeam.location = data["town"] + ", " + data["state"] + ", " + data["country"]
                self.teams[tempTeam.number] = tempTeam
                if self.maxTeamNameChars < len(tempTeam.name):
                    self.maxTeamNameChars = len(tempTeam.name)
        else:
            time.sleep(5)
            self.getTeams()
    def getRankings_old(self):#OLD
        print "RANKING FETCH"
        raw_html = self.getURL("/rankings",False,True)
        #print raw_html
        if(raw_html != ""):
            tableBody = raw_html.split("<tbody>")[1]
            tableBody = tableBody.split("</tbody>")[0]
            
            tI = 0
            for row in tableBody.split("<tr>"):
                raw_data = row.replace("</tr>","").replace("<td>","").replace("<td class=\"td-centered\">","").replace("<td class=\"td-centered\" nowrap=\"nowrap\">","").replace("</td>","").split('\n')
                #raw_data = []
                #print str(row)
                #print len(raw_data)
                if len(raw_data) == 13:
                    teamNumber = str(raw_data[2])
                    self.teams[teamNumber].rank = str(raw_data[1])
                    self.teams[teamNumber].wins = str(raw_data[4].split("-")[0])
                    self.teams[teamNumber].losses = str(raw_data[4].split("-")[1])
                    self.teams[teamNumber].ties = str(raw_data[4].split("-")[2])
                    self.teams[teamNumber].wps = str(raw_data[5])
                    self.teams[teamNumber].aps = str(raw_data[7])
                    self.teams[teamNumber].sps = str(raw_data[9])
                    self.teams[teamNumber].ranksStr = str(self.teams[teamNumber].rank).rjust(len(str(len(self.teams)))) + "  "
                    self.teams[teamNumber].ranksStr += '{:^6}'.format(str(self.teams[teamNumber].number)) + "  "
                    self.teams[teamNumber].ranksStr += str('{:^'+str(self.maxTeamNameChars)+'}').format(str(self.teams[teamNumber].name)) + "  "
                    self.teams[teamNumber].ranksStr += '{:^8}'.format(str(self.teams[teamNumber].wins) + "-" + self.teams[teamNumber].losses + "-" + self.teams[teamNumber].ties) + "  "
                    self.teams[teamNumber].ranksStr += '{:^11}'.format(str(self.teams[teamNumber].wps) + "-" + self.teams[teamNumber].aps + "-" + self.teams[teamNumber].sps) + "  "
                    if len(self.teams[teamNumber].ranksStr) > self.maxRankChars:
                        self.maxRankChars = len(self.teams[teamNumber].ranksStr)
                    self.ranks[str(tI+1)] = teamNumber
                    tI+=1
        if len(self.ranks) == 0:
            i = 0
            for team in self.teams:
                self.teams[team].rank = str(i+1)
                self.teams[team].wins = "0"
                self.teams[team].losses = "0"
                self.teams[team].ties = "0"
                self.teams[team].wps = "0"
                self.teams[team].aps = "0"
                self.teams[team].sps = "0"
                self.ranks[str(i+1)] = self.teams[team].number
                i += 1
            self.ranksAvail = False
        else:
            self.ranksAvail = True
    def getRankings(self):
        jsonStr = self.getURL("/ranks")#NEW
        if(jsonStr != "" and jsonStr != None):
            jsonData = json.loads(jsonStr)["ranks"]
            tI = 0
            for data in jsonData:
                teamNumber = data["number"]
                self.teams[teamNumber].rank = data["rank"]
                self.teams[teamNumber].wins = data["wins"]
                self.teams[teamNumber].losses = data["losses"]
                self.teams[teamNumber].ties = data["ties"]
                self.teams[teamNumber].wps = data["wps"]
                self.teams[teamNumber].aps = data["aps"]
                self.teams[teamNumber].sps = data["sps"]
                self.ranks[str(tI+1)] = teamNumber
                self.teams[teamNumber].ranksStr = str(self.teams[teamNumber].rank).rjust(len(str(len(self.teams)))) + "  "
                self.teams[teamNumber].ranksStr += '{:^6}'.format(str(self.teams[teamNumber].number)) + "  "
                self.teams[teamNumber].ranksStr += str('{:^'+str(self.maxTeamNameChars)+'}').format(str(self.teams[teamNumber].name)) + "  "
                self.teams[teamNumber].ranksStr += '{:^8}'.format(str(self.teams[teamNumber].wins) + "-" + self.teams[teamNumber].losses + "-" + self.teams[teamNumber].ties) + "  "
                self.teams[teamNumber].ranksStr += '{:^11}'.format(str(self.teams[teamNumber].wps) + "-" + self.teams[teamNumber].aps + "-" + self.teams[teamNumber].sps) + "  "
                if len(self.teams[teamNumber].ranksStr) > self.maxRankChars:
                    self.maxRankChars = len(self.teams[teamNumber].ranksStr)                 
                tI += 1
        if len(self.ranks) == 0:
            i = 0
            for team in self.teams:
                self.teams[team].rank = str(i+1)
                self.teams[team].wins = "0"
                self.teams[team].losses = "0"
                self.teams[team].ties = "0"
                self.teams[team].wps = "0"
                self.teams[team].aps = "0"
                self.teams[team].sps = "0"
                self.ranks[str(i+1)] = self.teams[team].number
                self.teams[teamNumber].ranksStr = str(self.teams[teamNumber].rank).rjust(len(str(len(self.teams)))) + "  "
                self.teams[teamNumber].ranksStr += '{:^6}'.format(str(self.teams[teamNumber].number)) + "  "
                self.teams[teamNumber].ranksStr += str('{:^'+str(self.maxTeamNameChars)+'}').format(str(self.teams[teamNumber].name)) + "  "
                self.teams[teamNumber].ranksStr += '{:^8}'.format(str(self.teams[teamNumber].wins) + "-" + self.teams[teamNumber].losses + "-" + self.teams[teamNumber].ties) + "  "
                self.teams[teamNumber].ranksStr += '{:^11}'.format(str(self.teams[teamNumber].wps) + "-" + self.teams[teamNumber].aps + "-" + self.teams[teamNumber].sps) + "  "
                if len(self.teams[teamNumber].ranksStr) > self.maxRankChars:
                    self.maxRankChars = len(self.teams[teamNumber].ranksStr)                
                i += 1
            self.ranksAvail = False
        else:
            self.ranksAvail = True
     
    def getMatches(self):
        
        #self.matches = []
        self.updatedMatches = []
        raw_html = self.getURL("/matches")
        foundMatchScored = False
        if(raw_html != "" and raw_html != None):
            jsonData = json.loads(raw_html)["matches"]
            index = 0
            fieldCount = 0
            self.showMatches = {}
            for row in jsonData:
                tempMatch = Match()
                
                

                tempMatch.match = row["match"]
                tempMatch.blueScore = row["blueScore"]
                tempMatch.redScore = row["redScore"]
                tempMatch.redTeams.append(row["red1"])
                tempMatch.redTeams.append(row["red2"])
            
                tempMatch.blueTeams.append(row["blue1"])
                tempMatch.blueTeams.append(row["blue2"])
                tempMatch.field = row["field"]
                tempMatch.matchScored = row["scored"]
                #print tempMatch.match + " | " + str(tempMatch.matchScored)
                if os.name == 'nt':
                    tempMatch.time = time.strftime('%I:%M %p', time.localtime(int(row["scheduledTime"]))).upper()
                    if tempMatch.time[0] == "0":
                        tempMatch.time = tempMatch.time[1:]
                else:
                    tempMatch.time = time.strftime('%-I:%M %p', time.localtime(int(raw_data["scheduledTime"]))).upper()
                if tempMatch.field not in self.fieldMatches:
                    self.fieldMatches[tempMatch.field] = FieldSet(tempMatch.field)
                    self.fieldOrder[fieldCount] = tempMatch.field
                    fieldCount += 1

                if index not in self.fieldMatches[tempMatch.field].matchList:
                    self.fieldMatches[tempMatch.field].matchList.append(index)
                elif index not in self.fieldMatches[tempMatch.field].completedMatches and tempMatch.matchScored == True:
                    self.fieldMatches[tempMatch.field].completedMatches.append(index)

                if tempMatch.matchScored:
                    self.fieldMatches[tempMatch.field].lastMatch = index
                    self.lastMatchScored = index
                    foundMatchScored = True
                else:
                    tempMatch.redScore = ""
                    tempMatch.blueScore = ""
                    if self.fieldMatches[tempMatch.field].nextMatch == None:
                        self.fieldMatches[tempMatch.field].nextMatch = self.fieldMatches[tempMatch.field].matchList.index(index)
                    else:
                        if index-1 in self.matches:
                            if self.fieldMatches[tempMatch.field].nextMatch < index and self.matches[index-1].matchScored == True:
                                self.fieldMatches[tempMatch.field].nextMatch = self.fieldMatches[tempMatch.field].matchList.index(index)
                    self.matchesUnscored = True   
                    
                if index in self.matches:
                    if self.matches[index] != tempMatch:
                        tempMatch.updated = True
                    if self.matches[index].redScore != tempMatch.redScore or self.matches[index].blueScore != tempMatch.blueScore:
                        tempMatch.scoresUpdated = True
                else:
                    tempMatch.updated = True

                if tempMatch.updated or tempMatch.scoresUpdated:
                    self.updatedMatches.append(index)
                                    
                self.matches[index] = tempMatch
                index += 1
            if len(self.matches) > 0:
                if foundMatchScored == False:
                    self.lastMatchScored = 0
                match = 0
                if self.lastMatchScored+1 in self.matches:
                    self.matches[self.lastMatchScored+1].onField = True
                for field in range(len(self.fieldOrder)):
                    if self.lastMatchScored+2+field in self.matches:
                        self.matches[self.lastMatchScored+2+field].onDeck = True
                   
                for i in range(len(self.fieldOrder),-1,-1):
                    number = self.lastMatchScored-i
                    if number in self.matches:
                        self.showMatches[match] = number
                        match += 1
                i = 0
                if self.matchesUnscored:
                    if (len(self.matches) - 1 - self.lastMatchScored < (8-len(self.showMatches))):
                        for i in range(len(self.matches) - self.lastMatchScored):
                            number = self.lastMatchScored+1+i
                            if number in self.matches:
                                self.showMatches[match] = number
                                match+=1
                                i+=1 
                    else:
                        while len(self.showMatches) < 8:
                            number = self.lastMatchScored+1+i
                            if number in self.matches:
                                self.showMatches[match] = number
                                match+=1
                                i+=1
                            else:
                                break
##                        else:
##                            i=0
##                            while len(self.showMatches) < 8:
##                                number = self.showMatches[len(self.showMatches)-1] + i
##                                if number in self.matches:
##                                    self.showMatches[match] = number
##                                    match+=1
##                                i+=1
                else:
                    self.showMatches = {}
        
    def getEventName(self):
        
        raw_html = self.getURL("/eventName",True)
        if raw_html != "" and raw_html != None:
            self.eventName = raw_html
    def getURL(self,URL="",mainDir = False,useWebServer = False):#URL - the sub url to go to inside the division, if mainDir is True, it will skip the division folder. useWebServer URL boolean is to use the TM web server.
        try:
            if (mainDir):
                uri = self.serverURL[:self.serverURL.rfind("/")] + URL
            elif (useWebServer):
                uri = self.serverURL[:self.serverURL.rfind(":")] 
                temp = self.serverURL[self.serverURL.rfind(":")+1:]
                uri += temp[temp.find("/"):] + URL
                
                
            else:
                uri = self.serverURL + URL
            opener = urllib2.build_opener()
            opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
            data = opener.open(uri).read().decode('utf-8')
            self.dataUpdateSuccess = True
        except Exception,ex:
            data = ""
            self.dataUpdateSuccess = False
        return data
    
#update = UpdateInfo("http://192.168.1.72:8989/division1","./sponsors")
#update.getTeams()
#update.getEventName()
#update.getRankings()
#update.getMatches()
##choice = 'y'
##while choice != 'n':
##    update.start()
##    print update.showMatches
##    choice = raw_input("NEXT")
##print update.lastMatchScored
##print update.nextMatches
##for match in update.nextMatches:
##    print update.matches[match].updated
###print update.nextMatches
##my = raw_input("Press a key to continue! ")
##update.start()
##print update.nextMatches
####for field in update.fieldMatches:
####    print update.matches[update.fieldMatches[field].lastMatch].updated
####    print update.matches[update.fieldMatches[field].lastMatch].scoresUpdated
####
##my = raw_input("Press a key to continue! ")
##update.start()
##print update.nextMatches
####for field in update.fieldMatches:
####    print update.matches[update.fieldMatches[field].lastMatch].updated
####    print update.matches[update.fieldMatches[field].lastMatch].scoresUpdated
    
