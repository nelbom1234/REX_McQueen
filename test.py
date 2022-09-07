from time import sleep
from turtle import right

import robot

arlo = robot.Robot()

print("Running ...")

leftSpeed = 66
rightSpeed = 66
print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))
sleep(3)
print(arlo.stop())
sleep(0.041)
print(arlo.go_diff(leftSpeed, rightSpeed, 0, 0))
sleep(3)
sleep(0.041)

print("finished")
