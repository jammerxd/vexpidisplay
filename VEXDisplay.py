import wx, os, sys
from Config import *
from Debugger import *
from Colors import *
from Updater import *
class Header(wx.StaticText):
    def __init__(self,parent,id,text,font,color,pos=(200,12)):
        wx.StaticText.__init__(self,parent,id,text,pos=pos)
        self.SetFont(font)
        self.SetForegroundColour(color)


class MatchPanel(wx.Panel):
    def __init__(self,parent,id,match=None,size=(0,0),pos=(0,0),bg=Colors["White"],fileStr = None):
        wx.Panel.__init__(self,parent,id,pos=pos,size=size)
        self.SetBackgroundColour(bg)
        self.fileStr = fileStr
        if match != None:
            self.matchNum = Header(self,-1,match.match,wx.Font(32,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="NotoSans"),Colors["vexTxtGray"])
            self.matchNum.SetPosition((125-self.matchNum.GetSize()[0],(self.matchNum.GetSize()[1]/2)-12))
        
            self.redTeam1 = Header(self,-1,match.redTeams[0],wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.NORMAL,faceName="NotoSans"),Colors["vexRed"])
            self.redTeam2 = Header(self,-1,match.redTeams[1],wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.NORMAL,faceName="NotoSans"),Colors["vexRed"])
            
            self.blueTeam1 = Header(self,-1,match.blueTeams[0],wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.NORMAL,faceName="NotoSans"),Colors["vexBlue"])
            self.blueTeam2 = Header(self,-1,match.blueTeams[1],wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.NORMAL,faceName="NotoSans"),Colors["vexBlue"])
            
            self.redScore = Header(self,-1,match.redScore,wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.NORMAL,faceName="NotoSans"),Colors["vexRed"])
            self.blueScore = Header(self,-1,match.blueScore,wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.NORMAL,faceName="NotoSans"),Colors["vexBlue"])

            self.field = Header(self,-1,match.field,wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.NORMAL,faceName="NotoSans"),Colors["vexTxtGray"])
            self.time = Header(self,-1,match.time,wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.NORMAL,faceName="NotoSans"),Colors["vexTxtGray"])
            #if match.onField:
            #    self.time.SetLabel("On Field")#ON FIELD
            #if match.onDeck:
            #    self.time.SetFont(wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="NotoSans"))
                
            if match.matchScored == True:
                self.field.Hide()
                self.time.Hide()
                if match.redScore > match.blueScore:
                    self.redTeam1.SetFont(wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="NotoSans"))
                    self.redTeam2.SetFont(wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="NotoSans"))
                    self.redScore.SetFont(wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="NotoSans"))
                elif match.blueScore > match.redScore:
                    self.blueTeam1.SetFont(wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="NotoSans"))
                    self.blueTeam2.SetFont(wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="NotoSans"))
                    self.blueScore.SetFont(wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="NotoSans"))
            else:
                self.field.SetPosition((380+(75-(self.field.GetSize()[0]/2)),(self.field.GetSize()[1]/2)-(18)))
                self.time.SetPosition((380+(75-(self.time.GetSize()[0]/2)),(self.time.GetSize()[1]/2)-(-35)))
            
                
            self.redTeam1.SetPosition((85+(105-(self.redTeam1.GetSize()[0]/2)),(self.redTeam1.GetSize()[1]/2)-18))
            self.redTeam2.SetPosition((215+(105-(self.redTeam2.GetSize()[0]/2)),(self.redTeam2.GetSize()[1]/2)-18))
            self.blueTeam1.SetPosition((85+(105-(self.blueTeam1.GetSize()[0]/2)),(self.blueTeam1.GetSize()[1]/2)-(-35)))
            self.blueTeam2.SetPosition((215+(105-(self.blueTeam2.GetSize()[0]/2)),(self.blueTeam2.GetSize()[1]/2)-(-35)))

            self.redScore.SetPosition((380+(75-(self.redScore.GetSize()[0]/2)),(self.redScore.GetSize()[1]/2)-18))
            self.blueScore.SetPosition((380+(75-(self.blueScore.GetSize()[0]/2)),(self.blueScore.GetSize()[1]/2)-(-35)))
            
        elif fileStr != None and match==None:
            self.bitmap = wx.Bitmap(fileStr,type=wx.BITMAP_TYPE_PNG)
            self.static = wx.StaticBitmap(self,-1,self.bitmap)
            x = (self.GetSize()[0]-self.static.GetSize()[0])/2
            y = (self.GetSize()[1]-self.static.GetSize()[1])/2
            self.static.SetPosition((x,y))
    def updateMatch(self,match):
        ###UPDATE TEXTS HERE###
        if self.fileStr == None:
            self.matchNum.SetLabel(match.match)
            self.matchNum.SetPosition((70+(-(self.matchNum.GetSize()[0]/2)),(self.matchNum.GetSize()[1]/2)-12))
            self.redTeam1.SetLabel(match.redTeams[0])
            self.redTeam2.SetLabel(match.redTeams[1])

            self.blueTeam1.SetLabel(match.blueTeams[0])
            self.blueTeam2.SetLabel(match.blueTeams[1])

            self.redScore.SetLabel(match.redScore)
            self.blueScore.SetLabel(match.blueScore)

            self.field.SetLabel(match.field)
            self.time.SetLabel(match.time)
            
            #if match.onField:
            #    self.time.SetLabel("On Field")
            #    self.time.SetFont(wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="NotoSans"))
            #elif match.onDeck:
            #    self.time.SetLabel("On Deck")
            #    self.time.SetFont(wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="NotoSans"))
            #else:
            #    self.time.SetFont(wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.NORMAL,faceName="NotoSans"))
                
            if match.matchScored == True:
                self.field.Hide()
                self.time.Hide()
                if int(match.redScore) > int(match.blueScore):
                    self.redTeam1.SetFont(wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="NotoSans"))
                    self.redTeam2.SetFont(wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="NotoSans"))
                    self.redScore.SetFont(wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="NotoSans"))

                    self.blueTeam1.SetFont(wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.NORMAL,faceName="NotoSans"))
                    self.blueTeam2.SetFont(wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.NORMAL,faceName="NotoSans"))
                    self.blueScore.SetFont(wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.NORMAL,faceName="NotoSans"))
                    
                elif int(match.blueScore) > int(match.redScore):
                    self.blueTeam1.SetFont(wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="NotoSans"))
                    self.blueTeam2.SetFont(wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="NotoSans"))
                    self.blueScore.SetFont(wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="NotoSans"))
                    
                    self.redTeam1.SetFont(wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.NORMAL,faceName="NotoSans"))
                    self.redTeam2.SetFont(wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.NORMAL,faceName="NotoSans"))
                    self.redScore.SetFont(wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.NORMAL,faceName="NotoSans"))
                else:
                    self.redTeam1.SetFont(wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.NORMAL,faceName="NotoSans"))
                    self.redTeam2.SetFont(wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.NORMAL,faceName="NotoSans"))
                    self.redScore.SetFont(wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.NORMAL,faceName="NotoSans"))

                    self.blueTeam1.SetFont(wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.NORMAL,faceName="NotoSans"))
                    self.blueTeam2.SetFont(wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.NORMAL,faceName="NotoSans"))
                    self.blueScore.SetFont(wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.NORMAL,faceName="NotoSans"))
                    
            else:
                self.field.Show()
                self.time.Show()
                self.field.SetPosition((380+(75-(self.field.GetSize()[0]/2)),(self.field.GetSize()[1]/2)-(18)))
                self.time.SetPosition((380+(75-(self.time.GetSize()[0]/2)),(self.time.GetSize()[1]/2)-(-35)))
            
            self.redTeam1.SetPosition((85+(105-(self.redTeam1.GetSize()[0]/2)),(self.redTeam1.GetSize()[1]/2)-18))
            self.redTeam2.SetPosition((215+(105-(self.redTeam2.GetSize()[0]/2)),(self.redTeam2.GetSize()[1]/2)-18))
            self.blueTeam1.SetPosition((85+(105-(self.blueTeam1.GetSize()[0]/2)),(self.blueTeam1.GetSize()[1]/2)-(-35)))
            self.blueTeam2.SetPosition((215+(105-(self.blueTeam2.GetSize()[0]/2)),(self.blueTeam2.GetSize()[1]/2)-(-35)))

            self.redScore.SetPosition((380+(75-(self.redScore.GetSize()[0]/2)),(self.redScore.GetSize()[1]/2)-18))
            self.blueScore.SetPosition((380+(75-(self.blueScore.GetSize()[0]/2)),(self.blueScore.GetSize()[1]/2)-(-35)))
            
        self.Layout()



