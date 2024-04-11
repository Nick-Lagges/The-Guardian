from . import Mobile
from . import Drawable
from . import Laser
from . import Weapon
from FSMs import FlyingFSM, AccelerationFSM
from utils import vec, RESOLUTION, SCALE, SoundManager

from pygame.locals import *

import pygame
import numpy as np


class Hero(Mobile):

   _INSTANCE = None

   @classmethod
   def getInstance(cls):
      """Used to obtain the singleton instance"""
      if cls._INSTANCE == None:
         cls._INSTANCE = cls._Hero( (0,(RESOLUTION[1]*0.45)), 100 )

      return cls._INSTANCE

   class _Hero(Mobile):
   
      def __init__(self, position, health, parallax=1):
         super().__init__(position, "heros.png", parallax)
         self.music = SoundManager.getInstance()

         self.weapons = Weapon(position)
         
         self.health = health
         self.score = 0
         self.damage = 5
         self.lives = 5
         #upgrades
         self.level = [1,2,0]
         self.gunCost = 10
         self.gunLevel = 1
         self.healthCost = 10
         self.baseCost = 30
         # Animation variables specific to the hero
         self.framesPerSecond = 1 
         self.nFrames = 1

         self.nFramesList = {
            "up"   : 2,
            "down" : 2,
            "standing" : 2
         }
      
         self.rowList = {
            "up"   : self.level[0],
            "down" : self.level[1],
            "standing" : self.level[2]
         }
      
         self.framesPerSecondList = {
            "up"   : 2,
            "down" : 2,
            "standing" : 2
         }
            
         self.FSManimated = FlyingFSM(self)
         self.LR = AccelerationFSM(self, axis=0)
         self.UD = AccelerationFSM(self, axis=1)

         self.lasers = []      
      
      def handleEvent(self, event):
         if event.type == KEYDOWN:
            if event.key == K_w:
               self.UD.decrease()
             
            elif event.key == K_s:
               self.UD.increase()
            
            elif event.key == K_a:
               self.LR.decrease()
            
            elif event.key == K_d:
               self.LR.increase()
            
         elif event.type == KEYUP:
            if event.key == K_w:
               self.UD.stop_decrease()
             
            elif event.key == K_s:
               self.UD.stop_increase()
             
            
            elif event.key == K_a:
               self.LR.stop_decrease()
            
            elif event.key == K_d:
               self.LR.stop_increase()
         elif event.type == MOUSEBUTTONDOWN:
            shootPos = vec(*event.pos) // SCALE - vec(5,5)
            cannonx = self.position[0] + self.getSize()[0]
            cannony = self.position[1] + 10
            laser = Laser((cannonx,cannony), shootPos, self.damage, True, gunLevel=self.gunLevel)
            self.lasers.append(laser)

      def getPosition(self):
         return self.position

      def alive(self):
         if self.health > 0:
            return True
         return False

      def upgradeGuns(self):
         if self.score < self.gunCost or self.gunLevel > 4:
            return
         else:
            self.gunLevel += 1
            self.damage *= 1.7
            self.score -= self.gunCost
            self.gunCost += 25
            self.weapons.weaponsLevel += 1
            self.music.playSFX("chaching.wav")
            
      def upgradeHealth(self):
         if self.score < self.healthCost:
            return
         else:
            self.health += 100
            self.score -= self.healthCost
            self.healthCost += 50
            self.music.playSFX("chaching.wav")

      def upgradeBase(self):
         if self.score < self.baseCost or self.level[2] == 9:
            return
         else:
            self.UD.accel += 100
            self.level[0] += 3
            self.level[1] += 3
            self.level[2] += 3
            self.rowList = {
               "up"   : self.level[0],
               "down" : self.level[1],
               "standing" : self.level[2]
               }
            print(self.level[2])
            self.score -= self.baseCost
            self.baseCost *= 2
            self.music.playSFX("chaching.wav")

      def draw(self, drawSurface):
         super().draw(drawSurface)
         self.weapons.draw(drawSurface)
   
      def update(self, seconds): 
         self.LR.update(seconds)
         self.UD.update(seconds)
         super().update(seconds)

         self.weapons.position = self.position
         self.weapons.update(seconds)

      def updateMovement(self):
         pass
   
   
  
