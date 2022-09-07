from time import sleep

import robot

arlo = robot.Robot()

print("Running ...")

leftForward = 64
rightForward = 66
leftTurn = 64
rightTurn = 64


for i in range(4):

    print(arlo.go_diff(leftForward, rightForward, 1, 1))
    sleep(3)
    print(arlo.stop())
    sleep(0.041)

    print(arlo.go_diff(leftTurn, rightTurn, 1, 0))
    sleep(0.10)
    print(arlo.stop())
    sleep(0.041)

print("finished")