class TeamPanel(wx.Panel):
    def __init__(self,parent,id,team=None,size=(0,0),pos=(0,0),bg=Colors["White"],fileStr = None):
        wx.Panel.__init__(self,parent,id,pos=pos,size=size)
        self.SetBackgroundColour(bg)
        self.fileStr = fileStr
        if team != None:
            self.Rank = Header(self,id,team.rank,wx.Font(48,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="NotoSans"),Colors["vexTxtGray"])
            self.Rank.SetPosition((75-(self.Rank.GetSize()[0]/2),-7))

            self.teamNum = Header(self,id,team.number,wx.Font(26,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="NotoSans"),Colors["vexTxtGray"])
            self.teamNum.SetPosition((175,-2))

            self.teamName = Header(self,id,team.name,wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.NORMAL,faceName="NotoSans"),Colors["vexTxtGrayLighter"])
            self.teamName.SetPosition((175,36))

            self.teamWP = Header(self,id,team.wps,wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.NORMAL,faceName="NotoSans"),Colors["vexTxtGrayLighter"])
            x = 850+100
            x = x-(100+(self.teamWP.GetSize()[0])/2)
            self.teamWP.SetPosition((x,18))

            self.teamAP = Header(self,id,team.aps,wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.NORMAL,faceName="NotoSans"),Colors["vexTxtGrayLighter"])
            x = 950+100
            x = x-(100+(self.teamAP.GetSize()[0])/2)
            self.teamAP.SetPosition((x,18))

            self.teamSP = Header(self,id,team.sps,wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.NORMAL,faceName="NotoSans"),Colors["vexTxtGrayLighter"])
            x = 1050+100
            x = x-(100+(self.teamSP.GetSize()[0])/2)
            self.teamSP.SetPosition((x,18))
 
            self.teamWs = Header(self,id,team.wins,wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="NotoSans"),Colors["vexTxtGray"])
            x = 1160
            x = x-(self.teamWs.GetSize()[0])/2
            self.teamWs.SetPosition((x,18))

            self.teamWD = Header(self,id,"-",wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="NotoSans"),Colors["vexTxtGray"])
            x = self.teamWs.GetPosition()[0]+self.teamWs.GetSize()[0]
            self.teamWD.SetPosition((x,16))

            self.teamLs = Header(self,id,team.losses,wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="NotoSans"),Colors["vexTxtGray"])
            x = self.teamWD.GetPosition()[0]+self.teamWD.GetSize()[0]
            self.teamLs.SetPosition((x,18))

            self.teamLD = Header(self,id,"-",wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="NotoSans"),Colors["vexTxtGray"])
            x = self.teamLs.GetPosition()[0]+self.teamLs.GetSize()[0]
            self.teamLD.SetPosition((x,16))

            self.teamTs = Header(self,id,team.ties,wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="NotoSans"),Colors["vexTxtGray"])
            x = self.teamLD.GetPosition()[0]+self.teamLD.GetSize()[0]
            self.teamTs.SetPosition((x,18))
            
        elif fileStr != None:
            self.bitmap = wx.Bitmap(fileStr,type=wx.BITMAP_TYPE_PNG)
            self.static = wx.StaticBitmap(self,-1,self.bitmap)
            x = (self.GetSize()[0]-self.static.GetSize()[0])/2
            y = (self.GetSize()[1]-self.static.GetSize()[1])/2
            self.static.SetPosition((x,y))

