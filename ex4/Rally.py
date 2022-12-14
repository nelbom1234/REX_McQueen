from turtle import right
import cv2
import particle
import camera
import numpy as np
import time
import AuxFunctions
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

# Some color constants in BGR format
CRED = (0, 0, 255)
CGREEN = (0, 255, 0)
CBLUE = (255, 0, 0)
CCYAN = (255, 255, 0)
CYELLOW = (0, 255, 255)
CMAGENTA = (255, 0, 255)
CWHITE = (255, 255, 255)
CBLACK = (0, 0, 0)

def initialize_particles(num_particles):
    particles = []
    for i in range(num_particles):
        # Random starting points. 
        p = particle.Particle(600.0*np.random.ranf() - 100.0, 600.0*np.random.ranf() - 250.0, np.mod(2.0*np.pi*np.random.ranf(), 2.0*np.pi), 1.0/num_particles)
        particles.append(p)

    return particles

def timer(x):
    start = time.time()
    end = start + x
    while time.time() < end:
        if arlo.read_front_ping_sensor() < 250:
            print("something in front")
            break
        elif arlo.read_left_ping_sensor() < 150:
            print("something in the left")
            break
        elif arlo.read_right_ping_sensor() < 150:
            print("something in the right")
            break

def drive_to_coordinates(x_end, y_end, est_pose, time_multiple):
    x = est_pose.getX()
    y = est_pose.getX()
    theta = est_pose.getTheta()
    dvx = x_end-x
    dvy = y_end-y
    dvtheta = np.arctan(dvy/dvx)
    theta_diff = theta-dvtheta
    speedMultiple=0.75
    leftTurn=64
    rightTurn=64 #64
    leftForward=64
    rightForward=66
            
    turns = theta_diff/(0.205*np.pi)
    dist = np.sqrt(dvx**2+dvy**2)

    print("===========")
    print("Robot at ({}, {})".format(x, y))
    print("Robot heading {}".format(theta))
    print("Robot moving towards ({}, {})".format(x_end, y_end))
    print("Robot heading towards {}".format(dvtheta))
    print("Distance to destination: {}".format(dist))
    print("===========")

    if theta_diff < 0.0:
        if dvx < 0:
            turns = turns - 3.5
        if dvy < 0:
            turns = turns - 1.5
        while -turns > 0.0:
            if -turns > 1:
                arlo.go_diff(leftTurn*speedMultiple, rightTurn*speedMultiple, 0, 1)
                sleep(0.322)
                arlo.stop()
                sleep(0.1)
                turns = turns + 1.0
            else:
                arlo.go_diff(leftTurn*speedMultiple, rightTurn*speedMultiple, 0, 1)
                sleep(0.322*(-turns))
                arlo.stop()
                sleep(0.1)
                turns = 0
    else:
        if dvx < 0:
            turns = turns + 3.5
        if dvy < 0:
            turns = turns + 1.5
        while turns > 0.0:
            if turns > 1.0:
                arlo.go_diff(leftTurn*speedMultiple, rightTurn*speedMultiple, 1, 0)
                sleep(0.322)
                arlo.stop()
                sleep(0.1)
                turns = turns - 1.0
            else:
                arlo.go_diff(leftTurn*speedMultiple, rightTurn*speedMultiple, 1, 0)
                sleep(0.322*turns)
                print(arlo.stop())
                sleep(0.1)
                turns = 0

    
    
    arlo.go_diff(leftForward, rightForward, 1, 1)
    timer((3.2*(dist/120))*time_multiple)
    arlo.stop()
    sleep(0.041)


est_pose = None

def DrivingPlan(ListOfCoordinates):
    i = 0
    est_pose=AuxFunctions.LocalizeRobot(num_particles=num_particles,cam=cam,arlo=arlo,world=world)
    while i < len(ListOfCoordinates):
        print(f"driving to {i+1}")
        drive_to_coordinates(ListOfCoordinates[i][0], ListOfCoordinates[i][1], est_pose,time_multiple=0.5)
        est_pose=AuxFunctions.LocalizeRobot(num_particles=num_particles,cam=cam,arlo=arlo,world=world)
        drive_to_coordinates(ListOfCoordinates[i][0], ListOfCoordinates[i][1], est_pose,time_multiple=1.0)
        est_pose=AuxFunctions.LocalizeRobot(num_particles=num_particles,cam=cam,arlo=arlo,world=world)
        #Check if est_pose is close to ListOfCoordinates[i]
        if est_pose.getX() < ListOfCoordinates[i][0]+50 and est_pose.getX() > ListOfCoordinates[i][0]-50 and est_pose.getY() < ListOfCoordinates[i][1]+50 and est_pose.getY() > ListOfCoordinates[i][1]-50:
            print("Reached the destination")
            i += 1
        else:
            print("not reached destination")
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
    
    ListOfCoordinates = [[20, 20], [20, 280], [380, 20], [380, 280], [20, 20]]

    DrivingPlan(ListOfCoordinates)

    #print(est_pose.x,est_pose.y,est_pose.theta)
    #est_pose, particles=AuxFunctions.LocalizeRobot(num_particles=num_particles,cam=cam,arlo=arlo,world=world)
    #print(f"est_pose.x: {est_pose.getX()},est_pose.y: {est_pose.getY()},est_pose.theta: {est_pose.getTheta()}")
    #drive_to_coordinates(30, 30, est_pose)
    #est_pose, particles=AuxFunctions.LocalizeRobot(num_particles=num_particles,cam=cam,arlo=arlo,world=world)
    #print(f"est_pose.x: {est_pose.getX()},est_pose.y: {est_pose.getY()},est_pose.theta: {est_pose.getTheta()}")
    #drive_to_coordinates(30, 250, est_pose)
    #est_pose, particles=AuxFunctions.LocalizeRobot(num_particles=num_particles,cam=cam,arlo=arlo,world=world)
    #print(f"est_pose.x: {est_pose.getX()},est_pose.y: {est_pose.getY()},est_pose.theta: {est_pose.getTheta()}")
    #drive_to_coordinates(370, 30, est_pose)
    #est_pose, particles=AuxFunctions.LocalizeRobot(num_particles=num_particles,cam=cam,arlo=arlo,world=world)
    #print(f"est_pose.x: {est_pose.getX()},est_pose.y: {est_pose.getY()},est_pose.theta: {est_pose.getTheta()}")
    #drive_to_coordinates(370, 250, est_pose)
    #est_pose, particles=AuxFunctions.LocalizeRobot(num_particles=num_particles,cam=cam,arlo=arlo,world=world)
    #print(f"est_pose.x: {est_pose.getX()},est_pose.y: {est_pose.getY()},est_pose.theta: {est_pose.getTheta()}")
    #drive_to_coordinates(30, 30, est_pose)
    


finally: 
    # Make sure to clean up even if an exception occurred
    
    # Close all windows
    cv2.destroyAllWindows()

    # Clean-up capture thread
    cam.terminateCaptureThread()
