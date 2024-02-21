from . import Mobile
from . import Laser
from FSMs import WalkingFSM, AccelerationFSM
from utils import vec, RESOLUTION, SCALE

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
   
      def __init__(self, position, health):
         super().__init__(position, "heros.png")
         self.health = health
         # Animation variables specific to the hero
         self.framesPerSecond = 1 
         self.nFrames = 1

         self.nFramesList = {
            "up"   : 2,
            "down" : 2,
            "standing" : 2
         }
      
         self.rowList = {
            "up"   : 1,
            "down" : 2,
            "standing" : 0
         }
      
         self.framesPerSecondList = {
            "up"   : 2,
            "down" : 2,
            "standing" : 2
         }
            
         self.FSManimated = WalkingFSM(self)
         self.LR = AccelerationFSM(self, axis=0)
         self.UD = AccelerationFSM(self, axis=1)

         self.lasers = []
      '''for i in range(0, len(self.lasers)):
         self.lasers[i].draw()'''
      
      
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
            laser = Laser((cannonx,cannony), shootPos, 5)
            self.lasers.append(laser)
            #print(self.lasers)
         
   
      def update(self, seconds): 
         self.LR.update(seconds)
         self.UD.update(seconds)
         super().update(seconds)

      def updateMovement(self):
         pass
   
   
  
