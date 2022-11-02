from time import sleep
from turtle import right

import robot

arlo = robot.Robot()
hello = True
def timer(x):
    start = time.time()
    end = start + (x*1000)
    while hello==True:
        if time.time() == end:
            hello = False
        elif arlo.read_front_ping_sensor() < 50:
            hello = False
        else:
            Print("going")


print("Running ...")

leftSpeed = 64
rightSpeed = 66
arlo.go_diff(leftSpeed, rightSpeed, 1, 0)
timer(20)







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





