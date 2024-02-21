'''
Nick Lagges

static timer
'''


class TimerStatic(object):
    def __init__(self, setTo):
    	self.time = 0
    	self.setTo = setTo
    	self.reset()
    
    def reset(self):
    	self.time = self.setTo
    
    def done(self):
    	return self.time <= 0

    def update(self, seconds):
    	self.time -= seconds

