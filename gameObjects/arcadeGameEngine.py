'''
Nick Lagges

scrolling background from: 
'''

import pygame
import math
import random
import time

from . import Drawable, Hero, Laser, Alien, TestGameEngine

from utils import vec, RESOLUTION, SCALE, TimerStatic, SoundManager

class ArcadeGameEngine(TestGameEngine):
    import pygame

    def __init__(self):
        super().__init__()
        
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
        for wave2 in range(0, 6):
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
        for wave3 in range(0, 7):
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
        for wave4 in range(0, 8):
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

        self.startTime = time.time()
    
    def draw(self, drawSurface):
        super().draw(drawSurface)
        #Best Time
        file = open("bestTime.txt", 'r')
        self.BT = file.readline()
        file.close()
        xBT,yBT = list(map(int, RESOLUTION))
        xBT *= 0.45
        yBT *= 0.02
        BTBoard = "Best Time: " + str(self.BT)
        BTMessage = self.font.render(BTBoard, True, (255,255,255))
        drawSurface.blit(BTMessage, (xBT,yBT))

        #Current Time
        
        xCT,yCT = list(map(int, RESOLUTION))
        xCT *= 0.7
        yCT *= 0.02
        CTBoard = "Time: " + str(round((time.time() - self.startTime), 2))
        CTMessage = self.font.render(CTBoard, True, (255,255,255))
        drawSurface.blit(CTMessage, (xCT,yCT))
        
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

        if len(self.waveNine) == 0:
            self.endTime = time.time()
            self.wholeTime = self.endTime - self.startTime
            if self.wholeTime < float(self.BT):
                recordFile = open("bestTime.txt", 'w')
                print(round(self.wholeTime, 2))
                recordFile.write(str(round(self.wholeTime, 2)))
                recordFile.close()
            #WIN
            xWin,yWin = list(map(int, RESOLUTION))
            xWin *= 0.22
            yWin *= 0.5
            winText = "YOU WIN!!!"
            self.winFont = pygame.font.SysFont("default8", 100)
            rgb = [(255,0,0), (0,255,0), (0,0,255)]
            winMessage = self.winFont.render(winText, True, random.choice(rgb))
            drawSurface.blit(winMessage, ( (xWin),(yWin-25) ))
    
    def update(self, seconds):
        super().update(seconds)
        self.waveOneTimer.update(seconds)

        if self.waveOneTimer.done():
            self.spawnAliens1 = True
            self.alienCollisionUpdate(self.waveOne, seconds)
            self.heroLaserCollisionUpdate(self.waveOne, seconds)
            if len(self.waveOne) == 0:
                if not self.endOfWave[0]:
                    #print(1)
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
                    #print(2)
                    self.music.playSFX("explosion.wav")
                    self.endOfWave[1] = True
                self.waveThreeTimer.update(seconds)

        if self.waveThreeTimer.done():
            self.spawnAliens3 = True
            self.alienCollisionUpdate(self.waveThree, seconds)
            self.heroLaserCollisionUpdate(self.waveThree, seconds)
            if len(self.waveThree) == 0:
                if not self.endOfWave[2]:
                    #print(3)
                    self.music.playSFX("explosion.wav")
                    self.endOfWave[2] = True
                self.waveFourTimer.update(seconds)

        if self.waveFourTimer.done():
            self.spawnAliens4 = True
            self.alienCollisionUpdate(self.waveFour, seconds)
            self.heroLaserCollisionUpdate(self.waveFour, seconds)
            if len(self.waveFour) == 0:
                if not self.endOfWave[3]:
                    #print(4)
                    self.music.playSFX("explosion.wav")
                    self.endOfWave[3] = True
                self.waveFiveTimer.update(seconds)

        if self.waveFiveTimer.done():
            self.spawnAliens5 = True
            self.alienCollisionUpdate(self.waveFive, seconds)
            self.heroLaserCollisionUpdate(self.waveFive, seconds)
            if len(self.waveFive) == 0:
                if not self.endOfWave[4]:
                    #print(5)
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
        
        
