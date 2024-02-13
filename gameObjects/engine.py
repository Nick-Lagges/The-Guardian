import pygame

from . import Drawable, Hero

from utils import vec, RESOLUTION

class GameEngine(object):
    import pygame

    def __init__(self):       
        self.hero = Hero((0,0))
        self.size = vec(*RESOLUTION)
        self.background = Drawable((0,0), "background.png")
    
    def draw(self, drawSurface):        
        self.background.draw(drawSurface)
        
        self.hero.draw(drawSurface)
            
    def handleEvent(self, event):
        self.hero.handleEvent(event)
    
    def update(self, seconds):
        self.hero.update(seconds)
        
        Drawable.updateOffset(self.hero, self.size)
    

