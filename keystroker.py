from time import sleep
from turtle import right
from pynput.keyboard import Listener

import robot

# Create a robot object and initialize
arlo = robot.Robot()

print("Running ...")


# send a go_diff command to drive forward
leftSpeed = 64
rightSpeed = 64
print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))

# Wait a bit while robot moves forward
sleep(3)

# send a stop command
print(arlo.stop())

from pynput.keyboard import Listener, Key

filename = "key_log.txt"  # The file to write characters to

print("Så kører vi fuckhoveder")

def on_press(key):
    if key == Key.up:  # If space was pressed, write a space
        print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))
    elif key == Key.down:  # If enter was pressed, write a new line
        print(arlo.go_diff(leftSpeed, rightSpeed, 0, 0))
    elif key == Key.left:  # If tab was pressed, write a tab
        print(arlo.go_diff(-leftSpeed, rightSpeed, 1, 1))
    elif key == Key.right:
        print(arlo.go_diff(leftSpeed, -rightSpeed, 1, 1))




with Listener(on_press=on_press) as listener:  # Setup the listener
    listener.join()  # Join the thread to the main thread



print("Finished")
