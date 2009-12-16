class Interactable(Entity):
    def __init__(self, x, y, w, h, path, screen, actions, relevantObjects):
        #super(x, y, w, h, path, screen) #call Entity constructor
       
        #concept : actions will be an array of commands ["open", "close", "turn on"], and relevantObjects will be the objects that you open, close, etc.

        #feel free to come up with another way of how to do it (maybe an array of tuples)?


        pass

    def doAction(self):
        #this should just read through actions/relevantObjects to determine what to do.
        pass
