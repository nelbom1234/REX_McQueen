from time import sleep

import robot
import random

random.randint(0, 9)

# Create a robot object and initialize
arlo = robot.Robot()

print("Running ...")


# send a go_diff command to drive forward
leftSpeed = 64
rightSpeed = 66

print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))

go=True
switch=0

while(go==True):
    if arlo.read_front_ping_sensor()<500:
        if switch==0:
            switch=1
            arlo.stop()
            print(arlo.read_front_ping_sensor)
            sleep(3)
            rand=random.randint(5, 15)/10
            print(arlo.go_diff(leftSpeed, rightSpeed, 1, 0))
            sleep(1.435*rand)
            print(arlo.stop())
            sleep(3)
            print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))
            switch=0

print("Finished")
