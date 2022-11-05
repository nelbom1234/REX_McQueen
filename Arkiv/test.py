import time
from time import sleep
from turtle import right

import robot

arlo = robot.Robot()
leftForward = 64
rightForward = 66
leftTurn = 64
rightTurn = 64

def timer(x):
    start = time.time()
    end = start + x
    print(end)
    while time.time() < end:
        print(time.time())
        if arlo.read_front_ping_sensor() < 250:
            print(arlo.stop())
            print("something in front")
            print(arlo.go_diff(leftTurn, rightTurn, 1, 0))
            sleep(0.637)
            print(arlo.stop())
            
            sleep(0.041)
            print(arlo.go_diff(leftForward, rightForward, 1, 1))
            timer(2)
            print(arlo.stop())
            
            sleep(0.041)
            print(arlo.go_diff(leftTurn, rightTurn, 0, 1))
            sleep(0.637)
            print(arlo.stop())
            
            print(arlo.go_diff(leftForward, rightForward, 1, 1))
            timer(2)
            print(arlo.stop())
            
            sleep(0.041)
            print(arlo.go_diff(leftTurn, rightTurn, 0, 1))
            sleep(0.637)
            print(arlo.stop())
            
            print(arlo.go_diff(leftForward, rightForward, 1, 1))
            timer(2)
            print(arlo.stop())

        elif arlo.read_left_ping_sensor() < 100:
            print(arlo.stop())
            print("something in the left")
            print(arlo.go_diff(leftTurn, rightTurn, 1, 0))
            sleep(0.637)
            print(arlo.stop())
            
            sleep(0.041)
            print(arlo.go_diff(leftForward, rightForward, 1, 1))
            timer(2)
            print(arlo.stop())
            
            sleep(0.041)
            print(arlo.go_diff(leftTurn, rightTurn, 0, 1))
            sleep(0.637)
            print(arlo.stop())
            
            print(arlo.go_diff(leftForward, rightForward, 1, 1))
            timer(2)
            print(arlo.stop())
            
            sleep(0.041)
            print(arlo.go_diff(leftTurn, rightTurn, 0, 1))
            sleep(0.637)
            print(arlo.stop())
            
            print(arlo.go_diff(leftForward, rightForward, 1, 1))
            timer(2)
            print(arlo.stop())
            
        elif arlo.read_right_ping_sensor() < 100:
            print(arlo.stop())
            print("something in the right")
            print(arlo.go_diff(leftTurn, rightTurn, 0, 1))
            sleep(0.637)
            print(arlo.stop())
            
            sleep(0.041)
            print(arlo.go_diff(leftForward, rightForward, 1, 1))
            timer(2)
            print(arlo.stop())
            
            sleep(0.041)
            print(arlo.go_diff(leftTurn, rightTurn, 1, 0))
            sleep(0.637)
            print(arlo.stop())
            
            print(arlo.go_diff(leftForward, rightForward, 1, 1))
            timer(2)
            print(arlo.stop())
            
            sleep(0.041)
            print(arlo.go_diff(leftTurn, rightTurn, 1, 0))
            sleep(0.637)
            print(arlo.stop())
            
            print(arlo.go_diff(leftForward, rightForward, 1, 1))
            timer(2)
            print(arlo.stop())


print("Running ...")

leftSpeed = 64
rightSpeed = 66

arlo.go_diff(leftSpeed, rightSpeed, 1, 1)
timer(20)
print(arlo.stop())








  # request to read Front sonar ping sensor
print("Front sensor = ", arlo.read_front_ping_sensor())
sleep(0.041)


  # request to read Back sonar ping sensor
print("Back sensor = ", arlo.read_back_ping_sensor())
sleep(0.041)

  # request to read Right sonar ping sensor
print("Right sensor = ", arlo.read_right_ping_sensor())
sleep(0.041)

# request to read Left sonar ping sensor
print("Left sensor = ", arlo.read_left_ping_sensor())
sleep(0.041)



print("finished")





