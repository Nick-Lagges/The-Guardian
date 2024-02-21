'''
Nick Lagges

scrolling background from: 
'''

import pygame
import math

from . import Drawable, Hero, Laser, Alien

from utils import vec, RESOLUTION, SCALE, TimerStatic 

class GameEngine(object):
    import pygame

    def __init__(self):

        pygame.font.init()

        #initializes hero and scrolling background
        self.hero = Hero.getInstance()
        self.size = vec(*RESOLUTION)
        self.background = Drawable((0,0), "background.png")
        self.bgWidth = self.background.getSize()[0]
        self.tiles = math.ceil( RESOLUTION[0] / self.bgWidth ) + 1
        self.scroll = 0

        #score / currency system
        self.score = 0
        self.font = pygame.font.SysFont("magneto", 20)

        #First wave of aliens
        #   * 10 health
        self.waveOne = [Alien((400,100), 10), Alien((500,300), 10), Alien((330,200), 10), Alien((400, 300), 10)]
        self.waveOneTimer = TimerStatic(10)
        self.spawnAliens = False

        pygame.mouse.set_visible(False)
    
    def draw(self, drawSurface):
        for t in range(0, self.tiles):
            self.background = Drawable((t * self.bgWidth + self.scroll, 0), "background.png")
            self.background.draw(drawSurface)
        self.scroll -=3

        if abs(self.scroll) > self.bgWidth:
            self.scroll = 0
        
        self.hero.draw(drawSurface)
        for i in range(0, len(self.hero.lasers)):
            self.hero.lasers[i].draw(drawSurface)

        if self.spawnAliens:
            for a in range(len(self.waveOne)):
                self.waveOne[a].draw(drawSurface)

        #Scoring
        x,y = list(map(int, RESOLUTION))
        x *= 0.8
        y *= 0.02
        scoreBoard = "$: " + str(self.score)
        message = self.font.render(scoreBoard, True, (255,255,255))
        drawSurface.blit(message, (x,y))

        mousePos = vec(*pygame.mouse.get_pos()) // SCALE - vec(16,16)
        self.cursor = Drawable(mousePos, "reticle.png")
        self.cursor.draw(drawSurface)
            
    def handleEvent(self, event):
        self.hero.handleEvent(event)
    
    def update(self, seconds):
        self.waveOneTimer.update(seconds)
        if self.waveOneTimer.done():
            self.spawnAliens = True
            for x in range(len(self.waveOne)):
                self.waveOne[x].update(seconds)
        self.hero.update(seconds)
        #collision detection for hero lasers with aliens
        #removes laser after collision
        for i in range(0, len(self.hero.lasers)):
            self.hero.lasers[i].update(seconds)
            remove = False
            for a in range(len(self.waveOne)):
                if self.hero.lasers[i].position[0] < self.waveOne[a].position[0] + self.waveOne[a].getSize()[0] and \
                   self.hero.lasers[i].position[0] + self.hero.lasers[i].getSize()[0] > self.waveOne[a].position[0] and \
                   self.hero.lasers[i].position[1] < self.waveOne[a].position[1] + self.waveOne[a].getSize()[1] and \
                   self.hero.lasers[i].position[1] + self.hero.lasers[i].getSize()[1] > self.waveOne[a].position[1]:
                    self.waveOne[a].health -= self.hero.lasers[i].damage
                    remove = True
                    if not self.waveOne[a].alive():
                        self.waveOne.pop(a)
                        self.score += 10
                        break
            if remove:
                self.hero.lasers.pop(i)
                #print(i, len(self.hero.lasers))
                break
            
        Drawable.updateOffset(self.hero, self.size)
    

