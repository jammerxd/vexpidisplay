import time
import threading
import json
#from urllib.request import urlopen
from urllib2 import urlopen
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
    def getTeams(self):
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
    def getRankings(self):
        raw_html = self.getURL("/rankings")
        if(raw_html != ""):
            tableBody = raw_html.split("<tbody>")[1]
            tableBody = tableBody.split("</tbody>")[0]
            tI = 0
            for row in tableBody.split("<tr>"):
                raw_data = row.replace("</tr>","").replace("<td>","").replace("<td class=\"td-centered\">","").replace("<td class=\"td-centered\" nowrap=\"nowrap\">","").replace("</td>","").split('\n')
                
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
    def getMatches(self):
        #self.matches = []
        self.updatedMatches = []
        raw_html = self.getURL("/matches")
        foundMatchScored = False
        if(raw_html != ""):
            tableBody = raw_html.split("<tbody>")[1]
            tableBody = tableBody.split("</tbody>")[0]
            index = 0

            matchI = 0
            fieldI = 1
            timeI = 2
            redTeam1I = 3
            redTeam2I = 4
            blueTeam1I = 5
            blueTeam2I = 6
            redScoreI = 7
            blueScoreI = 8
            matchScoredI = 9
            fieldCount = 0
            self.showMatches = {}
            for row in tableBody.split("<tr>"):
                tempMatch = Match()
                raw_data = row.replace("</tr>","").split("<td")
                if len(raw_data) == 11:
                    for x in range(0,len(raw_data)):
                        start = raw_data[x].find(">") + 1
                        end = raw_data[x].rfind("<",start)
                        raw_data[x] = raw_data[x][start:end].replace('\n','')
                    raw_data[len(raw_data)-1] =  raw_data[len(raw_data)-1][0:raw_data[len(raw_data)-1].rfind("</td")]

                    del raw_data[0]
                    
                    start = raw_data[redScoreI].find(">") + 1
                    end = raw_data[redScoreI].rfind("</strong",start)
                    end  = end if end > 0  else len(raw_data[redScoreI])
                    raw_data[redScoreI] = raw_data[redScoreI][start:end]

                    start = raw_data[blueScoreI].find(">") + 1
                    end = raw_data[blueScoreI].rfind("</strong",start)
                    end  = end if end > 0  else len(raw_data[blueScoreI])
                    raw_data[blueScoreI] = raw_data[blueScoreI][start:end]

                    tempMatch.match = raw_data[matchI]
                    tempMatch.blueScore = raw_data[blueScoreI]
                    tempMatch.redScore = raw_data[redScoreI]
                    tempMatch.redTeams.append(raw_data[redTeam1I])
                    tempMatch.redTeams.append(raw_data[redTeam2I])
                
                    tempMatch.blueTeams.append(raw_data[blueTeam1I])
                    tempMatch.blueTeams.append(raw_data[blueTeam2I])
                    tempMatch.field = raw_data[fieldI]
                    tempMatch.matchScored = True if raw_data[matchScoredI] == "Yes" else False
                    if os.name == 'nt':
                        tempMatch.time = time.strftime('%I:%M %p', time.localtime(int(raw_data[timeI]))).upper()
                        if tempMatch.time[0] == "0":
                            tempMatch.time = tempMatch.time[1:]
                    else:
                        tempMatch.time = time.strftime('%-I:%M %p', time.localtime(int(raw_data[timeI]))).upper()
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
                            
                    while len(self.showMatches) < 8:
                        number = self.lastMatchScored+1+i
                        if number in self.matches:
                            self.showMatches[match] = number
                            match+=1
                            i+=1
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
        
        raw_html = self.getURL("")
        if raw_html != "":
            name = raw_html.split("<title>")[1].split("</title")[0].split("::")[1]
            self.eventName = name
    def getURL(self,URL=""):
        try:
            data = urlopen(self.serverURL + URL).read().decode('utf-8')
            self.dataUpdateSuccess = True
        except Exception,ex:
            data = ""
            self.dataUpdateSuccess = False
        return data
    
##update = UpdateInfo("http://localhost:8080/division1","./sponsors")
##update.start()
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
    
