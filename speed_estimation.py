from time import sleep

import robot

arlo = robot.Robot()

print("Running ...")

leftSpeed = 64
rightSpeed = 66

print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))
sleep(3)
print(arlo.stop())
sleep(0.041)

print("finished")