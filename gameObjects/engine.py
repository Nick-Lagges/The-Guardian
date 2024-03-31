'''
Nick Lagges

scrolling background from: 
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
        self.bgWidth2 = self.bg3.getSize()[0]
        self.bgWidth3 = self.bg3.getSize()[0]
        self.tiles1 = math.ceil( RESOLUTION[0] / self.bgWidth1 ) + 1
        self.tiles2 = math.ceil( RESOLUTION[0] / self.bgWidth2 ) + 1
        self.tiles3 = math.ceil( RESOLUTION[0] / self.bgWidth3 ) + 1
        self.scrollFar = 0
        self.scrollMedium = 0
        self.scrollClose = 0

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
        self.waveThreeTimer = TimerStatic(5)
        self.spawnAliens3 = False

        #Fourth wave of aliens
        #200 health, 50 damage
        self.waveFour = []
        spawnXAlien4 = 480
        spawnYAlien4 = 50
        for wave4 in range(0, 9):
            x,y = (spawnXAlien4, spawnYAlien4)
            #print(x,y)
            self.waveFour.append(Alien((x,y), 200, 50))
            self.waveFour[wave4].rowList = {
                "up"   : 1,
               "down" : 1,
               "standing" : 1
                }
            spawnYAlien4 += 30
            if wave4 == 3:
                spawnXAlien4 += 70
                spawnYAlien4 = 50
        self.waveFourTimer = TimerStatic(7)
        self.spawnAliens4 = False

        #Fifth wave of aliens
        #250 health, 70 damage
        self.waveFive = []
        spawnXAlien5 = 480
        spawnYAlien5 = 50
        for wave5 in range(0, 9):
            x,y = (spawnXAlien5, spawnYAlien5)
            #print(x,y)
            self.waveFive.append(Alien((x,y), 250, 70))
            self.waveFive[wave5].rowList = {
                "up"   : 1,
               "down" : 1,
               "standing" : 1
                }
            spawnYAlien5 += 30
            if wave5 == 3:
                spawnXAlien5 += 70
                spawnYAlien5 = 50
        self.waveFiveTimer = TimerStatic(5)
        self.spawnAliens5 = False

        #Sixth wave of aliens
        #300 health, 100 damage
        self.waveSix = []
        spawnXAlien6 = 480
        spawnYAlien6 = 50
        for wave6 in range(0, 9):
            x,y = (spawnXAlien6, spawnYAlien6)
            #print(x,y)
            self.waveSix.append(Alien((x,y), 300, 100))
            self.waveSix[wave6].rowList = {
                "up"   : 1,
               "down" : 1,
               "standing" : 1
                }
            spawnYAlien6 += 30
            if wave6 == 3:
                spawnXAlien6 += 70
                spawnYAlien6 = 50
        self.waveSixTimer = TimerStatic(5)
        self.spawnAliens6 = False

        #Seventh wave of aliens
        #400 health, 100 damage
        self.waveSeven = []
        spawnXAlien7 = 480
        spawnYAlien7 = 50
        for wave7 in range(0, 9):
            x,y = (spawnXAlien7, spawnYAlien7)
            #print(x,y)
            self.waveSeven.append(Alien((x,y), 400, 100))
            self.waveSeven[wave7].rowList = {
                "up"   : 2,
               "down" : 2,
               "standing" : 2
                }
            spawnYAlien7 += 30
            if wave7 == 3:
                spawnXAlien7 += 70
                spawnYAlien7 = 50
        self.waveSevenTimer = TimerStatic(7)
        self.spawnAliens7 = False

        #Eighth wave of aliens
        #400 health, 125 damage
        self.waveEight = []
        spawnXAlien8 = 480
        spawnYAlien8 = 50
        for wave8 in range(0, 9):
            x,y = (spawnXAlien8, spawnYAlien8)
            #print(x,y)
            self.waveEight.append(Alien((x,y), 400, 125))
            self.waveEight[wave8].rowList = {
                "up"   : 2,
               "down" : 2,
               "standing" : 2
                }
            spawnYAlien8 += 30
            if wave8 == 3:
                spawnXAlien8 += 70
                spawnYAlien8 = 50
        self.waveEightTimer = TimerStatic(5)
        self.spawnAliens8 = False

        #Ninth wave of aliens
        #500 health, 200 damage
        self.waveNine = []
        spawnXAlien9 = 480
        spawnYAlien9 = 50
        for wave9 in range(0, 9):
            x,y = (spawnXAlien9, spawnYAlien9)
            #print(x,y)
            self.waveNine.append(Alien((x,y), 500, 200))
            self.waveNine[wave9].rowList = {
                "up"   : 2,
               "down" : 2,
               "standing" : 2
                }
            spawnYAlien9 += 30
            if wave9 == 3:
                spawnXAlien9 += 70
                spawnYAlien9 = 50
        self.waveNineTimer = TimerStatic(5)
        self.spawnAliens9 = False

        self.endOfWave = [False, False, False, False, False, False, False, False, False]

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
        self.scrollClose -=3

        if abs(self.scrollFar) > self.bgWidth1:
            self.scrollFar = 0
        if abs(self.scrollMedium) > self.bgWidth2:
            self.scrollMedium = 0
        if abs(self.scrollClose) > self.bgWidth3:
            self.scrollClose = 0
        
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

        if self.spawnAliens4:
            self.drawAliens(self.waveFour, drawSurface)

        if self.spawnAliens5:
            self.drawAliens(self.waveFive, drawSurface)

        if self.spawnAliens6:
            self.drawAliens(self.waveSix, drawSurface)

        if self.spawnAliens7:
            self.drawAliens(self.waveSeven, drawSurface)

        if self.spawnAliens8:
            self.drawAliens(self.waveEight, drawSurface)

        if self.spawnAliens9:
            self.drawAliens(self.waveNine, drawSurface)

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
                if not self.endOfWave[0]:
                    self.music.playSFX("explosion.wav")
                    self.endOfWave[0] = True
                self.waveTwoTimer.update(seconds)

        if self.waveTwoTimer.done():
            self.waveOneTimer.reset()
            self.spawnAliens2 = True
            self.alienCollisionUpdate(self.waveTwo, seconds)
            self.heroLaserCollisionUpdate(self.waveTwo, seconds)
            if len(self.waveTwo) == 0:
                if not self.endOfWave[1]:
                    self.music.playSFX("explosion.wav")
                    self.endOfWave[1] = True
                self.waveThreeTimer.update(seconds)

        if self.waveThreeTimer.done():
            self.spawnAliens3 = True
            self.alienCollisionUpdate(self.waveThree, seconds)
            self.heroLaserCollisionUpdate(self.waveThree, seconds)
            if len(self.waveThree) == 0:
                if not self.endOfWave[2]:
                    self.music.playSFX("explosion.wav")
                    self.endOfWave[2] = True
                self.waveFourTimer.update(seconds)

        if self.waveFourTimer.done():
            self.spawnAliens4 = True
            self.alienCollisionUpdate(self.waveFour, seconds)
            self.heroLaserCollisionUpdate(self.waveFour, seconds)
            if len(self.waveFour) == 0:
                if not self.endOfWave[3]:
                    self.music.playSFX("explosion.wav")
                    self.endOfWave[3] = True
                self.waveFiveTimer.update(seconds)

        if self.waveFiveTimer.done():
            self.spawnAliens5 = True
            self.alienCollisionUpdate(self.waveFive, seconds)
            self.heroLaserCollisionUpdate(self.waveFive, seconds)
            if len(self.waveFive) == 0:
                if not self.endOfWave[4]:
                    self.music.playSFX("explosion.wav")
                    self.endOfWave[4] = True
                self.waveSixTimer.update(seconds)

        if self.waveSixTimer.done():
            self.spawnAliens6 = True
            self.alienCollisionUpdate(self.waveSix, seconds)
            self.heroLaserCollisionUpdate(self.waveSix, seconds)
            if len(self.waveSix) == 0:
                if not self.endOfWave[5]:
                    self.music.playSFX("explosion.wav")
                    self.endOfWave[5] = True
                self.waveSevenTimer.update(seconds)

        if self.waveSevenTimer.done():
            self.spawnAliens7 = True
            self.alienCollisionUpdate(self.waveSeven, seconds)
            self.heroLaserCollisionUpdate(self.waveSeven, seconds)
            if len(self.waveSeven) == 0:
                if not self.endOfWave[6]:
                    self.music.playSFX("explosion.wav")
                    self.endOfWave[6] = True
                self.waveEightTimer.update(seconds)

        if self.waveEightTimer.done():
            self.spawnAliens8 = True
            self.alienCollisionUpdate(self.waveEight, seconds)
            self.heroLaserCollisionUpdate(self.waveEight, seconds)
            if len(self.waveEight) == 0:
                if not self.endOfWave[7]:
                    self.music.playSFX("explosion.wav")
                    self.endOfWave[7] = True
                self.waveNineTimer.update(seconds)

        if self.waveNineTimer.done():
            self.spawnAliens9 = True
            self.alienCollisionUpdate(self.waveNine, seconds)
            self.heroLaserCollisionUpdate(self.waveNine, seconds)
            if len(self.waveNine) == 0:
                if not self.endOfWave[8]:
                    self.music.playSFX("explosion.wav")
                    self.endOfWave[8] = True            
        
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

