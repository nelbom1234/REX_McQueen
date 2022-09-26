import string
from time import sleep
from turtle import left
import camera

import robot

# Create a robot object and initialize
arlo = robot.Robot()
camera1 = camera.Camera(camidx=1)

print("Running ...")


# send a go_diff command to drive forward
leftSpeed = 64
rightSpeed = 66

leftForward = 64
rightForward = 66
leftTurn = 64
rightTurn = 64

print(camera1.detect_aruco_objects(camera1.get_next_frame()))

print("Finished")