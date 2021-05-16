# ----------------- Libraries
import pyfirmata
import serial.tools.list_ports
import sys
import time
import pycom
import numpy as np

# ----------------- Initial Terms
Servo_inner = 7
Servo_bottom = 6
Servo_top = 5
small_servo_arm_3 = 3
small_servo_top = 2
small_servo_gripper = 8

echo_pin = 13
trig_pin = 12

theta_1_init = 140
theta_2_init = 90
theta_0_init = 0
theta_arm_3 = 30

# --------- Chester
"""
Object Chester:
Holds all control systems and commands 

"""

class Chester:

    def __init__(self, board):
        self.board = board
        self.control_array = np.array([[Servo_inner,0],[Servo_top,0],[Servo_bottom,0],[small_servo_arm_3,0],
                                  [small_servo_top,0],[small_servo_gripper,0]],dtype=np.int)

    def setServoAngle(self, pin, angle):
        """
        :param pin: pin wanting to write too
        :param angle: angle wanting to write
        :return: void
        """
        board.digital[pin].write(angle)
        time.sleep(0.0015)

    def set_angle(self, pin, angle_s, update=True):
        """
        :param pin: pin wanting to write too
        :param angle_s: angle wanting to write shifted into new coordinate system
        :param update: bool value determine whether to update the control array with the new angle
        :return: void
        """
        if pin == Servo_bottom:
            if (angle_s > 90):
                angle_s = 90
                print("Exceeding Tolerances")
            angle_write = theta_1_init - angle_s

        if pin == Servo_top:
            angle_write = angle_s + theta_2_init

        if pin == Servo_inner:
            angle_write= angle_s - theta_0_init

        if pin == small_servo_arm_3:
            angle_write = angle_s

        if pin == small_servo_gripper:
            angle_write = angle_s

        if pin == small_servo_top:
            angle_write = angle_s

        self.setServoAngle(pin, angle_write)

        if (update):
            rows, cols = np.where(self.control_array == pin)
            self.control_array[rows] = np.array([pin, angle_s])


    def angle_slow(self, pin, angle_target):
        """
        :param pin: pin to write too
        :param angle_target: angle to move too
        :return: void
        """
        rows, cols = np.where(self.control_array==pin)
        start_angle = self.control_array[rows][0][1]
        self.control_array[rows] = np.array([pin, angle_target])
        if (pin == Servo_inner or pin == Servo_bottom or [pin ==Servo_top]):
            if (start_angle < angle_target):
                unit = 1
            else:
                unit = -1
            for i in range(start_angle, angle_target, unit):
                self.set_angle(pin, i, update=False)
                time.sleep(.03)
        else:
            self.set_angle(pin, angle_target)

    def run_routine(self, routine):
        """
        :param routine: a list with pins and angle positions
        :return: void
        """
        print("Running Routine....")
        for i in range(0, len(routine)):
            self.angle_slow(routine[i][0], routine[i][1])
            time.sleep(.4)
        print("Routine Ended")

    def initialize(self):
        """
        runs a initializion sequence sets servos to 0 angle_s
        :return: void
        """
        time.sleep(2)

        board.digital[Servo_inner].mode = pyfirmata.SERVO
        board.digital[Servo_bottom].mode = pyfirmata.SERVO
        board.digital[Servo_top].mode = pyfirmata.SERVO
        board.digital[small_servo_gripper].mode = pyfirmata.SERVO
        board.digital[small_servo_arm_3].mode = pyfirmata.SERVO
        board.digital[small_servo_top].mode = pyfirmata.SERVO

        self.control_array = np.array([[Servo_inner,0],[Servo_top,0],[Servo_bottom,0],[small_servo_arm_3,0],
                                       [small_servo_top,0],[small_servo_gripper,0]],dtype=np.int)

        self.setServoAngle(Servo_bottom, theta_1_init)
        self.setServoAngle(Servo_inner, theta_0_init)
        self.setServoAngle(Servo_top, theta_2_init)
        self.setServoAngle(small_servo_arm_3, theta_arm_3)

    def rest(self):
        """
        sets motors to rest position
        :return: void
        """
        rest = [[Servo_inner, 0], [small_servo_arm_3, 70], [Servo_bottom, 30] ,[Servo_top, 70]]
        self.run_routine(rest)

    def basic_routine(self):
        """
        simple routine for testing
        :return: void
        """
        routine_1 = [[Servo_inner, 120], [Servo_inner, 0], [Servo_top, -40],
                     [Servo_top, 0], [small_servo_arm_3, 110],
                     [small_servo_top, 90],[small_servo_arm_3, 30], [small_servo_top, 0],
                     [Servo_top, 40], [small_servo_top, 90], [small_servo_arm_3, 100],
                     [small_servo_top, 0],[Servo_top, 0], [small_servo_arm_3, 30],
                     [Servo_inner, 90], [Servo_inner, 0]]
        self.run_routine(routine_1)


# -------- Implementation
board = pyfirmata.Arduino('COM3')
Chester = Chester(board)
Chester.initialize()
Chester.basic_routine()
Chester.rest()

