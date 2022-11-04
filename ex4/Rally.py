from turtle import right
import cv2
import particle
import camera
import numpy as np
import AuxFunctions
import time
from time import sleep
from timeit import default_timer as timer
import sys
import copy


# Flags
showGUI = True  # Whether or not to open GUI windows
onRobot = True # Whether or not we are running on the Arlo robot

def isRunningOnArlo():
    return onRobot
    
if isRunningOnArlo():
    # XXX: You need to change this path to point to where your robot.py file is located
    sys.path.append("/home/pi/Arlo/Robot/git/REX_McQueen")

try:
    import robot
    onRobot = True
except ImportError:
    print("selflocalize.py: robot module not present - forcing not running on Arlo!")
    onRobot = False





def initialize_particles(num_particles):
    particles = []
    for i in range(num_particles):
        # Random starting points. 
        p = particle.Particle(600.0*np.random.ranf() - 100.0, 600.0*np.random.ranf() - 250.0, np.mod(2.0*np.pi*np.random.ranf(), 2.0*np.pi), 1.0/num_particles)
        particles.append(p)

    return particles


# Main program #
try:
    if showGUI:
        # Open windows
        WIN_RF1 = "Robot view"
        cv2.namedWindow(WIN_RF1)
        cv2.moveWindow(WIN_RF1, 50, 50)

        WIN_World = "World view"
        cv2.namedWindow(WIN_World)
        cv2.moveWindow(WIN_World, 500, 50)
    

    # Initialize particles
    num_particles = 1200
    particles = initialize_particles(num_particles)

    est_pose = particle.estimate_pose(particles) # The estimate of the robots current pose

    # Initialize the robot (XXX: You do this)
    arlo = robot.Robot()
    # Allocate space for world map
    world = np.zeros((400,500,3), dtype=np.uint8)

    # Draw map
    AuxFunctions.draw_world(est_pose, particles, world)

    print("Opening and initializing camera")
    if isRunningOnArlo():
        cam = camera.Camera(0, 'arlo', useCaptureThread = True)
    else:
        cam = camera.Camera(0, 'macbookpro', useCaptureThread = True)
        
    print(est_pose.x,est_pose.y,est_pose.theta)
    est_pose, particles=AuxFunctions.LocalizeRobot(particles=particles, num_particles=num_particles,cam=cam,arlo=arlo,world=world)
    print(est_pose.x,est_pose.y,est_pose.theta)
    sleep(20)
  
finally: 
    # Make sure to clean up even if an exception occurred
    
    # Close all windows
    cv2.destroyAllWindows()

    # Clean-up capture thread
    cam.terminateCaptureThread()