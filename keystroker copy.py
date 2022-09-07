from multiprocessing.resource_sharer import stop
from time import sleep
from pynput import keyboard

print("Running ...")

from pynput.keyboard import Listener, Key

def on_press(key):
    if key == Key.up:
        print("down")
    elif key == Key.down:
        print("down")
    elif key == Key.left:
        print("down")
    elif key == Key.right:
        print("down")
    elif key == Key.escape:
        exit()

def on_release(key):
    if key == Key.up:
        print("up")
    elif key == Key.down:
        print("up")
    elif key == Key.left:
        print("up")
    elif key == Key.right:
        print("up")


with Listener(on_press=on_press, on_release=on_release) as listener:  # Setup the listener
    listener.join()  # Join the thread to the main thread



print("Finished")
