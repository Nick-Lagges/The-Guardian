from . import AbstractGameFSM
from statemachine import State


class ScreenManagerFSM(AbstractGameFSM):
    mainMenu = State(initial=True)
    arcade     = State()
    zen = State()
    paused   = State()
    
    pauseA = arcade.to(paused) | paused.to(arcade)
    pauseZ = zen.to(paused) | paused.to(zen)
    pause = mainMenu.to.itself(internal=True)
    
    startArcade = mainMenu.to(arcade) | zen.to(arcade)
    startZen = mainMenu.to(zen) | arcade.to(zen)
    quitGame  = arcade.to(mainMenu) | \
                paused.to.itself(internal=True) | \
                zen.to(mainMenu)
    
    def isInGame(self):
        return self == "arcade" or self == "zen" or self == "paused"
    
    def on_enter_game(self):
        self.obj.game.hero.updateMovement()
    
