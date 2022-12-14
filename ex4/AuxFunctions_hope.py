from turtle import right
import cv2
import particle
import camera
import numpy as np
import time
from time import sleep
from timeit import default_timer as timer
import sys
import copy

# Some color constants in BGR format
CRED = (0, 0, 255)
CGREEN = (0, 255, 0)
CBLUE = (255, 0, 0)
CCYAN = (255, 255, 0)
CYELLOW = (0, 255, 255)
CMAGENTA = (255, 0, 255)
CWHITE = (255, 255, 255)
CBLACK = (0, 0, 0)

# Landmarks.
# The robot knows the position of 2 landmarks. Their coordinates are in the unit centimeters [cm].
landmarkIDs = [1, 2, 3, 4]
landmarks = {
    1: (0.0, 0.0),  # Coordinates for landmark 1
    2: (0.0, 300.0),  # Coordinates for landmark 2
    3: (400.0, 0.0),  # Coordinates for landmark 3
    4: (400.0, 300.0) # Coordinates for landmark 4
}
landmark_colors = [CRED, CGREEN, CBLUE, CYELLOW] # Colors used when drawing the landmarks

def jet(x):
    """Colour map for drawing particles. This function determines the colour of 
    a particle from its weight."""
    r = (x >= 3.0/8.0 and x < 5.0/8.0) * (4.0 * x - 3.0/2.0) + (x >= 5.0/8.0 and x < 7.0/8.0) + (x >= 7.0/8.0) * (-4.0 * x + 9.0/2.0)
    g = (x >= 1.0/8.0 and x < 3.0/8.0) * (4.0 * x - 1.0/2.0) + (x >= 3.0/8.0 and x < 5.0/8.0) + (x >= 5.0/8.0 and x < 7.0/8.0) * (-4.0 * x + 7.0/2.0)
    b = (x < 1.0/8.0) * (4.0 * x + 1.0/2.0) + (x >= 1.0/8.0 and x < 3.0/8.0) + (x >= 3.0/8.0 and x < 5.0/8.0) * (-4.0 * x + 5.0/2.0)

    return (255.0*r, 255.0*g, 255.0*b)

def draw_world(est_pose, particles, world):
    """Visualization.
    This functions draws robots position in the world coordinate system."""

    # Fix the origin of the coordinate system
    offsetX = 50
    offsetY = 50

    # Constant needed for transforming from world coordinates to screen coordinates (flip the y-axis)
    ymax = world.shape[0]
    
    #do 
    #do
    #do
    world[:] = CBLACK # Clear background to white 
    # do
    
    # Find largest weight
    max_weight = 0
    for particle in particles:
        max_weight = max(max_weight, particle.getWeight())

    # Draw particles
    for particle in particles:
        x = int(particle.getX() + offsetX)
        y = ymax - (int(particle.getY() + offsetY))
        colour = jet(particle.getWeight() / max_weight)
        cv2.circle(world, (x,y), 2, colour, 2)
        b = (int(particle.getX() + 15.0*np.cos(particle.getTheta()))+offsetX, 
                                     ymax - (int(particle.getY() + 15.0*np.sin(particle.getTheta()))+offsetY))
        cv2.line(world, (x,y), b, colour, 2)

    # Draw landmarks
    for i in range(len(landmarkIDs)):
        ID = landmarkIDs[i]
        lm = (int(landmarks[ID][0] + offsetX), int(ymax - (landmarks[ID][1] + offsetY)))
        cv2.circle(world, lm, 5, landmark_colors[i], 2)

    # Draw estimated robot pose
    a = (int(est_pose.getX())+offsetX, ymax-(int(est_pose.getY())+offsetY))
    b = (int(est_pose.getX() + 15.0*np.cos(est_pose.getTheta()))+offsetX, 
                                 ymax-(int(est_pose.getY() + 15.0*np.sin(est_pose.getTheta()))+offsetY))
    cv2.circle(world, a, 5, CMAGENTA, 2)
    cv2.line(world, a, b, CMAGENTA, 2)

def initialize_particles(num_particles):
    particles = []
    for i in range(num_particles):
        # Random starting points. 
        p = particle.Particle(600.0*np.random.ranf() - 100.0, 600.0*np.random.ranf() - 250.0, np.mod(2.0*np.pi*np.random.ranf(), 2.0*np.pi), 1.0/num_particles)
        particles.append(p)

    return particles

