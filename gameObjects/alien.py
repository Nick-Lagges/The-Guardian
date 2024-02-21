from . import Mobile
from . import Laser
from FSMs import WalkingFSM, AccelerationFSM
from utils import vec, RESOLUTION, SCALE, TimerStatic
from . import Hero

from pygame.locals import *

import pygame
import numpy as np
import random

class Alien(Mobile):
   def __init__(self, position, health):
      super().__init__(position, "enemies.png")
      self.health = health      
      self.velocity[0] = random.choice([-1,1]) * random.randint(45,50)
      self.velocity[1] = random.choice([-1,1]) * random.randint(45,50)
      hero = Hero.getInstance()
      # Animation variables specific to the alien
      self.framesPerSecond = 1 
      self.nFrames = 1
      randShip = 0
      self.nFramesList = {
         "standing" : 2,
         "up" : 2,
         "down" : 1
      }
      
      self.rowList = {
         "standing" : randShip,
         "up" : 0,
         "down" : 1
      }
      
      self.framesPerSecondList = {
         "standing" : 2,
         "up" : 2,
         "down" : 2
      }
            
      self.FSManimated = WalkingFSM(self)
      self.LR = AccelerationFSM(self, axis=0)
      self.UD = AccelerationFSM(self, axis=1)

      #alien attack timer
      self.attackTimer = TimerStatic((random.randint(-2,2) * 0.1) + 3)

   def alive(self):
       if self.health > 0:
           return True
       return False
   
   def update(self, seconds):
      super().update(seconds)
      self.attackTimer.update(seconds)
      if self.attackTimer.done():
          self.attackTimer.reset()
          
      edgeX = RESOLUTION[0] - self.getSize()[0]
      edgeY = RESOLUTION[1] - self.getSize()[1]
      if self.position[0] < RESOLUTION[0] // 2:
          self.velocity[0] = -self.velocity[0]
      elif self.position[0] > edgeX:
          self.velocity[0] = -self.velocity[0]
      elif self.position[1] < 1 // 2:
          self.velocity[1] = -self.velocity[1]
      elif self.position[1] > edgeY:
          self.velocity[1] = -self.velocity[1]

   def updateMovement(self):
      pass
   
   
  
