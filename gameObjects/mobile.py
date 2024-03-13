from . import Animated
from utils import vec, magnitude, scale

class Mobile(Animated):
    def __init__(self, position, fileName="", parallax=1):
        super().__init__(position, fileName, parallax)
        self.velocity = vec(0,0)
        self.maxVelocity = 300
    
    def update(self, seconds):
        super().update(seconds)
        if magnitude(self.velocity) > self.maxVelocity:
            self.velocity = scale(self.velocity, self.maxVelocity)
        self.position += self.velocity * seconds
