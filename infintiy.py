from time import sleep

import robot

# Create a robot object and initialize
arlo = robot.Robot()

print("Running ...")

leftSpeed = 64
rightSpeed = 64
print(arlo.go_diff(leftSpeed, rightSpeed, 1, 0))

sleep(0.36)


for i in range(10):
  turnspeed = 2

  # send a go_diff command to drive forward
  leftSpeed = 64
  rightSpeed = 32
  print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))

  # Wait a bit while robot moves forward
  sleep(turnspeed)

  # send a stop command
  print(arlo.stop())

  sleep(1)

  leftSpeed = 32
  rightSpeed = 64
  # send a go_diff command to drive forward in a curve turning right

  print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))

  # Wait a bit while robot moves forward
  sleep(turnspeed)

  # send a stop command
  print(arlo.stop())
  sleep(1)

  # send a go_diff command to drive forward
  leftSpeed = 64
  rightSpeed = 32
  print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))

  # Wait a bit while robot moves forward
  sleep(turnspeed)

  # send a stop command
  print(arlo.stop())

  sleep(1)

  leftSpeed = 32
  rightSpeed = 64
  # send a go_diff command to drive forward in a curve turning right

  print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))

  # Wait a bit while robot moves forward
  sleep(turnspeed)

  # send a stop command
  print(arlo.stop())
  sleep(1)

print("Finished")