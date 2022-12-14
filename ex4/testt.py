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


# Flags
showGUI = True  # Whether or not to open GUI windows
onRobot = True # Whether or not we are running on the Arlo robot


def isRunningOnArlo():
    """Return True if we are running on Arlo, otherwise False.
      You can use this flag to switch the code from running on you laptop to Arlo - you need to do the programming here!
    """
    input1 = cv2.waitKey(10)
    if (input1 == 'l'):
        onRobot == False
    else:
        return onRobot

def timer(x):
    start = time.time()
    end = start + x
    print(end)
    while time.time() < end:
        print(time.time())
        if arlo.read_front_ping_sensor() < 250:
            print("something in front")
            break
        elif arlo.read_left_ping_sensor() < 150:
            print("something in the left")
            break
        elif arlo.read_right_ping_sensor() < 150:
            print("something in the right")
            break

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

# Landmarks.
# The robot knows the position of 2 landmarks. Their coordinates are in the unit centimeters [cm].
landmarkIDs = [1, 2, 3, 4]
landmarks = {
    1: (0.0, 0.0),  # Coordinates for landmark 1
    2: (0.0, 285.0),  # Coordinates for landmark 2
    3: (400.0, 0.0),  # Coordinates for landmark 3
    4: (400.0, 275.0) # Coordinates for landmark 4
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

    world[:] = CWHITE # Clear background to white

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

    # Driving parameters
    velocity = 0.0 # cm/sec
    angular_velocity = 0.0 # radians/sec

    leftForward = 64
    rightForward = 66
    leftTurn = 64
    rightTurn = 64

    # Initialize the robot (XXX: You do this)
    arlo = robot.Robot()
    # Allocate space for world map
    world = np.zeros((400,500,3), dtype=np.uint8)

    # Draw map
    draw_world(est_pose, particles, world)

    print("Opening and initializing camera")
    if isRunningOnArlo():
        cam = camera.Camera(0, 'arlo', useCaptureThread = True)
    else:
        cam = camera.Camera(0, 'macbookpro', useCaptureThread = True)

    fullTurn = 0
    fullTurnAmount = 0
    turns = 0
    Skip=0
    dist_mul = 20

    while True:

        # Move the robot according to user input (only for testing)
        action = cv2.waitKey(10)
        if action == ord('q'): # Quit
            break
    
        if not isRunningOnArlo():
      #  if action == ord('l'):
            if action == ord('w'): # Forward
                velocity += 4.0
                print("you did it")
            elif action == ord('x'): # Backwards
                velocity -= 4.0
            elif action == ord('s'): # Stop
                velocity = 0.0
                angular_velocity = 0.0
            elif action == ord('a'): # Left
                angular_velocity += 0.2
            elif action == ord('d'): # Right
                angular_velocity -= 0.2

        # Use motor controls to update particles
        # XXX: Make the robot drive
        # XXX: You do this
        turnsAmount=12
        speedMultiple=0.75
        fullTurnVal=2.9/speedMultiple
        if Skip<0:
            Skip=0

        #SKAL DREJE 360 GRADER
        if Skip<1 and fullTurnAmount!=1:
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
        else:
            x = est_pose.getX()
            y = est_pose.getY()
            theta = est_pose.getTheta()
            #x,y,theta = est_pose
            dvx = 30.0-x
            dvy = 30.0-y
            dvtheta = np.arctan(dvy/dvx)
            theta_deg = theta*57.29
            dvtheta_deg = dvtheta*57.29
            theta_diff = theta-dvtheta
            
            turns = theta_diff/(0.166*np.pi)
            print(f"pos: {x}, {y}")
            print(f"dvpos: {dvx}, {dvy}")
            print(f"theta: {theta}")
            print(f"dvtheta: {dvtheta}")
            print(f"theta_diff: {theta_diff}")
            print(f"turns: {turns}")


            if theta_diff < 0.0:
                if dvx < 0:
                    turns = turns - 5.5
                while -turns > 0.0:
                    if -turns > 1:
                        print(arlo.go_diff(leftTurn*speedMultiple, rightTurn*speedMultiple, 0, 1))
                        sleep(0.322)
                        print(arlo.stop())
                        sleep(0.1)
                        turns = turns + 1.0
                    else:
                        print(arlo.go_diff(leftTurn*speedMultiple, rightTurn*speedMultiple, 0, 1))
                        sleep(0.322*(-turns))
                        print(arlo.stop())
                        sleep(0.1)
                        turns = 0
            else:
                if dvx < 0:
                    turns = turns + 5.75
                while turns > 0.0:
                    if turns > 1.0:
                        print(arlo.go_diff(leftTurn*speedMultiple, rightTurn*speedMultiple, 1, 0))
                        sleep(0.322)
                        print(arlo.stop())
                        sleep(0.1)
                        turns = turns - 1.0
                    else:
                        print(arlo.go_diff(leftTurn*speedMultiple, rightTurn*speedMultiple, 1, 0))
                        sleep(0.322*turns)
                        print(arlo.stop())
                        sleep(0.1)
                        turns = 0
            dist = np.sqrt(dvx**2+dvy**2)
            print(arlo.go_diff(leftForward, rightForward, 1, 1))
            timer(3*(dist/120))
            print(arlo.stop())
            sleep(0.041)
            break
        # Fetch next frame
        colour = cam.get_next_frame()
        
        particle.add_uncertainty(particles, 5, 0.02*np.pi)

        # Detect objects
        objectIDs, dists, angles = cam.detect_aruco_objects(colour)
        monoObjects = [None, None, None, None]

        if Skip < 1 and fullTurnAmount != 5 and not isinstance(objectIDs, type(None)) and any(p < 5 for p in objectIDs):
            Skip = 0
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

        if showGUI:
            # Draw map
            draw_world(est_pose, particles, world)
    
            # Show frame
            cv2.imshow(WIN_RF1, colour)

            # Show world
            cv2.imshow(WIN_World, world)
    
  
finally: 
    # Make sure to clean up even if an exception occurred
    
    # Close all windows
    cv2.destroyAllWindows()

    # Clean-up capture thread
    cam.terminateCaptureThread()
