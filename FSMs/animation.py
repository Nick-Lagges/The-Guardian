from . import AbstractGameFSM
from utils import magnitude, EPSILON, SpriteManager

from statemachine import State

class AnimateFSM(AbstractGameFSM):
    """For anything that animates. Adds behavior on
       transitioning into a state to change animation."""
    def on_enter_state(self):
        state = self.current_state.id
        if self.obj.row != self.obj.rowList[state]:
            self.obj.nFrames = self.obj.nFramesList[state]
            self.obj.frame = 0
            self.obj.row = self.obj.rowList[state]
            self.obj.framesPerSecond = self.obj.framesPerSecondList[state]
            self.obj.animationTimer = 0
            self.obj.image = SpriteManager.getInstance().getSprite(self.obj.imageName,
                                                                   (self.obj.frame, self.obj.row))
         
        
class FlyingFSM(AnimateFSM):
    """Three-state FSM for flying a spaceship."""
       
    standing = State(initial=True)
    up = State()
    down = State()

    climb = standing.to(up)
    fall = standing.to(down)
    stop = up.to(standing) | down.to(standing)
    
    def updateState(self):
        if self.hasVelocity() and self == "standing":
            if self.obj.velocity[1] > 0:
                self.climb()
            elif self.obj.velocity[1] < 0:
                self.fall()
        elif not self.hasVelocity() and self == "up":
            self.stop()
        elif not self.hasVelocity() and self == "down":
            self.stop()
    
    def hasVelocity(self):
        return magnitude(self.obj.velocity) > EPSILON
    
    def noVelocity(self):
        return not self.hasVelocity()

class UpgradingFSM(AnimateFSM):

    levelOne = State(initial=True)
    levelTwo = State()
    levelThree = State()
    levelFour = State()
    levelFive = State()

    stay1 = levelOne.to.itself(internal=True)
    stay2 = levelTwo.to.itself(internal=True)
    stay3 = levelThree.to.itself(internal=True)
    stay4 = levelFour.to.itself(internal=True)
    stay5 = levelFive.to.itself(internal=True)
    upgrade1 = levelOne.to(levelTwo)
    upgrade2 = levelTwo.to(levelThree)
    upgrade3 = levelThree.to(levelFour)
    upgrade4 = levelFour.to(levelFive)
    downgrade1 = levelTwo.to(levelOne)
    downgrade2 = levelThree.to(levelTwo)
    downgrade3 = levelFour.to(levelThree)
    downgrade4 = levelFive.to(levelFour)

    def updateState(self):
        if self.canUpgrade():
            if self == "levelOne" and self.obj.weaponsLevel == 2:
                self.upgrade1()
            elif self == "levelTwo" and self.obj.weaponsLevel == 3:
                self.upgrade2()
            elif self == "levelThree" and self.obj.weaponsLevel == 4:
                self.upgrade3()
            elif self == "levelFour" and self.obj.weaponsLevel == 5:
                self.upgrade4()
        elif not self.canUpgrade():
            if self == "levelOne":
                self.stay1()
            elif self == "levelTwo":
                self.stay2()
            elif self == "levelThree":
                self.stay3()
            elif self == "levelFour":
                self.stay4()
            elif self == "levelFive":
                self.stay5()

    def canUpgrade(self):
        return self.obj.weaponsLevel > 0
