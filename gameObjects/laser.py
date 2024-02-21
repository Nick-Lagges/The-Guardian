from . import Mobile
from utils import vec, RESOLUTION, normalize

from pygame.locals import *

import pygame
import numpy as np


class Laser(Mobile):
   def __init__(self, position, direction, damage):
      super().__init__(position, "laser.png")
      self.damage = damage
      x,y = direction
      a,b = position
      self.velocity[0] = x-a
      self.velocity[1] = y-b
      #print(self.getSize())        
   
   def update(self, seconds):
       super().update(seconds)
       #print(self.position)
       
      
   def updateMovement(self):
      pass
   
   
  
