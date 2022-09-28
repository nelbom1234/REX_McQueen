import string
from time import sleep
from turtle import left
import camera

import robot

# Create a robot object and initialize
arlo = robot.Robot()
#camera1 = camera.Camera(camidx=1, robottype='arlo')

print("Running ...")


# send a go_diff command to drive forward
leftSpeed = 64
rightSpeed = 66

if (__name__=='__main__'):
    print("Opening and initializing camera")
    
    cam = camera.Camera(0, 'macbookpro', useCaptureThread = True)
    #cam = Camera(0, 'macbookpro', useCaptureThread = False)
    #cam = Camera(0, 'arlo', useCaptureThread = True)
    
    # Open a window
    WIN_RF1 = "Camera view"
    camera.cv2.namedWindow(WIN_RF1)
    camera.cv2.moveWindow(WIN_RF1, 50, 50)
        
    #WIN_RF3 = "Camera view - gray"
    #cv2.namedWindow(WIN_RF3)
    #cv2.moveWindow(WIN_RF3, 550, 50)
    
    while True:
        
        action = camera.cv2.waitKey(10)
        if action == ord('q'):  # Quit
            break
    
        # Fetch next frame
        #colour = cam.get_colour()
        #colour = cam.get_next_frame()
        sleep(1)
        colour = cam.get_next_frame()
        
        # Detect objectscamera
        objectType, distance, angle, colourProb = cam.get_object(colour)
        if objectType != 'none':
            print("Object type = ", objectType, ", distance = ", distance, ", angle = ", angle, ", colourProb = ", colourProb)
            

        # Draw detected pattern
        #cam.draw_object(colour)

        IDs, dists, angles = cam.detect_aruco_objects(colour)
        if not isinstance(IDs, type(None)):
            for i in range(len(IDs)):
                print("Object ID = ", IDs[i], ", Distance = ", dists[i], ", angles = ", angles[i])
                #Get object straight in front of camera
                if dists[i]>0.5:
                    kørtilboks=dists[i]*0.05
                    arlo.go_diff(leftSpeed, rightSpeed, 1, 1)
                    sleep(kørtilboks)
                    arlo.stop()
                print("Tæt nok på")
                
        else:
            print("No aruco objects detected")
            # Look for object by turning
            arlo.stop()
            arlo.go_diff(leftSpeed, rightSpeed, 0, 1)
            sleep(0.2)
            arlo.stop()
        # Draw detected objects
        cam.draw_aruco_objects(colour)
        # Show frames
        camera.cv2.imshow(WIN_RF1, colour)
        # Show frames
        #camera.cv2.imshow(WIN_RF3, gray)
        
    # Close all windows
    camera.cv2.destroyAllWindows()

    # Clean-up capture thread
    cam.terminateCaptureThread()

#print(camera1.detect_aruco_objects(camera1.get_next_frame()))

print("Finished")
