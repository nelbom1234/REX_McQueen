import time
from time import sleep
from turtle import right

import robot

arlo = robot.Robot()

def timer(x):
    hello = True
    start = time.time()
    end = start + (x*1000)
    print(end)
    while time.time() < end:
        print(time.time())
        if arlo.read_front_ping_sensor() < 50:
            print("i am breaking")
            break
            
        
    
    
    #while hello==True:
     #   if time.time() > end:
      #      hello = False
       # elif arlo.read_front_ping_sensor() < 50:
        #    hello = False


print("Running ...")

leftSpeed = 64
rightSpeed = 66

arlo.go_diff(leftSpeed, rightSpeed, 1, 0)
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





