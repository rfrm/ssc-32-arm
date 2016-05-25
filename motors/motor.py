import numpy as np

class Motor(object):

    @property
    def curve(self):
        raise NotImplementedError

    def pwm(self, degrees):
        return np.interp(degrees, self.curve['degrees'], self.curve['pwm'])
