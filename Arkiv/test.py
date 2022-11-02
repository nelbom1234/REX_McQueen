from time import sleep
from turtle import right

import robot

arlo = robot.Robot()

print("Running ...")

leftSpeed = 64
rightSpeed = 66
print("driving")
arlo.go_diff(leftSpeed, rightSpeed, 1, 0)
print("sleeping")
sleep(3)
print("done")


b = tk.Button("q", command=self.pause)
def pause(self):
    if self.is_sleeping:
        self.pause()

self.is_sleeping = True
self.after(sleep_period, lambda: self.is_sleeping = False)
self.start_animation()


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





