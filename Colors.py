class Color:
    def __init__(self,name,r,g,b):
        self.r = r
        self.g = g
        self.b = b
        self.name = name
    def Get(self):
        return (self.r,self.g,self.b)
Colors={}
Colors["White"] = (255,255,255)
Colors["Black"] = (0,0,0)
Colors["Red"] = (255,0,0)
Colors["Green"] = (0,255,0)
Colors["Blue"] = (0,0,255)

Colors["vexRed"] = (218,38,46)
Colors["vexBlue"] = (2,119,190)
Colors["vexTxtGray"] = (110,112,114)
Colors["vexTxtGrayLighter"] = (130,132,134)
Colors["vexBGLightGray"] = (215,217,219)