class Event(wx.Panel):
    def __init__(self,parent,id,pos=(0,0),size=(120,120)):
        wx.Panel.__init__(self,parent,id,pos=pos,size=size)
        self.Bind(wx.EVT_PAINT,self.OnPaint)
        self.eventMaintainer = None
        
        self.ranksPanel = wx.Panel(self,-1,pos=(25,215),size=(1300,850))
        self.ranksPanelHeight = 850
        self.RankPanels = {}
        self.SchedulePanels = {}
        self.schedulePanel = wx.Panel(self,-1,pos=(1345,215+(850-792)),size=(550,792))
        

        self.SetBackgroundColour(Colors["vexRed"])
        self.ranksPanel.SetBackgroundColour(Colors["Black"])
        self.schedulePanel.SetBackgroundColour(Colors["White"])
        self.RightBannerImg = wx.Bitmap(os.path.join("Images","Display","2016","gear_pattern_right_16x9.png"),type = wx.BITMAP_TYPE_PNG)
        self.LeftBannerImg = wx.Bitmap(os.path.join("Images","Display","2016","gear_pattern_left_16x9.png"),type = wx.BITMAP_TYPE_PNG)
        self.MatchLogoImg = wx.Bitmap(os.path.join("Images","Display","2016","vrc_logo_match_titlebar.png"),type= wx.BITMAP_TYPE_PNG)

        self.Header = Header(self,-1,"Qualification Rankings",wx.Font(60,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="NotoSans"),Colors["White"],(215,20))
        
        
        self.MatchHeader = Header(self,-1,"Match Schedule and Results",wx.Font(24,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="NotoSans"),Colors["White"],(0,0))
        self.MatchHeader.SetPosition((1345+(550-self.MatchHeader.GetSize()[0])/2,215))
        
        self.MatchHeader = Header(self,-1,"Match Schedule and Results",wx.Font(24,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="NotoSans"),Colors["White"],(0,0))
        self.MatchHeader.SetPosition((1345+(550-self.MatchHeader.GetSize()[0])/2,215)) 
        
        self.RankHeader = Header(self,-1,"Rank",wx.Font(24,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="NotoSans"),Colors["White"],(0,0))
        self.RankHeader.SetPosition((((200/2) - (self.RankHeader.GetSize()[0]/2)),170))      
        
        self.TeamHeader = Header(self,-1,"Team",wx.Font(24,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="NotoSans"),Colors["White"],(0,0))
        self.TeamHeader.SetPosition((200,170))

        self.WPHeader = Header(self,-1,"WP",wx.Font(24,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="NotoSans"),Colors["White"],(0,0))
        self.WPHeader.SetPosition((875-(self.WPHeader.GetSize()[0]/2),170))

        self.APHeader = Header(self,-1,"AP",wx.Font(24,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="NotoSans"),Colors["White"],(0,0))
        self.APHeader.SetPosition((975-(self.APHeader.GetSize()[0]/2),170))

        self.SPHeader = Header(self,-1,"SP",wx.Font(24,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="NotoSans"),Colors["White"],(0,0))
        self.SPHeader.SetPosition((1075-(self.SPHeader.GetSize()[0]/2),170))

        self.WLTHeader = Header(self,-1,"W-L-T",wx.Font(24,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="NotoSans"),Colors["White"],(0,0))
        x = 1212-(self.WLTHeader.GetSize()[0]/2)
        self.WLTHeader.SetPosition(( x,170)) 

        self.ResetPositions = False

        self.GlobalSponsors = glob.glob(os.path.join("Images","Display","Logos","Small","*.png"))
        self.GlobalSponsorIndex = 0
        self.GlobalSponsorPanel = TeamPanel(self,-1,None,size=(190,112),pos=(0,25),bg=Colors["White"],fileStr=self.GlobalSponsors[self.GlobalSponsorIndex])

        
        self.rankHeight = 82
        
        self.deltaY = -2
        self.callInterval = 26
        self.logoCheck = 858#858
        
    def SetEvent(self,serverURL,startEvent = False,sponsorDir=False):
        self.eventMaintainer = UpdateInfo(serverURL,sponsorDir)
        if startEvent:
            self.StartEvent()
    def SetupRankPanels(self):
        YOffset = 0
        XOffset = 0
        self.ranksPanelHieght = self.rankHeight*len(self.eventMaintainer.teams)
        isGray = False
        i = 0
        for i in range(0,len(self.eventMaintainer.ranks)):
            tempTeam = self.eventMaintainer.teams[self.eventMaintainer.ranks[str(i+1)]]
            tempPanel = TeamPanel(self.ranksPanel,-1,self.eventMaintainer.teams[self.eventMaintainer.ranks[str(i+1)]],pos=(XOffset,YOffset),size=(1300,self.rankHeight))
            if isGray:
                tempPanel.SetBackgroundColour(Colors["vexBGLightGray"])
            self.RankPanels[i] = tempPanel
            YOffset += self.rankHeight
            isGray = not isGray            
        tempPanel = None
        if len(self.eventMaintainer.localSponsors) > 0:
            self.eventMaintainer.localSponsorIndex = 0
            tempPanel = TeamPanel(self.ranksPanel,-1,None,pos=(XOffset,YOffset),size=(1300,300),fileStr = self.eventMaintainer.localSponsors[self.eventMaintainer.localSponsorIndex])
        else:
            self.eventMaintainer.localSponsors = glob.glob(os.path.join("Images","Display","Logos","Medium","*.png"))
            self.eventMaintainer.localSponsorIndex = 0
            tempPanel = TeamPanel(self.ranksPanel,-1,None,pos=(XOffset,YOffset),size=(1300,300),fileStr = self.eventMaintainer.localSponsors[self.eventMaintainer.localSponsorIndex])
        self.RankPanels[len(self.RankPanels)] = tempPanel
        if len(self.eventMaintainer.teams) > 28:
            self.deltaY = -2
            self.callInterval = 26
            self.logoCheck = 858#850
    def UpdateSchedulesData(self,interval=10000):
        self.eventMaintainer.getMatches()
        for panel in self.SchedulePanels:
            if panel in self.eventMaintainer.showMatches:
                self.SchedulePanels[panel].updateMatch(self.eventMaintainer.matches[self.eventMaintainer.showMatches[panel]])
                self.SchedulePanels[panel].Show()
            else:
                self.SchedulePanels[panel].Hide()
            
        wx.CallLater(interval,self.UpdateSchedulesData,interval=interval)
    def SetupSchedulePanels(self):
        XOffset = 0
        YOffset = 0
        isGray = True
        self.eventMaintainer.getMatches()
        if len(self.eventMaintainer.matches) > 0:
            if len(self.SchedulePanels) != len(self.eventMaintainer.showMatches):
                self.SchedulePanels = {}
                for i in range(0,len(self.eventMaintainer.showMatches)):
                    self.SchedulePanels[i] = None
            for match in self.eventMaintainer.showMatches:
                tempPanel = MatchPanel(self.schedulePanel,-1,self.eventMaintainer.matches[self.eventMaintainer.showMatches[match]],pos=(XOffset,YOffset),size=(550,99))
                if isGray:
                    tempPanel.SetBackgroundColour(Colors["vexBGLightGray"])
                    isGray = False
                else:
                    isGray = True
                self.SchedulePanels[match] = tempPanel
                YOffset += 99
            self.UpdateSchedulesData()
        else:
            wx.CallLater(10000,self.SetupSchedulePanels)   

        
            
        
    def StartEvent(self):
        self.eventMaintainer.start()
        self.SetupRankPanels()
        self.SetupSchedulePanels()
        
        
        
        wx.CallLater(self.callInterval,self.UpdateRankPositions)
    def UpdateGlobalLogo(self):
        self.GlobalSponsorPanel.bitmap = wx.Bitmap(self.GlobalSponsors[self.GlobalSponsorIndex],type=wx.BITMAP_TYPE_PNG)
        self.GlobalSponsorPanel.static.SetBitmap(self.GlobalSponsorPanel.bitmap)
        x = (self.GlobalSponsorPanel.GetSize()[0]-self.GlobalSponsorPanel.bitmap.GetSize()[0])/2
        y = (self.GlobalSponsorPanel.GetSize()[1]-self.GlobalSponsorPanel.bitmap.GetSize()[1])/2
        self.GlobalSponsorPanel.static.SetSize(self.GlobalSponsorPanel.bitmap.GetSize())
        self.GlobalSponsorPanel.static.SetPosition((x,y))
        self.GlobalSponsorPanel.Refresh()
        if self.GlobalSponsorIndex == len(self.GlobalSponsors)-1:
            self.GlobalSponsorIndex = 0
        else:
            self.GlobalSponsorIndex += 1
    def UpdateRankData(self):
        self.eventMaintainer.getEventName()
        self.eventMaintainer.getTeams()
        self.eventMaintainer.getRankings()

        for panel in range(0,len(self.RankPanels)):
            if self.RankPanels[panel].fileStr == None:
                self.RankPanels[panel].teamNum.SetLabel(self.eventMaintainer.teams[self.eventMaintainer.ranks[(str(panel+1))]].number)
                self.RankPanels[panel].teamName.SetLabel(self.eventMaintainer.teams[self.eventMaintainer.ranks[(str(panel+1))]].name)
                self.RankPanels[panel].teamWP.SetLabel(self.eventMaintainer.teams[self.eventMaintainer.ranks[(str(panel+1))]].wps)
                self.RankPanels[panel].teamAP.SetLabel(self.eventMaintainer.teams[self.eventMaintainer.ranks[(str(panel+1))]].aps)
                self.RankPanels[panel].teamSP.SetLabel(self.eventMaintainer.teams[self.eventMaintainer.ranks[(str(panel+1))]].sps)
                self.RankPanels[panel].teamWs.SetLabel(self.eventMaintainer.teams[self.eventMaintainer.ranks[(str(panel+1))]].wins)
                self.RankPanels[panel].teamLs.SetLabel(self.eventMaintainer.teams[self.eventMaintainer.ranks[(str(panel+1))]].losses)
                self.RankPanels[panel].teamTs.SetLabel(self.eventMaintainer.teams[self.eventMaintainer.ranks[(str(panel+1))]].ties)

                x = self.RankPanels[panel].teamWs.GetPosition()[0] + self.RankPanels[panel].teamWs.GetSize()[0]
                self.RankPanels[panel].teamWD.SetPosition((x,self.RankPanels[panel].teamWD.GetPosition()[1]))

                x = self.RankPanels[panel].teamLs.GetPosition()[0] + self.RankPanels[panel].teamLs.GetSize()[0]
                self.RankPanels[panel].teamLD.SetPosition((x,self.RankPanels[panel].teamLD.GetPosition()[1]))


                x = 850+100
                x = x-(100+(self.RankPanels[panel].teamWP.GetSize()[0])/2)
                self.RankPanels[panel].teamWP.SetPosition((x,18))
                
                x = 950+100
                x = x-(100+(self.RankPanels[panel].teamAP.GetSize()[0])/2)
                self.RankPanels[panel].teamAP.SetPosition((x,18))

                x = 1050+100
                x = x-(100+(self.RankPanels[panel].teamSP.GetSize()[0])/2)
                self.RankPanels[panel].teamSP.SetPosition((x,18))

                
                self.RankPanels[panel].Layout()

    def UpdateRankPositions(self):
        for panel in range(0,len(self.RankPanels)):
            if self.RankPanels[panel].GetPosition()[1] < (-1*self.RankPanels[panel].GetSize()[1]):#Checks to see if panel is off screen
                    newY = panel*self.rankHeight + self.RankPanels[len(self.RankPanels)-1].GetPosition()[1] + self.RankPanels[len(self.RankPanels)-1].GetSize()[1]+self.deltaY#if it is reset the y
                    self.RankPanels[panel].SetPosition((self.RankPanels[panel].GetPosition()[0],newY))
