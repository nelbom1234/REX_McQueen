import string
from time import sleep
from turtle import left

import robot

# Create a robot object and initialize
arlo = robot.Robot()

print("Running ...")


# send a go_diff command to drive forward
leftSpeed = 64
rightSpeed = 66

leftForward = 64
rightForward = 66
leftTurn = 64
rightTurn = 64

print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))

#go down



def square(corners=int,sizeofsquare=float,LeftOrRight=string):

    if LeftOrRight=="left":
        leftwheel=0
        rightwheel=1
    elif LeftOrRight=="right":
        leftwheel=1
        rightwheel=0
    else:
        leftwheel=1
        rightwheel=0

    for i in range(corners):
        print(arlo.go_diff(leftTurn, rightTurn, leftwheel, rightwheel))
        sleep(0.637)
        print(arlo.stop())
        sleep(0.041)

        print(arlo.go_diff(leftForward, rightForward, 1, 1))
        sleep(sizeofsquare)
        print(arlo.stop())
        sleep(0.041)

        

go=True
switch=0

while(go==True):
    if arlo.read_front_ping_sensor()<400 or arlo.read_left_ping_sensor()<250:
        arlo.stop()
        print(arlo.read_front_ping_sensor)
        sleep(1)
        square(1,2,"right")
        square(2,2,"left")
        square(1,0,"right")
        print(arlo.stop())
        sleep(1)
        print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))
    if arlo.read_right_ping_sensor()<250:
        arlo.stop()
        print(arlo.read_front_ping_sensor)
        sleep(1)
        square(1,2,"left")
        square(2,2,"right")
        square(1,0,"left")
        print(arlo.stop())
        sleep(1)
        print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))

print("Finished")
