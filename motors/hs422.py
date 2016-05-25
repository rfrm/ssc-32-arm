from motor import Motor

class HS422(Motor):
    def __init__(self):
        super(HS422, self).__init__()

    @property
    def curve(self):
        return {'degrees': [0, 90],
                'pwm': [600, 1500]}
