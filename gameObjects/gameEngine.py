'''
Nick Lagges

scrolling background from: Code With Russ (YouTube)
'''

import pygame
import math
import random

from . import Drawable, Hero, Laser, Alien

from utils import vec, RESOLUTION, SCALE, TimerStatic, SoundManager

class GameEngine(object):
    import pygame

    def __init__(self):

        pygame.font.init()

        #initializes hero and scrolling background
        self.hero = Hero.getInstance()
        self.size = vec(*RESOLUTION)
                
        self.bg1 = Drawable(vec(0,0), "backgroundFar.png", parallax=0)
        self.bg2 = Drawable(vec(0,0), "backgroundMedium.png", parallax=0.25)
        self.bg3 = Drawable(vec(0,0), "backgroundClose.png", parallax=0.5)
        self.bgWidth1 = self.bg1.getSize()[0]
        self.bgWidth2 = self.bg2.getSize()[0]
        self.bgWidth3 = self.bg3.getSize()[0]
        self.tiles1 = math.ceil( RESOLUTION[0] / self.bgWidth1 ) + 1
        self.tiles2 = math.ceil( RESOLUTION[0] / self.bgWidth2 ) + 1
        self.tiles3 = math.ceil( RESOLUTION[0] / self.bgWidth3 ) + 1
        self.scrollFar = 0
        self.scrollMedium = 0
        self.scrollClose = 0

        #score / currency system
        self.font = pygame.font.SysFont("default8", 25)
        
        pygame.mouse.set_visible(False)

        #Music
        self.music = SoundManager.getInstance()
        self.music.playBGM("backgroundMusic.ogg")
    
    def draw(self, drawSurface):
        for t1 in range(0, self.tiles1):
            self.background1 = Drawable((t1 * self.bgWidth1 + self.scrollFar, 0), "backgroundFar.png", parallax=1)
            self.background1.draw(drawSurface)
        for t2 in range(0, self.tiles2):
            self.background2 = Drawable((t2 * self.bgWidth2 + self.scrollMedium, 0), "backgroundMedium.png", parallax=1)
            self.background2.draw(drawSurface)
        for t3 in range(0, self.tiles3):
            self.background3 = Drawable((t3 * self.bgWidth3 + self.scrollClose, 0), "backgroundClose.png", parallax=1)
            self.background3.draw(drawSurface)
        self.scrollFar -=0.5
        self.scrollMedium -=2
        self.scrollClose -=6

        if abs(self.scrollFar) > self.bgWidth1:
            self.scrollFar = 0
        if abs(self.scrollMedium) > self.bgWidth2:
            self.scrollMedium = 0
        if abs(self.scrollClose) > self.bgWidth3:
            self.scrollClose = 0
        
        self.hero.draw(drawSurface)
        
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
        self.hero.update(seconds)
        for i in range(0, len(self.hero.lasers)):
            self.hero.lasers[i].update(seconds)

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
            #self.hero.lasers[i].update(seconds)
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

