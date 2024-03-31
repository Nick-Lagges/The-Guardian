from . import Animated
from FSMs import UpgradingFSM, AccelerationFSM
from utils import vec, RESOLUTION, SCALE, TimerStatic

from pygame.locals import *

import pygame
import numpy as np
import random

class Weapon(Animated):
   def __init__(self, position):
      super().__init__(position, "guns.png")
      self.framesPerSecond = 1
      self.nFrames = 1
      self.weaponsLevel = 1
      self.nFramesList = {
         "levelOne" : 1,
         "levelTwo" : 1,
         "levelThree" : 1,
         "levelFour" : 1,
         "levelFive" : 1
      }
      
      self.rowList = {
         "levelOne" : 0,
         "levelTwo" : 1,
         "levelThree" : 2,
         "levelFour" : 3,
         "levelFive" : 4
      }
      
      self.framesPerSecondList = {
         "levelOne" : 1,
         "levelTwo" : 1,
         "levelThree" : 1,
         "levelFour" : 1,
         "levelFive" : 1
      }
            
      self.FSManimated = UpgradingFSM(self)
      self.LR = AccelerationFSM(self, axis=0)
      self.UD = AccelerationFSM(self, axis=1)
   
   def update(self, seconds):
      super().update(seconds)

   def updateMovement(self):
      pass
   
   
  
