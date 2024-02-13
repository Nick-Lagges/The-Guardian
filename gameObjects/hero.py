from . import Mobile
from FSMs import WalkingFSM, AccelerationFSM
from utils import vec, RESOLUTION

from pygame.locals import *

import pygame
import numpy as np


class Hero(Mobile):
   def __init__(self, position):
      super().__init__(position, "heros.png")
        
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
      
      
   def handleEvent(self, event):
      if event.type == KEYDOWN:
         if event.key == K_w:
            self.UD.decrease()
             
         elif event.key == K_s:
            self.UD.increase()
            
         '''elif event.key == K_LEFT:
            self.LR.decrease()
            
         elif event.key == K_RIGHT:
            self.LR.increase()'''
            
      elif event.type == KEYUP:
         if event.key == K_w:
            self.UD.stop_decrease()
             
         elif event.key == K_s:
            self.UD.stop_increase()
             
            
         '''elif event.key == K_LEFT:
            self.LR.stop_decrease()
            
         elif event.key == K_RIGHT:
            self.LR.stop_increase()'''
   
   def update(self, seconds): 
      #self.LR.update(seconds)
      self.UD.update(seconds)
      
      super().update(seconds)
   
   
  
