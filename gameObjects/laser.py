from . import Mobile
from utils import vec, RESOLUTION, normalize

from pygame.locals import *

import pygame
import numpy as np


class Laser(Mobile):
   def __init__(self, position, direction, damage, good):
      if good:
          super().__init__(position, "heroLaser.png")
      else:
          super().__init__(position, "alienLaser.png")
      self.damage = damage
      x,y = direction
      a,b = position
      self.velocity[0] = (x-a) * 10
      self.velocity[1] = (y-b) * 10
      #print(self.getSize())

      '''self.framesPerSecond = 1
      self.nFrames = 1
      self.nFramesList = {
          "good" : 1,
          "evil" : 1
          }
      
      self.rowList = {
          "good" : 0,
          "evil" : 1
          }

      self.framesPerSecondList = {
          "good" : 1,
          "evil" : 1
          }

      self.FSManimated = WalkingFSM(self)
      self.LR = AccelerationFSM(self, axis=0)
      self.UD = AccelerationFSM(self, axis=1)'''
   
   def update(self, seconds):
       super().update(seconds)
       #print(self.position)
       
      
   def updateMovement(self):
      pass
   
   
  
