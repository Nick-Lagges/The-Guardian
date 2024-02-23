'''
Nick Lagges

scrolling background from: 
'''

import pygame
import math
import random

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
        self.font = pygame.font.SysFont("default8", 25)

        #First wave of aliens
        #   * 10 health
        self.waveOne = []
        spawnYAlien = 50
        for wave1 in range(0, 5):
            x,y = (500, spawnYAlien)
            #print(x,y)
            self.waveOne.append(Alien((x,y), 20, 15))
            spawnYAlien += 50
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
                for laz in range(len(self.waveOne[a].lasers)):
                    self.waveOne[a].lasers[laz].draw(drawSurface)

        #Scoring
        xScore,yScore = list(map(int, RESOLUTION))
        xScore *= 0.9
        yScore *= 0.02
        scoreBoard = "$: " + str(self.hero.score)
        scoreMessage = self.font.render(scoreBoard, True, (255,255,255))
        drawSurface.blit(scoreMessage, (xScore,yScore))

        #Hero Health
        xHealth,yHealth = list(map(int, RESOLUTION))
        xHealth *= 0.01
        yHealth *= 0.02
        healthBar = "Health: " + str(self.hero.health)
        healthMessage = self.font.render(healthBar, True, (255,255,255))
        drawSurface.blit(healthMessage, (xHealth,yHealth))

        #Hero Lives
        xLives,yLives = list(map(int, RESOLUTION))
        xLives *= 0.3
        yLives *= 0.02
        lifeBar = "Lives: " + str(self.hero.lives)
        livesMessage = self.font.render(lifeBar, True, (255,255,255))
        drawSurface.blit(livesMessage, (xLives,yLives))
        
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
                for laser in range(len(self.waveOne[x].lasers)):
                    self.waveOne[x].lasers[laser].update(seconds)
                    removeALaser = False
                    if self.waveOne[x].lasers[laser].position[0] < self.hero.position[0] + self.waveOne[x].getSize()[0] and \
                       self.waveOne[x].lasers[laser].position[0] + self.waveOne[x].lasers[laser].getSize()[0] > self.hero.position[0] and \
                       self.waveOne[x].lasers[laser].position[1] < self.hero.position[1] + self.hero.getSize()[1] and \
                       self.waveOne[x].lasers[laser].position[1] + self.waveOne[x].lasers[laser].getSize()[1] > self.hero.position[1]:
                        self.hero.health -= self.waveOne[x].lasers[laser].damage
                        removeALaser = True
                        if not self.hero.alive():
                            self.hero.lives -= 1
                            self.hero.health = 100
                    if removeALaser:
                        self.waveOne[x].lasers.pop(laser)
                        break
                    if self.waveOne[x].lasers[laser].position[0] < 0:
                        self.waveOne[x].lasers.pop(laser)
                        break
                    elif self.waveOne[x].lasers[laser].position[0] > RESOLUTION[0]:
                        self.waveOne[x].lasers.pop(laser)
                        break
                    elif self.waveOne[x].lasers[laser].position[1] < 0:
                        self.waveOne[x].lasers.pop(laser)
                        break
                    elif self.waveOne[x].lasers[laser].position[1] > RESOLUTION[1]:
                        self.waveOne[x].lasers.pop(laser)
                        break
        self.hero.update(seconds)
        #collision detection for hero lasers with aliens
        #removes laser after collision
        for i in range(0, len(self.hero.lasers)):
            self.hero.lasers[i].update(seconds)
            removeHLaser = False
            for a in range(len(self.waveOne)):
                if self.hero.lasers[i].position[0] < self.waveOne[a].position[0] + self.waveOne[a].getSize()[0] and \
                   self.hero.lasers[i].position[0] + self.hero.lasers[i].getSize()[0] > self.waveOne[a].position[0] and \
                   self.hero.lasers[i].position[1] < self.waveOne[a].position[1] + self.waveOne[a].getSize()[1] and \
                   self.hero.lasers[i].position[1] + self.hero.lasers[i].getSize()[1] > self.waveOne[a].position[1]:
                    self.waveOne[a].health -= self.hero.lasers[i].damage
                    removeHLaser = True
                    if not self.waveOne[a].alive():
                        self.waveOne.pop(a)
                        self.hero.score += 10
                        break
            if removeHLaser:
                self.hero.lasers.pop(i)
                break
            if self.hero.lasers[i].position[0] < 0:
                self.hero.lasers.pop(i)
                break
            elif self.hero.lasers[i].position[0] > RESOLUTION[0]:
                self.hero.lasers.pop(i)
                break
            elif self.hero.lasers[i].position[1] < 0:
                self.hero.lasers.pop(i)
                break
            elif self.hero.lasers[i].position[1] > RESOLUTION[1]:
                self.hero.lasers.pop(i)
                break