def LocalizeRobot(num_particles,cam,arlo,world,goal):
    particles = initialize_particles(num_particles)

    fullTurn = 0
    fullTurnAmount = 0
    turns = 0
    dist_mul = 20
    WIN_RF1 = "Robot view"
    WIN_World = "World view"
    real_goal = goal

    while True:
        # Move the robot according to user input (only for testing)
        action = cv2.waitKey(10)
        if action == ord('q'): # Quit
            break  
            
        turnsAmount=12
        speedMultiple=0.75
        fullTurnVal=2.9/speedMultiple

        #SKAL DREJE 360 GRADER
        if fullTurnAmount!=5:
            arlo.go_diff(64*speedMultiple, 64*speedMultiple, 1, 0)
            sleep(fullTurnVal/turnsAmount)
                #print (p.getTheta())
            arlo.stop()
            sleep(0.100)
            for p in particles:
                particle.move_particle(p, 0, 0, -(2*np.pi)/turnsAmount)
            particle.add_uncertainty(particles, 10, 0.03*np.pi)
            fullTurn += 1
            if turnsAmount < fullTurn:
                print("Finished full turn")

                return est_pose

        # Fetch next frame
        colour = cam.get_next_frame()
        
        particle.add_uncertainty(particles, 5, 0.02*np.pi)

        # Detect objects
        objectIDs, dists, angles = cam.detect_aruco_objects(colour)
        monoObjects = [None, None, None, None]

        if not isinstance(objectIDs, type(None)) and any(p < 5 for p in objectIDs):
            # List detected objects
            if real_goal == 5:
                real_goal = 1
            if any(p == real_goal for p in objectIDs):
                return None
            else:
                for i in range(len(objectIDs)):
                    print("Object ID = ", objectIDs[i], ", Distance = ", dists[i]+dist_mul, ", angle = ", angles[i])
                    # XXX: Do something for each detected object - remember, the same ID may appear several times
                    if objectIDs[i] == 1:
                        if monoObjects[0] == None:
                            monoObjects[0] = (dists[i]+dist_mul, angles[i])
                        elif monoObjects[0][0] < dists[i]+dist_mul:
                            monoObjects[0] = (dists[i]+dist_mul, angles[i])
                    elif objectIDs[i] == 2:
                        if monoObjects[1] == None:
                            monoObjects[1] = (dists[i]+dist_mul, angles[i])
                        elif monoObjects[1][0] < dists[i]+dist_mul:
                            monoObjects[1] = (dists[i]+dist_mul, angles[i])
                    elif objectIDs[i] == 3:
                        if monoObjects[2] == None:
                            monoObjects[2] = (dists[i]+dist_mul, angles[i])
                        elif monoObjects[2][0] < dists[i]+dist_mul:
                            monoObjects[2] = (dists[i]+dist_mul, angles[i])
                    elif objectIDs[i] == 4:
                        if monoObjects[3] == None:
                            monoObjects[3] = (dists[i]+dist_mul, angles[i])
                        elif monoObjects[3][0] < dists[i]+dist_mul:
                            monoObjects[3] = (dists[i]+dist_mul, angles[i])
                
                

            if not all(p == None for p in monoObjects):
            # Compute particle weights
            # XXX: You do this
                sigma_dist = 10
                sigma_angle = 0.05
                sum_of_weights = 0
                for p in particles:
                    p.setWeight(1)
                    for i in range(len(monoObjects)):
                        if monoObjects[i] != None:
                            d = np.sqrt((landmarks[i+1][0] - p.getX())**2 + (landmarks[i+1][1]-p.getY())**2)
                            dist_w = 1/(np.sqrt(2*np.pi*sigma_dist**2))*np.exp(-((d-monoObjects[i][0])**2)/(2*sigma_dist**2))
                            e_l = [(landmarks[i+1][0] - p.getX())/d, (landmarks[i+1][1]-p.getY())/d]
                            #e_theta = [np.cos(monoObjects[i][1]), np.sin(monoObjects[i][1])]
                            e_theta = [np.cos(p.getTheta()), np.sin(p.getTheta())]
                            #e_hat_theta = [-np.sin(monoObjects[i][1]), np.cos(monoObjects[i][1])]
                            e_hat_theta = [-np.sin(p.getTheta()), np.cos(p.getTheta())]
                            phi = np.sign(e_l[0]*e_hat_theta[0]+e_l[1]*e_hat_theta[1])*np.arccos(e_l[0]*e_theta[0]+e_l[1]*e_theta[1])
                            angle_w = 1/(np.sqrt(2*np.pi*sigma_angle**2))*np.exp(-(((monoObjects[i][1]-(phi))**2)/(2*sigma_angle**2)))
                            #print("dist_w2: {:.2f}".format(dist_w))
                            p.setWeight(p.getWeight()*dist_w * angle_w)
                    sum_of_weights += p.getWeight()
                if sum_of_weights > 10**(-120):
                    for p in particles:           
                        p.setWeight((p.getWeight()/sum_of_weights))
                else:
                    for p in particles:
                        p.setWeight(1/num_particles)
                
                #Resample particles using numpy
                #Normalize weights

                #Resampling
                #XXX: You do this
                new_particles = []
                for i in range(num_particles):
                  r = np.random.ranf()
                  sum_of_weights = 0
                  for p in particles:
                      sum_of_weights += p.getWeight()
                      if sum_of_weights >= r:
                          new_particles.append(copy.copy(p))
                          break
                particles = new_particles
                

            # Draw detected objects
            cam.draw_aruco_objects(colour)
        #else:
             #No observation - reset weights to uniform distribution
        #    for p in particles:
        #        p.setWeight(1.0/num_particles)


        est_pose = particle.estimate_pose(particles) # The estimate of the robots current pose

        # Draw map
        draw_world(est_pose, particles, world)

        # Show frame
        cv2.imshow(WIN_RF1, colour)

        # Show world
        cv2.imshow(WIN_World, world)

