class Enemy(Animated):
    def __init__(self, x, y, w, h, path, screen, frames, type):
        #super(x, y, w, h, path, screen, frames) #call animated constructor
        #"type" should be a string which matches up to a dictionary somewhere with details about monsters.
        self.type = type
        #self.maxSpeed = monsterDict[type].maxSpeed
        #self.ai = monsterDict[type].ai
