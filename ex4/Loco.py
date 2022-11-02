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

def Localize(particles):
    # Use motor controls to update particles
    # XXX: Make the robot drive
    # XXX: You do this
    turnsAmount=12
    speedMultiple=0.75
    fullTurnVal=2.9/speedMultiple
    if Skip<0:
        Skip=0

    #SKAL DREJE 360 GRADER
    if Skip<1 and fullTurnAmount!=5:
        print(arlo.go_diff(leftTurn*speedMultiple, rightTurn*speedMultiple, 1, 0))
        sleep(fullTurnVal/turnsAmount)
        for p in particles:
            particle.move_particle(p, 0, 0, -(2*np.pi)/turnsAmount)
            #print (p.getTheta())
        print(arlo.stop())
        sleep(1)
        particle.add_uncertainty(particles, 10, 0.03*np.pi)
        fullTurn += 1
        if turnsAmount < fullTurn:
            fullTurnAmount += 1
            fullTurn=0

    # Fetch next frame
    colour = cam.get_next_frame()
    
    particle.add_uncertainty(particles, 5, 0.02*np.pi)

    # Detect objects
    objectIDs, dists, angles = cam.detect_aruco_objects(colour)
    monoObjects = [None, None, None, None]

    if Skip < 1 and fullTurnAmount != 5 and not isinstance(objectIDs, type(None)) and any(p < 5 for p in objectIDs):
        Skip = 5
    Skip-=1

    if not isinstance(objectIDs, type(None)) and any(p < 5 for p in objectIDs):
        # List detected objects
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
            print(sum_of_weights)
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

    return est_pose

if showGUI:
    # Draw map
    draw_world(est_pose, particles, world)

    # Show frame
    cv2.imshow(WIN_RF1, colour)

    # Show world
    cv2.imshow(WIN_World, world)