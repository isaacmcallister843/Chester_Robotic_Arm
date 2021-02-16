import pyfirmata
import serial.tools.list_ports
import sys
import time
import serial
import numpy as np
# def connections(self):
#     list = serial.tools.list_ports.comports()
#     connected = []
#     for element in list:
#     connected.append(element.device)
#     print("Connected COM ports: " + str(connected))
# ----------------- Initial Terms
Servo_inner = 7
Servo_bottom = 6
Servo_top = 5
small_servo_arm_3 = 3
small_servo_top = 2
small_servo_gripper = 8
theta_1_init = 110
theta_2_init = 90
theta_0_init = 0
theta_arm_3 = 30

#arm_1_length =
#arm_2_length =
#arm_3_length =
# --------- Chester


class Chester:
    def __init__(self, board):
        self.board = board
        self.control_array = np.array([[Servo_inner,0],[Servo_top,0],[Servo_bottom,0],[small_servo_arm_3,0],
                                  [small_servo_top,0],[small_servo_gripper,0]],dtype=np.int)

    def setServoAngle(self, pin, angle):
        board.digital[pin].write(angle)
        time.sleep(0.0015)

    def set_angle(self, pin, angle_s, update=True):
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

    def initialize(self):
            time.sleep(5)
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
            self.setServoAngle(small_servo_arm_3 , theta_arm_3)

    def angle_slow(self, pin, angle_target):

        if (pin == Servo_top or pin == Servo_inner or pin == Servo_bottom):
            rows, cols = np.where(self.control_array==pin)
            start_angle = self.control_array[rows][0][1]
            self.control_array[rows] = np.array([pin, angle_target])
            if (start_angle < angle_target):
                unit = int(abs(angle_target-start_angle)/10)
            else:
                unit = -1*int(abs(angle_target-start_angle)/5)
            for i in range(start_angle, angle_target + unit, unit):
                self.set_angle(pin, i, update=False)
                time.sleep(.75)
        else:
            self.set_angle(pin, angle_target)

    def run_routine(self, routine):
        print("Running Routine....")
        time.sleep(2)
        for i in range(0, len(routine)):
            self.angle_slow(routine[i][0], routine[i][1])
            time.sleep(2)
        print("Routine Ended")

    def rest(self):
        rest = [[Servo_bottom, -10] ,[Servo_top, 60]]
        self.run_routine(rest)

    def basic_routine(self):
        routine_1 = [[Servo_top,-10], [Servo_bottom,-10],
                     [Servo_top,20], [small_servo_arm_3, 110], [small_servo_top, 90], [Servo_top, 50],
                     [small_servo_arm_3, 60], [small_servo_arm_3, 100], [small_servo_top, 0],
                     [small_servo_arm_3, 40], [Servo_top, 65]]
        self.run_routine(routine_1)




# -------- Imp
board = pyfirmata.Arduino('COM3')
Chester = Chester(board)
Chester.initialize()
Chester.rest()