'''
Nick Lagges

scrolling background from: 
'''

import pygame
import math
import random

from . import Drawable, Hero, Laser, Alien, GameEngine

from utils import vec, RESOLUTION, SCALE, TimerStatic, SoundManager

class ZenGameEngine(GameEngine):
    import pygame

    #Sets the timer for each wave, initializes waves and round number
    def __init__(self):
        super().__init__()
        self.waveTimer = TimerStatic(3)
        self.waveNum = 0
        self.enemyWave = []
        
        
    #draws the enemies to the screen, along with levels and win/lose text
    def draw(self, drawSurface):
        super().draw(drawSurface)
        #Level
        xLevel,yLevel = list(map(int, RESOLUTION))
        xLevel *= 0.7
        yLevel *= 0.02
        levelBoard = "Level: " + str(self.waveNum)
        levelMessage = self.font.render(levelBoard, True, (255,255,255))
        drawSurface.blit(levelMessage, (xLevel,yLevel))

        #High Score
        file = open("highScore.txt", 'r')
        self.HS = file.readline()
        file.close()
        xHS,yHS = list(map(int, RESOLUTION))
        xHS *= 0.5
        yHS *= 0.02
        HSBoard = "High Score: " + str(self.HS)
        HSMessage = self.font.render(HSBoard, True, (255,255,255))
        drawSurface.blit(HSMessage, (xHS,yHS))
        
        if self.waveTimer.done():
            self.drawAliens(self.enemyWave, drawSurface)
        for i in range(0, len(self.hero.lasers)):
            self.hero.lasers[i].draw(drawSurface)
        if self.hero.lives < 1:
            if self.waveNum > int(self.HS):
                recordFile = open("highScore.txt", 'w')
                recordFile.write(str((self.waveNum - 1)))
                recordFile.close()
            #Lose
            xLoss,yLoss = list(map(int, RESOLUTION))
            xLoss *= 0.22
            yLoss *= 0.5
            lossText = "YOU DIED"
            self.lossFont = pygame.font.SysFont("default8", 100)
            lossMessage = self.lossFont.render(lossText, True, (255,255,255))
            drawSurface.blit(lossMessage, ( (xLoss),(yLoss-25) ))
            self.waveTimer.reset()
        
        
    #updates enemies and lasers, can make another wave in current wave is empty
    def update(self, seconds):
        super().update(seconds)
        self.waveTimer.update(seconds)
        if len(self.enemyWave) == 0:
            self.waveNum += 1
            self.enemyWave = self.makeEnemies()
            self.waveTimer.reset()
            self.music.playSFX("explosion.wav")
        else:
            if self.waveTimer.done():
                #print(len(self.enemyWave))
                self.alienCollisionUpdate(self.enemyWave, seconds)
                self.heroLaserCollisionUpdate(self.enemyWave, seconds)

    #generates a new wave of enemies depending on the current level
    def makeEnemies(self):
        enemies = []
        enemyCount = 0
        damage = 0
        health = 0

        spawnX = 400
        spawnY = 50
        if self.waveNum < 5:
            for i in range(5):
                x,y = (spawnX, spawnY)
                health = random.choice([20, 30, 30, 30, 50, 50, 50, 100])
                damage = random.choice([10, 25, 25, 25, 40, 40, 40, 50])
                enemies.append(Alien((x,y), health, damage, attackFreq=2))
                spawnY += 30
                if i == 3:
                    spawnX += 70
                    spawnY = 50
        elif self.waveNum >= 5 and self.waveNum <= 8:
            for i in range(8):
                x,y = (spawnX, spawnY)
                health = random.choice([100, 125, 125, 125, 150, 150, 150, 200])
                damage = random.choice([45, 50, 50, 50, 75, 75, 75, 100])
                enemies.append(Alien((x,y), health, damage, attackFreq=3))
                enemies[i].rowList = {
                    "up"   : 1,
                   "down" : 1,
                   "standing" : 1
                    }
                spawnY += 30
                if i%3 == 0:
                    spawnX += 70
                    spawnY = 50
            #print(self.waveNum)
        elif self.waveNum > 8 and self.waveNum < 13:
            #print(self.waveNum)
            for i in range(random.randint(10,20)):
                x,y = (spawnX, spawnY)
                health = random.choice([200, 200, 250, 250, 250, 300, 300, 300, 300, 500])
                damage = random.choice([100, 125, 150, 150, 150, 200])
                aF = random.choice([2, 2, 3, 3, 3])
                enemies.append(Alien((x,y), health, damage, attackFreq=aF))
                enemies[i].rowList = {
                    "up"   : 2,
                   "down" : 2,
                   "standing" : 2
                    }
                spawnY += 30
                if i%4 == 0 and i != 0:
                    spawnX += 40
                    spawnY = 50
            #print("wave > 20")
        elif self.waveNum >= 13 and self.waveNum <= 16:
            for i in range(random.randint(10,20)):
                x,y = (spawnX, spawnY)
                health = random.choice([300, 300, 350, 350, 350, 300, 300, 300, 300, 500])
                damage = random.choice([150, 125, 150, 250, 250, 200])
                enemies.append(Alien((x,y), health, damage, attackFreq=2))
                '''enemies[i].rowList = {
                    "up"   : 2,
                   "down" : 2,
                   "standing" : 2
                    }'''
                spawnY += 30
                if i%4 == 0 and i != 0:
                    spawnX += 40
                    spawnY = 50
        elif self.waveNum > 16 and self.waveNum < 20:
            for i in range(random.randint(10,20)):
                x,y = (spawnX, spawnY)
                health = random.choice([450, 450, 450, 450, 500, 500, 500, 600, 1000])
                damage = random.choice([200, 200, 250, 200, 200, 250, 200, 200, 250, 500])
                aF = random.choice([1, 2, 2, 2, 3, 3])
                color = random.randint(0,2)
                enemies.append(Alien((x,y), health, damage, attackFreq=aF))
                enemies[i].rowList = {
                    "up"   : color,
                   "down" : color,
                   "standing" : color
                    }
                spawnY += 30
                if i%4 == 0 and i != 0:
                    spawnX += 40
                    spawnY = 50
        elif self.waveNum >= 20:
            for i in range(random.randint(10,20)):
                x,y = (spawnX, spawnY)
                health = random.choice([500, 600, 1000])
                damage = random.choice([250, 350, 450, 500])
                color = random.randint(0,2)
                aF = color + 1
                enemies.append(Alien((x,y), health, damage, attackFreq=aF))
                enemies[i].rowList = {
                    "up"   : color,
                   "down" : color,
                   "standing" : color
                    }
                spawnY += 30
                if i%4 == 0 and i != 0:
                    spawnX += 40
                    spawnY = 50
        return enemies
        
        




        
