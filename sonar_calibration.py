from time import sleep
from turtle import left

import robot

# Create a robot object and initialize
arlo = robot.Robot()

print("Running ...")

print(arlo.read_front_ping_sensor())
print(arlo.read_front_ping_sensor())

print("Finished")