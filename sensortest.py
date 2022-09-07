from time import sleep

import robot

# Create a robot object and initialize
arlo = robot.Robot()

print("Running ...")

# send a go_diff command to drive forward
leftSpeed = 64
rightSpeed = 64


while (true):
    print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))
    # request to read Front sonar ping sensor
    
    front = arlo.read_front_ping_sensor()
    print("Front sensor = ", arlo.read_front_ping_sensor())
    sleep(0.041)

    back = arlo.read_back_ping_sensor()
    # request to read Back sonar ping sensor
    print("Back sensor = ", arlo.read_back_ping_sensor())
    sleep(0.041)


    # request to read Right sonar ping sensor
    print("Right sensor = ", arlo.read_right_ping_sensor())
    sleep(0.041)

    # request to read Left sonar ping sensor
    print("Left sensor = ", arlo.read_left_ping_sensor())
    sleep(0.041)
    
    if (front < 1000):
        leftSpeed = 64
        rightSpeed = 64
        print(arlo.go_diff(leftSpeed, rightSpeed, 0, 0))
        sleep(3)

    elif (back < 1000):
        leftSpeed = 64
        rightSpeed = 64
        print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))
        sleep(3)
    else 
        print(arlo.stop())



print("Finished")
