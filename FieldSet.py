class FieldSet(object):
    def __init__(self,name):
        self.fieldName = name
        self.matchList = []
        self.completedMatches = []
        self.nextMatch = None
        self.lastMatch = None
        
    