##                    ######THIS STRIP HAS LEFT THE SCREEN - UPDATE THE TEXT#########
                    #MAKE SURE WE AREN'T CHANGING THE LOGO
                    if self.RankPanels[panel].fileStr == None:
                        self.RankPanels[panel].teamNum.SetLabel(self.eventMaintainer.teams[self.eventMaintainer.ranks[(str(panel+1))]].number)
                        self.RankPanels[panel].teamName.SetLabel(self.eventMaintainer.teams[self.eventMaintainer.ranks[(str(panel+1))]].name)
                        self.RankPanels[panel].teamWP.SetLabel(self.eventMaintainer.teams[self.eventMaintainer.ranks[(str(panel+1))]].wps)
                        self.RankPanels[panel].teamAP.SetLabel(self.eventMaintainer.teams[self.eventMaintainer.ranks[(str(panel+1))]].aps)
                        self.RankPanels[panel].teamSP.SetLabel(self.eventMaintainer.teams[self.eventMaintainer.ranks[(str(panel+1))]].sps)
                        self.RankPanels[panel].teamWs.SetLabel(self.eventMaintainer.teams[self.eventMaintainer.ranks[(str(panel+1))]].wins)
                        self.RankPanels[panel].teamLs.SetLabel(self.eventMaintainer.teams[self.eventMaintainer.ranks[(str(panel+1))]].losses)
                        self.RankPanels[panel].teamTs.SetLabel(self.eventMaintainer.teams[self.eventMaintainer.ranks[(str(panel+1))]].ties)

                        x = self.RankPanels[panel].teamWs.GetPosition()[0] + self.RankPanels[panel].teamWs.GetSize()[0]
                        self.RankPanels[panel].teamWD.SetPosition((x,self.RankPanels[panel].teamWD.GetPosition()[1]))

                        x = self.RankPanels[panel].teamLs.GetPosition()[0] + self.RankPanels[panel].teamLs.GetSize()[0]
                        self.RankPanels[panel].teamLD.SetPosition((x,self.RankPanels[panel].teamLD.GetPosition()[1]))

                        
                        self.RankPanels[panel].Layout()
                    ##elif self.RankPanels[panel].fileStr != None: 
                    if self.RankPanels[panel].fileStr != None:
                        self.RankPanels[panel].fileStr = self.eventMaintainer.localSponsors[self.eventMaintainer.localSponsorIndex]
                        self.RankPanels[panel].bitmap = wx.Bitmap(self.eventMaintainer.localSponsors[self.eventMaintainer.localSponsorIndex],type=wx.BITMAP_TYPE_PNG)
                        self.RankPanels[panel].static.SetBitmap(self.RankPanels[panel].bitmap)
                        x = (self.RankPanels[panel].GetSize()[0]-self.RankPanels[panel].static.GetSize()[0])/2
                        y = (self.RankPanels[panel].GetSize()[1]-self.RankPanels[panel].static.GetSize()[1])/2
                        self.RankPanels[panel].static.SetPosition((x,y))
                        self.RankPanels[panel].Layout()
                        if self.eventMaintainer.localSponsorIndex == (len(self.eventMaintainer.localSponsors)-1):
                            self.eventMaintainer.localSponsorIndex = 0
                        else:
                            self.eventMaintainer.localSponsorIndex += 1
                        self.UpdateGlobalLogo()
            else:
                self.RankPanels[panel].SetPosition((self.RankPanels[panel].GetPosition()[0],self.RankPanels[panel].GetPosition()[1]+self.deltaY))
        if self.RankPanels[len(self.RankPanels)-1].GetPosition()[1] == self.logoCheck:
             self.UpdateRankData()
        
        
        wx.CallLater(self.callInterval,self.UpdateRankPositions)

    def OnPaint(self,evt):
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.RightBannerImg,self.GetSize()[0]-self.RightBannerImg.GetSize()[0],self.GetSize()[1]-self.RightBannerImg.GetSize()[1],True)
        dc.DrawBitmap(self.LeftBannerImg,0,self.GetSize()[1]-self.LeftBannerImg.GetSize()[1],True)
        dc.DrawBitmap(self.MatchLogoImg,self.GetSize()[0]-self.MatchLogoImg.GetSize()[0]-25,25,True)
        dc.SetPen(wx.Pen(Colors["White"]))

        dc.DrawRoundedRectangle(-25,25,225,112,14)



