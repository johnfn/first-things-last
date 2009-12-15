import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
walls = [1, 3]


colors = {}
colors[0] = (255,0,0)
colors[1] = (255,255,0)
colors[2] = (0,0,200)
colors[3] = (0,200,0)



class FileReader:
    def __init__(self, filename):
        self.f_object = open(filename)

    def get(self):
        return self.f_object.readlines()

class Text:
    def __init__(self, words, x, y, surf, font="Sans"):
        self.font = font
        self.x=x
        self.y=y
        f = pygame.font.SysFont(font,15)
        self.text = f.render(words , True, (255,255, 255), (0, 0, 0))
        self.t_rect = self.text.get_rect()
        self.t_rect.x = x
        self.t_rect.y = y

    def set_text(self, words):
        """Change what the text object says"""
        f = pygame.font.SysFont(self.font,15)
        self.text = f.render(words , True, (255,255, 255), (0, 0, 0))
        self.t_rect = self.text.get_rect()
        self.t_rect.x = self.x
        self.t_rect.y = self.y

    def draw(self, surf):
        surf.blit(self.text, self.t_rect)

class MyTile:
    def __init__(self, clr):
        self.clr = clr
        self.gfx = pygame.Surface([15, 15])
        self.rect = self.gfx.get_rect()
        self.gfx.fill((255, 0,0))
        self.gfxMod = 0

    def setmap(self, _map):
        self.itsmap = _map

    def setpos(self, x, y):
        self.rect.x=x
        self.rect.y=y

    def draw(self, scrn):
        scrn.blit(self.gfx, self.rect)
        self.gfx.fill(colors[self.clr])

    def isWall(self):
        return self.clr in walls

    def getBordering(self, x, y):
        x = int(x)
        y = int(y)
        t1 = (self.itsmap.getTile((self.rect.x+x)/15, (self.rect.y+y)/15))
        t2 = (self.itsmap.getTile((self.rect.x+x+13)/15, (self.rect.y+y)/15))
        t3 = (self.itsmap.getTile((self.rect.x+x)/15, (self.rect.y+y+13)/15))
        t4 = (self.itsmap.getTile((self.rect.x+x+13)/15, (self.rect.y+y+13)/15))
        return [t1, t2, t3, t4]

    def setrelpos(self, x, y, col=False):
        #col means 'should we bother with collision while moving this tile'
        self.rect.x += x
        self.rect.y += y
        if col:
            tl = self.getBordering(x, y)
            for t in tl:
                if t != None:
                    if t.isWall():
                        self.rect.x -= x
                        self.rect.y -= y
                        return



class Character(MyTile):
    def __init__(self):
        MyTile.__init__(self, 2)
        MyTile.setpos(self, 20,20)

    def setrelpos(self, x, y, col=True):
        MyTile.setrelpos(self, x, y, col)

    def setabspos(self, x, y):
        MyTile.setpos(x, y)

    def outsidebounds(self):
        return self.getx()>135 or self.getx()<0 or self.gety()>135 or self.gety()<0

    def getx(self):
        return self.rect.x

    def gety(self):
        return self.rect.y

class Map:
    def __init__(self, filename):
        self.tiles = []
        fr = FileReader(filename)

        data = fr.get()
        for i in range(10):
            for j in range(10):
                self.tiles.append(MyTile(int(data[j][i])))
                self.tiles[-1].setpos(i*15, j*15)

        key_info = []
        for i, x in enumerate(data[10:]):
            key_info.append(x.replace("\n", ""))

        
        for x in key_info:
            if x == "":
                key_info.remove(x)


        self.adjMaps = []
        #self.adjMaps = dict([(x[0], x[1]) for x in [d.split("|",1) for d in key_info[1:key_info.index("Words")]]])

        print(self.adjMaps)

    def getmapat(self, key):
        if self.adjMaps.has_key(key) == False:
            print( "Map not found: "+ key)
            return None
        return self.adjMaps[key]


    def getTile(self, x, y):
        if x>=10 or y>=10 or x<0 or y <0:
            print( "Tile out of range.")
            return None
        x = int(x)
        y = int(y)
        return self.tiles[x*10+y]

    def draw(self, scrn):
        for m in self.tiles:
            m.draw(scrn)


class EventHandler:
    pass

class Game:
    def __init__(self, startmap):
        self.curmap = startmap
        self.play= True
        self.size = width, height = 320, 240
        self.screen = pygame.display.set_mode(self.size)
        self.drawers = []
        self.drawers.append(self.curmap)
        self.char = Character()
        self.char.setmap(self.curmap)
        self.drawers.append(self.char)
        self.te = Text("Hello Worldgame", 0, 150, self.screen)
        self.drawers.append(self.te)

    def gameloop(self):
        keys = {'up':False, 'down':False, 'left':False, 'right':False}
        states = [K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE]
        state_strings = ["up", "down", "left", "right", "space"]
        prev = 0
        while self.play:
            fps = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.play = False
                if event.type == KEYDOWN:
                    if event.key in states:
                        keys[state_strings[states.index(event.key)]]=True
                if event.type == KEYUP:
                    if event.key in states:
                        keys[state_strings[states.index(event.key)]]=False

            leavingdir = ""
	    
        
            dirs = {}
            dirs["up"] = (0,-1)
            dirs["down"] = (0,1)
            dirs["left"] = (-1,0)
            dirs["right"] = (1,0)

            dirkeys = []
            if keys["up"]: dirkeys.append("up")
            if keys["down"]: dirkeys.append("down")
            if keys["left"]: dirkeys.append("left")
            if keys["right"]: dirkeys.append("right")
    
            if self.char.outsidebounds() == False:
                for k in dirkeys:
                    self.char.setrelpos(*dirs[k])
                if keys["up"]:
                    if self.char.outsidebounds():
                       leavingdir = "up"
                if keys["down"]:
                    if self.char.outsidebounds():
                        leavingdir = "down"
                if keys["left"]:
                    if self.char.outsidebounds():
                        leavingdir = "left"
                if keys["right"]:
                    if self.char.outsidebounds():
                        leavingdir = "right"


            if self.char.outsidebounds():
                #set the new map
                self.drawers.remove(self.curmap)
                self.curmap = Map(self.curmap.getmapat(leavingdir))
                self.drawers.insert(0, self.curmap)
                self.char.itsmap = self.curmap
   
                self.char.setrelpos(*dirs[leavingdir], col=False)


            pygame.time.wait(1)
    
            self.te.set_text(str(fps-prev))
            prev = fps
            self.screen.fill((0,0,0))

            for x in self.drawers: x.draw(self.screen)
            pygame.display.flip()


firstmap = Map("levels\level1.txt")
main = Game(firstmap)

main.gameloop()