leftForward = 64
rightForward = 66
leftTurn = 64
rightTurn = 64

def Avoid_to_the_Front(arlo):
    print(arlo.go_diff(leftTurn, rightTurn, 1, 0))
    sleep(0.637)
    print(arlo.stop())

    sleep(0.041)
    print(arlo.go_diff(leftForward, rightForward, 1, 1))
    sleep(1.5)
    print(arlo.stop())

    sleep(0.041)
    print(arlo.go_diff(leftTurn, rightTurn, 0, 1))
    sleep(0.637)
    print(arlo.stop())

    print(arlo.go_diff(leftForward, rightForward, 1, 1))
    timer(2,arlo)
    print(arlo.stop())

    sleep(0.041)
    print(arlo.go_diff(leftTurn, rightTurn, 0, 1))
    sleep(0.637)
    print(arlo.stop())

    print(arlo.go_diff(leftForward, rightForward, 1, 1))
    timer(1.5,arlo)
    print(arlo.stop())
    
    sleep(0.041)
    print(arlo.go_diff(leftTurn, rightTurn, 1, 0))
    sleep(0.637)
    print(arlo.stop())

def Avoid_to_the_Right(arlo):
    print(arlo.go_diff(leftTurn, rightTurn, 1, 0))
    sleep(0.637)
    print(arlo.stop())

    sleep(0.041)
    print(arlo.go_diff(leftForward, rightForward, 1, 1))
    sleep(0.5)
    print(arlo.stop())

    sleep(0.041)
    print(arlo.go_diff(leftTurn, rightTurn, 0, 1))
    sleep(0.637)
    print(arlo.stop())

    print(arlo.go_diff(leftForward, rightForward, 1, 1))
    timer(2,arlo)
    print(arlo.stop())

    sleep(0.041)
    print(arlo.go_diff(leftTurn, rightTurn, 0, 1))
    sleep(0.637)
    print(arlo.stop())

    print(arlo.go_diff(leftForward, rightForward, 1, 1))
    timer(0.5,arlo)
    print(arlo.stop())
    
    sleep(0.041)
    print(arlo.go_diff(leftTurn, rightTurn, 1, 0))
    sleep(0.637)
    print(arlo.stop())

def Avoid_to_the_left(arlo):
    print(arlo.stop())
    print("something in the right")
    print(arlo.go_diff(leftTurn, rightTurn, 0, 1))
    sleep(0.637)
    print(arlo.stop())

    sleep(0.041)
    print(arlo.go_diff(leftForward, rightForward, 1, 1))
    sleep(0.5)
    print(arlo.stop())

    sleep(0.041)
    print(arlo.go_diff(leftTurn, rightTurn, 1, 0))
    sleep(0.637)
    print(arlo.stop())

    print(arlo.go_diff(leftForward, rightForward, 1, 1))
    timer(2,arlo)
    print(arlo.stop())

    sleep(0.041)
    print(arlo.go_diff(leftTurn, rightTurn, 1, 0))
    sleep(0.637)
    print(arlo.stop())

    print(arlo.go_diff(leftForward, rightForward, 1, 1))
    timer(0.5,arlo)
    print(arlo.stop())
    
    sleep(0.041)
    print(arlo.go_diff(leftTurn, rightTurn, 0, 1))
    sleep(0.637)
    print(arlo.stop())

def timer(x,arlo):
    start = time.time()
    end = start + x
    while time.time() < end:
        if arlo.read_front_ping_sensor() < 250:
            print(arlo.stop())
            print("something in front")
            Avoid_to_the_Front(arlo=arlo)

        elif arlo.read_left_ping_sensor() < 100:
            print(arlo.stop())
            print("something in the left")
            Avoid_to_the_Right(arlo=arlo)
            
        elif arlo.read_right_ping_sensor() < 150:
            print(arlo.stop())
            print("something in the right")
            Avoid_to_the_left(arlo=arlo)