from time import sleep
from pynput import keyboard
from pynput.keyboard import Listener, Key

import robot

# Create a robot object and initialize
arlo = robot.Robot()

print("Running ...")


# send a go_diff command to drive forward
leftSpeed = 100
rightSpeed = 100
print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))

# Wait a bit while robot moves forward
sleep(1)

# send a stop command
print(arlo.stop())

print("Så kører vi fuckhoveder")

def on_press(key):
    if key == Key.up:  # If space was pressed, write a space
        print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))
    elif key == Key.down:  # If enter was pressed, write a new line
        print(arlo.go_diff(leftSpeed, rightSpeed, 0, 0))
    elif key == Key.left:  # If tab was pressed, write a tab
        print(arlo.go_diff(leftSpeed, rightSpeed, 0, 1))
    elif key == Key.right:
        print(arlo.go_diff(leftSpeed, rightSpeed, 1, 0))
    elif key == Key.space:
        print("Status:")
        print("Front sensor")
        print(arlo.read_front_ping_sensor)
        nuts=arlo.read_front_ping_sensor
        if nuts<100:
            print("go back")
            print(arlo.go_diff(leftSpeed, rightSpeed, 0, 0))
    elif key == Key.escape:
        exit()

def on_release(key):
    if key == Key.up:  # If space was pressed, write a space
        print(arlo.stop())
    elif key == Key.down:  # If enter was pressed, write a new line
        print(arlo.stop())
    elif key == Key.left:  # If tab was pressed, write a tab
        print(arlo.stop())
    elif key == Key.right:
        print(arlo.stop())


with Listener(on_press=on_press, on_release=on_release) as listener:  # Setup the listener
    listener.join()  # Join the thread to the main thread



print("Finished")
