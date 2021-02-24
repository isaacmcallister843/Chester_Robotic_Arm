# Chester (Robotic Arm) 

## Motivation
Currently developing a robotic arm control system in Python. Chester_main uses pyfirmata to communicate with an arduino micro controller and sends commands to various servo motors. Final program will allow the robot to play a game of chess against a human opponent. 

## Build Status
Basic robotic control systems are complete and most of my work involves fine tuning the motor controls. Current to-do: 
- Fine tune motor control systems 
- Add connection to sonar distance sensor
- Add angle thresholds for safety (stop the arm from knocking itself over) 

The chess AI is in the early stages of development, UI elements are done and pygame interface is mainly complete. This project will be documented in its own respository. I did want the arm to be able to map out the location of various pieces on the chess board using the sonar sensor, however the sensor is probably not accurate enough. A small LIDAR sensor might be better. 

## Features 
This project will allow 
- Easy to use routine setup. User friendly control over all motor positions and movement - Complete
- Gripper support allowing the arm to hold and move objects - Complete
- Geospatial system to keep track to gripper location - Complete
- Safety thresholds to ensure stability - In progress, mostly complete 
- Sonar sensor support to measure distance - In progress 
- Chess AI support - In progress

## Code Examples 
All features are supported through the object Chester which takes one input "board" 

```Python
board = pyfirmata.Arduino('COM3')
Chester = Chester(board)
```
Once connected to the arduino commands can be sent to the arm. First the arm needs to be initialized and set to its neutral position, all angles are measured from this location. 

```Python
Chester.initialize()
```

From here custom routines can be sent, specifying motor positions. For example: 

```Python
routine_1 = [[Servo_top,-10], [Servo_bottom,-10],
                     [Servo_top,20], [small_servo_arm_3, 110], [small_servo_top, 90], [Servo_top, 50],
                     [small_servo_arm_3, 60], [small_servo_arm_3, 100], [small_servo_top, 0],
                     [small_servo_arm_3, 40], [Servo_top, 65]]
                     
Chester.run_routine(routine_1) 
```

Future implementation for the sonar sensors will include the method "see" 

```Python
Chester.see()
```
## Installation
Long term goals for this project include making a simple API for motor control, which will be released as a python package. 

## Intellectual Property
Chester_main was created by me and all work is original. The Chess AI is being developed with the help of various online tutorials and guides and most of the current posted work is a variation on other publically available projects. Pygame is not a package I am familiar with and this is a valuable learning experience. 






