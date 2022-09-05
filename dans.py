from time import sleep

import robot

# Create a robot object and initialize
arlo = robot.Robot()

print("Running ...")


# send a go_diff command to drive forward
leftSpeed = 100
rightSpeed = 100
i=1
while(i!=100):
    print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))
    sleep(0.1)
    print(arlo.stop())
    print(arlo.go_diff(leftSpeed, rightSpeed, 0, 0))
    sleep(0.1)
    print(arlo.stop())
    i=i+1

print("Finished")
