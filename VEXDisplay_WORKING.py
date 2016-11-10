import wx, os
from Config import *
from Debugger import *
from Colors import *
from Updater import *
class Header(wx.StaticText):
    def __init__(self,parent,id,text,font,color,pos=(200,12)):
        wx.StaticText.__init__(self,parent,id,text,pos=pos)
        self.SetFont(font)
        self.SetForegroundColour(color)
class TeamPanel(wx.Panel):
    def __init__(self,parent,id,team=None,size=(0,0),pos=(0,0),bg=Colors["White"],fileStr = None):
        wx.Panel.__init__(self,parent,id,pos=pos,size=size)
        self.SetBackgroundColour(bg)
        self.fileStr = fileStr
        if team != None:
            self.Rank = Header(self,id,team.rank,wx.Font(60,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="NotoSans"),Colors["vexTxtGray"])
            self.Rank.SetPosition((75-(self.Rank.GetSize()[0]/2),-15))

            self.teamNum = Header(self,id,team.number,wx.Font(28,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="NotoSans"),Colors["vexTxtGray"])
            self.teamNum.SetPosition((175,0))

            self.teamName = Header(self,id,team.name,wx.Font(24,wx.DEFAULT,wx.NORMAL,wx.NORMAL,faceName="NotoSans"),Colors["vexTxtGrayLighter"])
            self.teamName.SetPosition((175,43))

            self.teamWP = Header(self,id,team.wps,wx.Font(28,wx.DEFAULT,wx.NORMAL,wx.NORMAL,faceName="NotoSans"),Colors["vexTxtGrayLighter"])
            x = 850
            x = x-(self.teamWP.GetSize()[0])/2
            self.teamWP.SetPosition((x,18))

            self.teamAP = Header(self,id,team.aps,wx.Font(28,wx.DEFAULT,wx.NORMAL,wx.NORMAL,faceName="NotoSans"),Colors["vexTxtGrayLighter"])
            x = 950
            x = x-(self.teamAP.GetSize()[0])/2
            self.teamAP.SetPosition((x,18))

            self.teamSP = Header(self,id,team.sps,wx.Font(28,wx.DEFAULT,wx.NORMAL,wx.NORMAL,faceName="NotoSans"),Colors["vexTxtGrayLighter"])
            x = 1050
            x = x-(self.teamSP.GetSize()[0])/2
            self.teamSP.SetPosition((x,18))

            self.teamWs = Header(self,id,team.wins,wx.Font(28,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="NotoSans"),Colors["vexTxtGray"])
            x = 1160
            x = x-(self.teamWs.GetSize()[0])/2
            self.teamWs.SetPosition((x,18))

            self.teamWD = Header(self,id,"-",wx.Font(28,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="NotoSans"),Colors["vexTxtGray"])
            x = self.teamWs.GetPosition()[0]+self.teamWs.GetSize()[0]
            self.teamWD.SetPosition((x,14))

            self.teamLs = Header(self,id,team.losses,wx.Font(28,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="NotoSans"),Colors["vexTxtGray"])
            x = self.teamWD.GetPosition()[0]+self.teamWD.GetSize()[0]
            self.teamLs.SetPosition((x,18))

            self.teamLD = Header(self,id,"-",wx.Font(28,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="NotoSans"),Colors["vexTxtGray"])
            x = self.teamLs.GetPosition()[0]+self.teamLs.GetSize()[0]
            self.teamLD.SetPosition((x,14))

            self.teamTs = Header(self,id,team.ties,wx.Font(28,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="NotoSans"),Colors["vexTxtGray"])
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
        self.schedulePanel = wx.Panel(self,-1,pos=(1345,235),size=(550,830))
        

        self.SetBackgroundColour(Colors["vexRed"])
        self.ranksPanel.SetBackgroundColour(Colors["Black"])
        self.schedulePanel.SetBackgroundColour(Colors["White"])
        self.RightBannerImg = wx.Bitmap(os.path.join("Images","Display","2016","gear_pattern_right_16x9.png"),type = wx.BITMAP_TYPE_PNG)
        self.LeftBannerImg = wx.Bitmap(os.path.join("Images","Display","2016","gear_pattern_left_16x9.png"),type = wx.BITMAP_TYPE_PNG)
        self.MatchLogoImg = wx.Bitmap(os.path.join("Images","Display","2016","vrc_logo_match_titlebar.png"),type= wx.BITMAP_TYPE_PNG)

        self.Header = Header(self,-1,"Qualification Rankings",wx.Font(60,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="NotoSans"),Colors["White"],(215,20))

        self.ResetPositions = False

        self.GlobalSponsors = glob.glob(os.path.join("Images","Display","Logos","Small","*.png"))
        self.GlobalSponsorIndex = 0
        self.GlobalSponsorPanel = TeamPanel(self,-1,None,size=(190,112),pos=(0,25),bg=Colors["White"],fileStr=self.GlobalSponsors[self.GlobalSponsorIndex])
        
    def SetEvent(self,serverURL,startEvent = False,sponsorDir=False):
        self.eventMaintainer = UpdateInfo(serverURL,sponsorDir)
        if startEvent:
            self.StartEvent()

    def StartEvent(self):
        self.eventMaintainer.start()
        YOffset = 0
        XOffset = 0
        self.ranksPanelHieght = 86*len(self.eventMaintainer.teams)
        isGray = False
        i = 0
        for i in range(0,len(self.eventMaintainer.ranks)):
            tempTeam = self.eventMaintainer.teams[self.eventMaintainer.ranks[str(i+1)]]
            tempPanel = TeamPanel(self.ranksPanel,-1,self.eventMaintainer.teams[self.eventMaintainer.ranks[str(i+1)]],pos=(XOffset,YOffset),size=(1300,86))
            if isGray:
                tempPanel.SetBackgroundColour(Colors["vexBGLightGray"])
            self.RankPanels[i] = tempPanel
            YOffset += 86
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
        wx.CallLater(30,self.UpdateRankPositions)
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


    def UpdateRankPositions(self):
        for panel in range(0,len(self.RankPanels)):
            if self.RankPanels[panel].GetPosition()[1] < (-1*self.RankPanels[panel].GetSize()[1]):#Checks to see if panel is off screen
                    newY = panel*86 + self.RankPanels[len(self.RankPanels)-1].GetPosition()[1] + self.RankPanels[len(self.RankPanels)-1].GetSize()[1]#if it is reset the y
                    self.RankPanels[panel].SetPosition((self.RankPanels[panel].GetPosition()[0],newY))
                    ######THIS STRIP HAS LEFT THE SCREEN - UPDATE THE TEXT#########
                    #MAKE SURE WE AREN'T CHANGING THE LOGO
                    if self.RankPanels[panel].fileStr == None:
                        self.RankPanels[panel].teamNum.SetLabel(self.eventMaintainer.teams[self.eventMaintainer.ranks[(str(panel+1))]].number)
                        self.RankPanels[panel].teamName.SetLabel(self.eventMaintainer.teams[self.eventMaintainer.ranks[(str(panel+1))]].name)
                        self.RankPanels[panel].teamWP.SetLabel(self.eventMaintainer.teams[self.eventMaintainer.ranks[(str(panel+1))]].wps)

                        self.RankPanels[panel].teamWs.SetLabel(self.eventMaintainer.teams[self.eventMaintainer.ranks[(str(panel+1))]].wins)
                        self.RankPanels[panel].teamLs.SetLabel(self.eventMaintainer.teams[self.eventMaintainer.ranks[(str(panel+1))]].losses)
                        self.RankPanels[panel].teamTs.SetLabel(self.eventMaintainer.teams[self.eventMaintainer.ranks[(str(panel+1))]].ties)

                        x = self.RankPanels[panel].teamWs.GetPosition()[0] + self.RankPanels[panel].teamWs.GetSize()[0]
                        self.RankPanels[panel].teamWD.SetPosition((x,self.RankPanels[panel].teamWD.GetPosition()[1]))

                        x = self.RankPanels[panel].teamLs.GetPosition()[0] + self.RankPanels[panel].teamLs.GetSize()[0]
                        self.RankPanels[panel].teamLD.SetPosition((x,self.RankPanels[panel].teamLD.GetPosition()[1]))

                        
                        self.RankPanels[panel].Layout()
                    elif self.RankPanels[panel].fileStr != None:
                        self.RankPanels[panel].fileStr = self.eventMaintainer.localSponsors[self.eventMaintainer.localSponsorIndex]
                        self.RankPanels[panel].bitmap = wx.Bitmap(self.eventMaintainer.localSponsors[self.eventMaintainer.localSponsorIndex],type=wx.BITMAP_TYPE_PNG)
                        self.RankPanels[panel].static.SetBitmap(self.RankPanels[panel].bitmap)
                        x = (self.RankPanels[panel].GetSize()[0]-self.RankPanels[panel].static.GetSize()[0])/2
                        y = (self.RankPanels[panel].GetSize()[1]-self.RankPanels[panel].static.GetSize()[1])/2
                        #newY = panel*86 + self.RankPanels[len(self.RankPanels)-1].GetPosition()[1] + self.RankPanels[len(self.RankPanels)-1].GetSize()[1]
                        self.RankPanels[panel].static.SetPosition((x,y))
                        self.RankPanels[panel].Layout()
                        if self.eventMaintainer.localSponsorIndex == (len(self.eventMaintainer.localSponsors)-1):
                            self.eventMaintainer.localSponsorIndex = 0
                        else:
                            self.eventMaintainer.localSponsorIndex += 1
                        self.UpdateGlobalLogo()
            else:
                self.RankPanels[panel].SetPosition((self.RankPanels[panel].GetPosition()[0],self.RankPanels[panel].GetPosition()[1]-2))
        if self.RankPanels[len(self.RankPanels)-1].GetPosition()[1] == 850:#1066 represents the y-coordinate at which the panel will be visible
            self.UpdateRankData()
        
        wx.CallLater(30,self.UpdateRankPositions)

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
        self.SetCursor(wx.StockCursor(wx.CURSOR_BLANK))
        self.SetBackgroundColour(Colors["White"])
        self.EventPanel = Event(self,-1,size=(1920,1080))

        
        serverUp = False

        while serverUp == False:
            IPBox = wx.TextEntryDialog(None,"Server IP Address","Configure Display",self.CONFIG.serverURL)
            
            if IPBox.ShowModal()==wx.ID_OK:
                serverUp = self.CONFIG.TestServer(IPBox.GetValue())
            else:
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
        quit(0)

    def UpdatePositions(self):
        wx.CallLater(30,self.UpdatePositions)
    def OnPaint(self,event):
        dc = wx.PaintDC(self.panel)

def main():
    app = wx.App(False)
    frame = VEXDisplay(parent=None,id=-1,fullscreen=True,title="Test",style=(wx.STAY_ON_TOP | wx.NO_BORDER))
    frame.ShowApp()
    app.MainLoop()

if __name__ == '__main__':
    main()
