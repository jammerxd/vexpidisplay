import wx
global btn
def updater():
    p = btn.GetPosition()
    btn.SetPosition((p[0] ,p[1] - 2))
    wx.CallLater(30,updater)
a= wx.App(redirect=False)

f = wx.Frame(None,-1,"Animation",size=(400,600))
p = wx.Panel(f,-1)
btn = wx.Button(p,-1,"Click Me",pos=(175,520))
f.Show()
wx.CallLater(30,updater) #could have used a normal timer just as easy ... maybe even easier
a.MainLoop()
