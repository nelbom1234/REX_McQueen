from time import sleep
from turtle import right

import robot

arlo = robot.Robot()

print("Running ...")

leftSpeed = 64
rightSpeed = 66
print("driving")
arlo.go_diff(leftSpeed, rightSpeed, 1, 1)
print("sleeping")
sleep(3)
print("done")

print("finished")





