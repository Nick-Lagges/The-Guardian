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
        self.background = Drawable((0,0), "background.png", parallax=1)
        self.bgWidth = self.background.getSize()[0]
        self.tiles = math.ceil( RESOLUTION[0] / self.bgWidth ) + 1
        self.scroll = 0

        #score / currency system
        self.font = pygame.font.SysFont("default8", 25)

        #First wave of aliens
        #20 health, 15 damage
        self.waveOne = []
        spawnYAlien1 = 50
        for wave1 in range(0, 5):
            x,y = (500, spawnYAlien1)
            #print(x,y)
            self.waveOne.append(Alien((x,y), 20, 15))
            spawnYAlien1 += 50
        self.waveOneTimer = TimerStatic(5)
        self.spawnAliens1 = False

        #Second wave of aliens
        #40 health, 25 damage
        self.waveTwo = []
        spawnXAlien2 = 480
        spawnYAlien2 = 50
        for wave2 in range(0, 9):
            x,y = (spawnXAlien2, spawnYAlien2)
            #print(x,y)
            self.waveTwo.append(Alien((x,y), 40, 25))
            spawnYAlien2 += 30
            if wave2 == 3:
                spawnXAlien2 += 70
                spawnYAlien2 = 50
        self.waveTwoTimer = TimerStatic(5)
        self.spawnAliens2 = False

        #Third wave of aliens
        #100 health, 45 damage
        self.waveThree = []
        spawnXAlien3 = 480
        spawnYAlien3 = 50
        for wave3 in range(0, 9):
            x,y = (spawnXAlien3, spawnYAlien3)
            #print(x,y)
            self.waveThree.append(Alien((x,y), 100, 45))
            spawnYAlien3 += 30
            if wave3 == 3:
                spawnXAlien3 += 70
                spawnYAlien3 = 50
        self.waveThreeTimer = TimerStatic(7)
        self.spawnAliens3 = False

        pygame.mouse.set_visible(False)
    
    def draw(self, drawSurface):
        for t in range(0, self.tiles):
            self.background = Drawable((t * self.bgWidth + self.scroll, 0), "background.png", parallax=1)
            self.background.draw(drawSurface)
        self.scroll -=2

        if abs(self.scroll) > self.bgWidth:
            self.scroll = 0
        
        self.hero.draw(drawSurface)
        if self.spawnAliens1:
            for i in range(0, len(self.hero.lasers)):
                self.hero.lasers[i].draw(drawSurface)

        if self.spawnAliens1:
            self.drawAliens(self.waveOne, drawSurface)

        if self.spawnAliens2:
            self.drawAliens(self.waveTwo, drawSurface)

        if self.spawnAliens3:
            self.drawAliens(self.waveThree, drawSurface)

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
            self.spawnAliens1 = True
            self.alienCollisionUpdate(self.waveOne, seconds)
            self.heroLaserCollisionUpdate(self.waveOne, seconds)
            if len(self.waveOne) == 0:
                self.waveTwoTimer.update(seconds)

        if self.waveTwoTimer.done():
            self.spawnAliens2 = True
            self.alienCollisionUpdate(self.waveTwo, seconds)
            self.heroLaserCollisionUpdate(self.waveTwo, seconds)
            if len(self.waveTwo) == 0:
                self.waveThreeTimer.update(seconds)

        if self.waveThreeTimer.done():
            self.spawnAliens3 = True
            self.alienCollisionUpdate(self.waveThree, seconds)
            self.heroLaserCollisionUpdate(self.waveThree, seconds)
        
        self.hero.update(seconds)

    def alienCollisionUpdate(self, wave, seconds):
        for x in range(len(wave)):
            wave[x].update(seconds)
            for laser in range(len(wave[x].lasers)):
                wave[x].lasers[laser].update(seconds)
                removeALaser = False
                if wave[x].lasers[laser].position[0] < self.hero.position[0] + wave[x].getSize()[0] and \
                   wave[x].lasers[laser].position[0] + wave[x].lasers[laser].getSize()[0] > self.hero.position[0] and \
                   wave[x].lasers[laser].position[1] < self.hero.position[1] + self.hero.getSize()[1] and \
                   wave[x].lasers[laser].position[1] + wave[x].lasers[laser].getSize()[1] > self.hero.position[1]:
                    self.hero.health -= wave[x].lasers[laser].damage
                    removeALaser = True
                    if not self.hero.alive():
                        self.hero.lives -= 1
                        self.hero.health = 100
                if removeALaser:
                    wave[x].lasers.pop(laser)
                    break
                if wave[x].lasers[laser].position[0] < 0:
                    wave[x].lasers.pop(laser)
                    break
                elif wave[x].lasers[laser].position[0] > RESOLUTION[0]:
                    wave[x].lasers.pop(laser)
                    break
                elif wave[x].lasers[laser].position[1] < 0:
                    wave[x].lasers.pop(laser)
                    break
                elif wave[x].lasers[laser].position[1] > RESOLUTION[1]:
                    wave[x].lasers.pop(laser)
                    break

    def heroLaserCollisionUpdate(self, wave, seconds):
        for i in range(0, len(self.hero.lasers)):
            self.hero.lasers[i].update(seconds)
            removeHLaser = False
            for a in range(len(wave)):
                if self.hero.lasers[i].position[0] < wave[a].position[0] + wave[a].getSize()[0] and \
                   self.hero.lasers[i].position[0] + self.hero.lasers[i].getSize()[0] > wave[a].position[0] and \
                   self.hero.lasers[i].position[1] < wave[a].position[1] + wave[a].getSize()[1] and \
                   self.hero.lasers[i].position[1] + self.hero.lasers[i].getSize()[1] > wave[a].position[1]:
                    wave[a].health -= self.hero.lasers[i].damage
                    removeHLaser = True
                    if not wave[a].alive():
                        wave.pop(a)
                        self.hero.score += 10
                        break
            #hero laser removal if off map
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

    def drawAliens(self, wave, drawSurface):
        for a in range(len(wave)):
            wave[a].draw(drawSurface)
            for laz in range(len(wave[a].lasers)):
                wave[a].lasers[laz].draw(drawSurface)

