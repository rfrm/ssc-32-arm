import math, sys
from time import sleep
from sympy import *
from motors import *
import logging

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger()

class Robot:
    def __init__(self, ser, **kwargs):
        self.ser = ser
        self.l1 = kwargs['l1']
        self.l2 = kwargs['l2']
        self.l3 = kwargs['l3']
        self.l4 = kwargs['l4']
        self.l5 = kwargs['l5']
        self.motors = [MotorBase(), HS805BB(), HS645MG(), HS422()]

    def move_piece(self, piece, from_square, to_square):
        self.open_gripper()
        self.take_piece(from_square, piece)
        self.lift_piece(from_square, piece)
        self.release_piece(to_square, piece)
        self.go_home()

    def take_piece(self, square, piece):
        x, y, z = self.get_coordinates_to_get_or_release_piece(square, piece)
        self.make_down_trajectory_to(x, y, z)
        self.close_gripper()
    
    def make_down_trajectory_to(self, x, y, z):
        trajectory = [(0,12,12), (x,y,25), (x,y,z)]
        self.execute_trajectory(trajectory)

    def close_gripper(self):
        self.ser.write("#4P2400\r")
        self.__wait_for_completion()

    def lift_piece(self, square, piece):
        x, y, z = self.get_coordinates_to_get_or_release_piece(square, piece)
        self.make_lift_trajectory(x, y, z)

    def release_piece(self, square, piece):
        x, y, z = self.get_coordinates_to_get_or_release_piece(square, piece)
        self.make_release_trajectory_to(x, y, z)
        self.open_gripper()

    def open_gripper(self):
        self.ser.write("#4P600\r")
        self.__wait_for_completion()

    def make_release_trajectory_to(self, x, y, z):
        trajectory = [(x,y,25), (x,y,z)]
        self.execute_trajectory(trajectory)
            
    def make_lift_trajectory(self, x, y, z):
        trajectory = [(x,y,25), (0,12,12)]
        self.execute_trajectory(trajectory)

    def execute_trajectory(self, trajectory):
        for px, py, pz in trajectory:
            self.move_to(px, py, pz)
            sleep(0.1)

    def get_coordinates_to_get_or_release_piece(self, square, piece):
        column, row = square[0], square[1]
        y_for_rows =   {'1': 15, '2': 21, '3': 26, '4': 31, '5': 36, '6': 41.5, '7': 46.5, '8': 51.5}
        x_for_colums = {'a': -19, 'b': -13.5, 'c': -8, 'd': -2.5, 'e': 2.5, 'f': 8, 'g': 13.5, 'h': 19}
        x, y = x_for_colums[column], y_for_rows[row]
        if piece == 'K' or piece == 'Q':
            z = 6
        elif piece == 'B':
            z = 4
        elif piece == 'N' or piece == 'T':
            z = 2
        else:
            z = 0

        return (x, y, z)

    def go_home(self):
        self.move_to(0, 20, 25)

    def move_to(self, px, py, pz):
        vals = self.pwm_for(px, py, pz)
        msg = " ".join("#%dP%d"%(i, pwm) for i, pwm in enumerate(vals))
        self.ser.write(msg+"T2000\r")
        self.__wait_for_completion()

    def __wait_for_completion(self):
        self.ser.write("Q\r")
        while self.ser.read() == '+':
            self.ser.write("Q\r")

    def pwm_for(self, px, py, pz):
        degrees = self.joint_degrees_for(px, py, pz)
        logger.info("The angular coordinates for %s are %s" % (str((px,py,pz)), str(degrees)))
        pwms = [int(motor.pwm(degree)) for motor, degree in zip(self.motors, degrees)]
        logger.info("The PWMs are %s" % str(pwms))
        pwms[0] = 3000 - pwms[0]
        return pwms

    def joint_degrees_for(self, px, py, pz):
        q2, q3 = symbols('q2 q3')
        l1, l2, l3, l4, l5 = self.l1, self.l2, self.l3, self.l4, self.l5
        equations = (l2+l3*cos(q2)+l4*cos(q3-q2)-root(px**2+py**2, 2),
                     l1+l3*sin(q2)+l4*sin(q2-q3)-pz-l5)

        q1 = math.degrees(math.atan2(py, px))
        q2, q3 = [math.degrees(s) for s in nsolve(equations, (q2, q3), (1, 1), verify=False)]
        q4 = 90+q2-q3 

        return (q1, q2, q3, q4)