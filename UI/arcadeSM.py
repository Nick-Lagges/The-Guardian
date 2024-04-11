from FSMs import ScreenManagerFSM
from . import TextEntry, EventMenu
from utils import vec, RESOLUTION
from gameObjects import GameEngine, Hero, ArcadeGameEngine

from pygame.locals import *

class ArcadeScreenManager(object):
      
    def __init__(self):
        self.game = ArcadeGameEngine() # Add your game engine here!
        self.hero = Hero.getInstance()
        self.state = ScreenManagerFSM(self)
        self.pausedText = TextEntry(vec(0,0),"Arcade Paused: p to play or r to restart")

        self.gunCost = "Upgrade Guns: g $" + str(self.hero.gunCost)
        self.healthCost = "Upgrade Health: h $"+ str(self.hero.healthCost)
        self.baseCost = "Upgrade Base: b $" + str(self.hero.baseCost)
        
        self.upgradeGunsText = TextEntry(vec(0,0), self.gunCost)
        self.upgradeHealthText = TextEntry(vec(0,0), self.healthCost)
        self.upgradeBaseText = TextEntry(vec(0,0), self.baseCost)

        self.pausedText.position[0] = RESOLUTION[0] * 0.1
        self.pausedText.position[1] = RESOLUTION[1] * 0.2

        self.upgradeGunsText.position[0] = RESOLUTION[0] * 0.1
        self.upgradeGunsText.position[1] = RESOLUTION[1] * 0.4

        self.upgradeHealthText.position[0] = RESOLUTION[0] * 0.1
        self.upgradeHealthText.position[1] = RESOLUTION[1] * 0.6

        self.upgradeBaseText.position[0] = RESOLUTION[0] * 0.1
        self.upgradeBaseText.position[1] = RESOLUTION[1] * 0.8
        
        self.mainMenu = EventMenu("backgroundFar.png", fontName="default8")
        self.menuText = TextEntry(vec(0,0), "The Guardian")
        self.menuText.position[0] = RESOLUTION[0] // 2 - (self.menuText.getSize()[0] // 2)
        self.menuText.position[1] = RESOLUTION[1] * 0.1
        self.mainMenu.addOption("arcade", "Press 1 to play Arcade Mode",
                                 RESOLUTION // 2 - vec(0,75),
                                 lambda x: x.type == KEYDOWN and x.key == K_1,
                                 center="both")
        self.mainMenu.addOption("zen", "Press 2 to play zen mode",
                                 RESOLUTION // 2,
                                 lambda x: x.type == KEYDOWN and x.key == K_2,
                                 center="both")
        self.mainMenu.addOption("exit", "Press ESC to exit ",
                                 RESOLUTION // 2 + vec(0,75),
                                 lambda x: x.type == KEYDOWN and x.key == K_ESCAPE,
                                 center="both")
    
    
    def draw(self, drawSurf):
        if self.state.isInGame():
            self.game.draw(drawSurf)
        
            if self.state == "paused":
                self.pausedText.draw(drawSurf)
                self.upgradeGunsText.draw(drawSurf)
                self.upgradeHealthText.draw(drawSurf)
                self.upgradeBaseText.draw(drawSurf)
        
        elif self.state == "mainMenu":
            self.mainMenu.draw(drawSurf)
            self.menuText.draw(drawSurf)
    
    def handleEvent(self, event):
        if self.state in ["arcade", "paused"]:
            if event.type == KEYDOWN and event.key == K_r:
                self.state.quitGame()
            elif event.type == KEYDOWN and event.key == K_p:
                self.state.pauseA()
            elif event.type == KEYDOWN and event.key == K_g:
                self.hero.upgradeGuns()
            elif event.type == KEYDOWN and event.key == K_h:
                self.hero.upgradeHealth()
            elif event.type == KEYDOWN and event.key == K_b:
                self.hero.upgradeBase()
            else:
                self.game.handleEvent(event)
        elif self.state == "mainMenu":
            choice = self.mainMenu.handleEvent(event)
            if choice == "arcade":
                self.state.startArcade()
            elif choice == "zen":
                self.state.startZen()
            elif choice == "exit":
                return "exit"
     
    
    def update(self, seconds):      
        if self.state == "arcade" or self.state == "zen":
            self.game.update(seconds)

            if self.hero.gunLevel > 4:
                self.gunCost = "Upgrade Guns: MAXED"
            else:
                self.gunCost = "Upgrade Guns: g $" + str(self.hero.gunCost)
            self.healthCost = "Upgrade Health: h $"+ str(self.hero.healthCost)
            if self.hero.level[2] == 9:
                self.baseCost = "Upgrade Base: MAXED"
            else:
                self.baseCost = "Upgrade Base: b $" + str(self.hero.baseCost)

            self.upgradeGunsText = TextEntry(vec(0,0), self.gunCost)
            self.upgradeHealthText = TextEntry(vec(0,0), self.healthCost)
            self.upgradeBaseText = TextEntry(vec(0,0), self.baseCost)

            self.upgradeGunsText.position[0] = RESOLUTION[0] * 0.1
            self.upgradeGunsText.position[1] = RESOLUTION[1] * 0.4

            self.upgradeHealthText.position[0] = RESOLUTION[0] * 0.1
            self.upgradeHealthText.position[1] = RESOLUTION[1] * 0.6

            self.upgradeBaseText.position[0] = RESOLUTION[0] * 0.1
            self.upgradeBaseText.position[1] = RESOLUTION[1] * 0.8
        elif self.state == "mainMenu":
            self.mainMenu.update(seconds)

    def continueGame(self):
        if self.hero.lives > 0:
            return True
        return False

    
    
