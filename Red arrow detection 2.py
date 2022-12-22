# detcts red arrow in the camera feed and prints the angle of arrow with the vertical axis
import cv2 as cv
import numpy as np
import math


def initialize():
    global frameWidth
    frameWidth = 640
    global frameHeight
    frameHeight = 480

    cap.set(3, frameWidth) #sets width of frame as frameWidth(640)
    cap.set(4, frameHeight) #sets height of frame as frameHeight(480)
    cap.set(10,150) #brightness level

def findAngle(X1,y1,X2,y2):
    
    Y1 = max(y1,y2) #needed for applying formula
    Y2 = min(y1,y2) #needed for applying formula

    angRadians = math.acos((Y1-Y2)/((((X1-X2)**2)+((Y1-Y2)**2))**0.5)) #mathematical formula

    angle = round(math.degrees(angRadians)) #convert angle from radians to degrees

    return angle

def gradient(pt1,pt2):
    if pt2[0]==pt1[0]:
        pt2[0]+=0.1
    
    return (pt2[1]-pt1[1])/(pt2[0]-pt1[0]) #maths formula of slope = (y2-y1)/(x2-x1)

def findAngleNew(pt1,pt2,pt3):
    m1 = gradient(pt1,pt2) #m1 is slope1
    m2 = gradient(pt2,pt3) #m2 is slope2

    print(m1," ",m2)

    angRadians = math.atan((m2-m1)/(1+(m2*m1))) #maths formula tan(thetha) = (m2-m1)/(1+m1m2)

    angle = round(math.degrees(angRadians)) #convert angle from radians to degrees

    return angle


def findDis(pt1,pt2): #mathematical way for finding distance between 2 points
    return((pt2[0]-pt1[0])**2 + (pt2[1]-pt1[1])**2)**0.5


def detectArrow(img):
    imgHSV = cv.cvtColor(img, cv.COLOR_BGR2HSV) #converting image to HSV
    
    lower = np.array([0,50,20]) #lower HSV value for red colour
    upper = np.array([5,255,255]) #upper HSV value for red colour
    mask = cv.inRange(imgHSV, lower, upper) #create mask of red-coloured objects

    kernel = np.ones((5,5)) #needed for dialation and erosion
    imgDial = cv.dilate(mask, kernel, iterations=3) #applies dilation to mask
    imgErode = cv.erode(imgDial, kernel, iterations=2) #applies erosion to dilated mask
    
    contours, heirarchy = cv.findContours(imgErode, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE) 
    #finds outlines of that mask

    for cnt in contours:
        area = cv.contourArea(cnt) #calculate area of that mask

        if area>1000: #to remove noises/ small objects from getting detected *VALUE CAN BE CHANGED*

            peri = cv.arcLength(cnt, True) #calculate perimeter of outline
            approx = cv.approxPolyDP(cnt, 0.02*peri, True) #gives corners of the mask
            objCor = len(approx) #to store number of corners

            rect = cv.minAreaRect(cnt)

            if objCor==7: #arrow has 7 corners so its checking

                points = cv.boxPoints(rect) #gets corner points of that rectangle
                points = np.int0(points) #converts points to integers

                a = findDis(points[0],points[1]) #find distance between corner1 and corner2
                b = findDis(points[1],points[2]) #find distance between corner2 and corner3

                if a>b: #finding longest edge and setting the longest edge's corners as points for angle calculation
                    pt1 = points[0]  
                    pt2 = points[1]

                else:
                    pt1 = points[1]
                    pt2 = points[2]

                angle = findAngle(pt1[0],pt1[1],pt2[0],pt2[1]) #finds angle with vertical axis
                cv.putText(imgContour, "angle :"+str(angle), (frameWidth//2,frameHeight//2), cv.FONT_HERSHEY_COMPLEX,1.5,(0,0,0),2) #display angle
        

       
#MAIN CODE STARTS HERE  

cap = cv.VideoCapture(0)

initialize() 

while True:
    
    ret, img = cap.read() 
    #ret is a boolean value of if the reading of capture worked or not
    #img stores the current frame/image of the camera feed

    imgContour = img.copy()

    detectArrow(img)

    cv.imshow("Original Camera Feed", img) 
    cv.imshow('Arrow Detect',imgContour) #shows the image which shows if arrow detected or not

    if cv.waitKey(1) & 0xFF == ord('q'): #let q be the key to be pressed to quit program
        break
