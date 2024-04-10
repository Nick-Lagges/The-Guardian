from . import Mobile
from . import Laser
from FSMs import FlyingFSM, AccelerationFSM
from utils import vec, RESOLUTION, SCALE, TimerStatic
from . import Hero

from pygame.locals import *

import pygame
import numpy as np
import random

class Alien(Mobile):
   def __init__(self, position, health, damage):
      super().__init__(position, "enemies.png")
      self.health = health      
      self.velocity[0] = random.choice([-1,1]) * random.randint(45,50)
      self.velocity[1] = random.choice([-1,1]) * random.randint(45,50)
      self.hero = Hero.getInstance()
      self.damage = damage
      # Animation variables specific to the alien
      self.framesPerSecond = 2 
      self.nFrames = 2
      self.lasers = []
      self.nFramesList = {
         "standing" : 2,
         "up" : 2,
         "down" : 2
      }
      
      self.rowList = {
         "standing" : 0,
         "up" : 0,
         "down" : 0
      }
      
      self.framesPerSecondList = {
         "standing" : 2,
         "up" : 2,
         "down" : 2
      }
            
      self.FSManimated = FlyingFSM(self)
      self.LR = AccelerationFSM(self, axis=0)
      self.UD = AccelerationFSM(self, axis=1)

      #alien attack timer
      self.attackTimer = TimerStatic((random.randint(-2,2) * 0.5) + 3)

   def alive(self):
       if self.health > 0:
           return True
       return False
   
   def update(self, seconds):
      super().update(seconds)
      self.attackTimer.update(seconds)
      if self.attackTimer.done():
          self.attackTimer.reset()
          cannonx = self.position[0]
          cannony = self.position[1] + 10
          laser = Laser((cannonx,cannony), (self.hero.position + vec(16,16)), self.damage, False)
          self.lasers.append(laser)
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
   
   
  
