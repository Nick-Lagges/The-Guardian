from UI import ScreenManager, ArcadeScreenManager, ZenScreenManager
from FSMs import LevelFSM
import pygame

class LevelManager(object):
    """creates the level manaeger to manuever between levels"""
    def __init__(self, numLevels=3):
        self.levels = [ScreenManager(), ArcadeScreenManager(), ZenScreenManager()]
        self.state = LevelFSM(self, numLevels)
    
    def update(self, seconds):
        if self.state == "activeLevel":
            self.levels[self.state.currentLevel].update(seconds)
        else:
            self.state.loadLevel()  
  
    def handleEvent(self, event):
        if self.state == "activeLevel":
            self.levels[self.state.currentLevel].handleEvent(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_2 and self.levels[self.state.currentLevel].state != "arcade":
                self.state.nextLevel()
                #print(self.levels[self.state.currentLevel].state)
    
    def draw(self, drawSurface):
        if self.state == "activeLevel":
            self.levels[self.state.currentLevel].draw(drawSurface)

    def continueGame(self):
        if self.levels[self.state.currentLevel].hero.lives > 0:
            return True
        return False
