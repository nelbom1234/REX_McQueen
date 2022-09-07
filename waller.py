from time import sleep

import robot

# Create a robot object and initialize
arlo = robot.Robot()

print("Running ...")


# send a go_diff command to drive forward
leftSpeed = 64
rightSpeed = 63

print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))

go=True

while(go==True):
    if arlo.read_front_ping_sensor()<500:
        arlo.stop()
        arlo.read_front_ping_sensor

print("Finished")
