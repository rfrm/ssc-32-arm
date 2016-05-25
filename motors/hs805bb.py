from motor import Motor

class HS805BB(Motor):
    def __init__(self):
        super(HS805BB, self).__init__()

    # @property
    # def curve(self):
    #     return {'degrees': [0, 44.5, 51, 54, 60, 65.5, 72, 80, 85, 90, 95, 100,
    #     					110, 120, 135, 180],
    #             'pwm': [750, 1100, 1150, 1180, 1220, 1270, 1320, 1385, 1420, 1460, 1500, 1525,
    #             		1615, 1685, 1790, 2250]}

    @property
    def curve(self):
        return {'degrees': [0, 180],
                'pwm': [750, 2250]}