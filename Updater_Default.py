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

class Team:
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
class Match:
    def __init__(self):
        self.match = ""
        self.redTeams = []
        self.blueTeams = []
        self.redScore = ""
        self.blueScore = ""
    def debugString(self):
        print ("---------------------")
        print ("Match: " + self.match)
        print ("Red score " + self.redScore)
        print ("Blue score " + self.blueScore)
        print ("Red Teams: ")
        for team in self.redTeams:
            print (team.name)
        print ("Blue Teams: ")
        for team in self.blueTeams:
            print (team.name)
        print ("---------------------")
class UpdateInfo:
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
        if sponsorDir != False:
            #print sponsorDir
            if os.path.isdir(os.path.join(sponsorDir)):
                self.localSponsors = glob.glob(os.path.join(sponsorDir,"*.png"))
        if len(self.localSponsors) > 0:
            self.localSponsorIndex = 0
        else:
            self.localSponsorIndex = -1
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
        raw_html = self.getURL("/matches")
        if(raw_html != ""):
            tableBody = raw_html.split("<tbody>")[1]
            tableBody = tableBody.split("</tbody>")[0]
            index = 0
            for row in tableBody.split("<tr>"):
                tempMatch = Match()
                raw_data = row.replace("</tr>","").split('\n')
                if(len(raw_data) == 26):
                    dI = 0
                    for data in raw_data:
                        if(dI != 15 and dI != 20):
                            data = data[data.find(">")+1:data.find("<",data.find(">"))]
                            raw_data[dI] = data
                        elif(dI == 15 or dI == 20):
                            data = data.replace("<strong>","").replace("</strong","")
                            raw_data[dI] = data
                        
                        dI += 1
                    

                    tempMatch.match = raw_data[1]
                    tempMatch.redScore = raw_data[15]
                    tempMatch.blueScore = raw_data[20]

                    tempMatch.redTeams.append(raw_data[4])
                    tempMatch.redTeams.append(raw_data[6])

                    tempMatch.blueTeams.append(raw_data[9])
                    tempMatch.blueTeams.append(raw_data[11])
                    self.matches[index] = tempMatch
                elif(len(raw_data) == 30):
                    dI = 0
                    for data in raw_data:
                        if(dI != 19 and dI != 24):
                            data = data[data.find(">")+1:data.find("<",data.find(">"))]
                            raw_data[dI] = data
                        elif(dI == 19 or dI == 24):
                            data = data.replace("<strong>","").replace("</strong","")
                            raw_data[dI] = data
                        
                        dI += 1
                    

                    tempMatch.match = raw_data[1]
                    tempMatch.redScore = raw_data[19]
                    tempMatch.blueScore = raw_data[24]

                    tempMatch.redTeams.append(raw_data[4])
                    tempMatch.redTeams.append(raw_data[6])
                    tempMatch.redTeams.append(raw_data[8])

                    tempMatch.blueTeams.append(raw_data[11])
                    tempMatch.blueTeams.append(raw_data[13])
                    tempMatch.blueTeams.append(raw_data[15])
                    
                    self.matches[index] = tempMatch
                index += 1
    def getEventName(self):
        name = self.getURL("").split("<title>")[1].split("</title")[0].split("::")[1]
        self.eventName = name
    def getURL(self,URL=""):
        #print ("SERVER: " + self.serverURL + URL)
        data = urlopen(self.serverURL + URL).read().decode('utf-8')
        return data
    
#update = UpdateInfo("http://192.168.1.135:80/division1","./sponsors")
#update.start()
#for i in range(0,len(update.teams)):
#    print(update.teams[update.ranks[str(i+1)]].name)
    