class VEXDisplay(wx.Frame):

    def __init__(self,parent,id,title,w=1920,h=1080,style=(wx.STAY_ON_TOP),fullscreen=False,configFile="config.ini"):

        self.DEBUGGER = Debugger()
        self.CONFIG = Config(configFile)

        self.isFullScreen = fullscreen

        wx.Frame.__init__(self,parent,id,title, size=(w,h),style=style)
        self.locale = wx.Locale(wx.LANGUAGE_ENGLISH)
        
        self.Bind(wx.EVT_CHAR_HOOK,self.OnKey)
        self.SetCursor(wx.StockCursor(wx.CURSOR_BLANK))
        self.SetBackgroundColour(Colors["White"])

        
        self.EventPanel = Event(self,-1,size=(1920,1080))

        
        
        serverUp = False
        exitPr = False
        while serverUp == False:
            IPBox = wx.TextEntryDialog(None,"Server IP Address","Configure Display",self.CONFIG.serverURL)
            
            if IPBox.ShowModal()==wx.ID_OK:
                serverUp = self.CONFIG.TestServer(IPBox.GetValue())
            else:
                exitPr = True
                serverUp = True
        if exitPr:
            self.Quit()

        self.EventPanel.SetEvent(self.CONFIG.serverURL,True,self.CONFIG.sponsorDir)
        
        wx.CallLater(30,self.UpdatePositions)
    def ShowApp(self):
        if self.isFullScreen:
            self.ShowFullScreen(self.isFullScreen)
        else:
            self.Show()
            
    def Quit(self):
        self.Destroy()
        sys.exit()

    def UpdatePositions(self):
        wx.CallLater(30,self.UpdatePositions)
    def OnPaint(self,event):
        dc = wx.PaintDC(self.panel)
    def OnKey(self,event):
        KEY = event.GetKeyCode()
        self.DEBUGGER.log(str(KEY))
        if KEY == 27:
            self.Destroy()
            sys.exit()
def main():
    app = wx.App(False)
    frame = VEXDisplay(parent=None,id=-1,fullscreen=True,title="Test",style=(wx.NO_BORDER))#style=(wx.STAY_ON_TOP | wx.NO_BORDER)
    frame.ShowApp()
    app.MainLoop()

if __name__ == '__main__':
    main()
