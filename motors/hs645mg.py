from motor import Motor

class HS645MG(Motor):
    def __init__(self):
        super(HS645MG, self).__init__()

    @property
    def curve(self):
        return {'degrees': [0, 180],
                'pwm': [750, 2250]}
