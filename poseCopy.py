import cv2
import mediapipe as mp
import numpy as np
import serial

mySerial = serial.Serial("COM11", 9600)

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)

langleOut=""
rangleOut=""


def calculate_angle(a,b,c):
    a = np.array(a) 
    b = np.array(b)
    c = np.array(c) 
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    if angle >180.0:
        angle = 360-angle
    return angle 

def final_angle(angle):
    angle  = int(angle)
    if angle == 0:
        return ("000")
    if angle < 100  and angle>0:
        if angle<10:
            return ("00"+str(angle))
        return ("0"+str(angle))
    if angle >=100:
        return (str(angle))

def final_angleB(angle):
    angle  = 180-int(angle)
    if angle == 0:
        return ("180")
    if angle < 100  and angle>0:
        if angle<10:
            return ("00"+str(angle))
        return ("0"+str(angle))
    if angle >=100:

        return (str(angle))
    
def final_anglelimited(angle):
    angle  = 180-int(angle)
    if angle == 0:
        return ("000")
    if angle < 90  and angle>0:
        if angle<10:
            return ("00"+str(angle))
        return ("0"+str(angle))
    if angle >=90:
        return ("0"+"90")

def final_anglelimitedB(angle):
    angle  = int(angle)
    if angle == 0:
        return ("180")
    if angle >90  and angle<180:
        if angle <100:
            return ("0"+str(angle))
        if angle >=100:
            return (str(angle))
    if angle <=90:
        return ("0"+"90")
    
def final_angleKneeRight(angle):
    angle  = int(angle)
    if angle == 0:
        return ("000")
    if angle >=90:
        return ("090")
    if angle <90 and angle >0:
        if angle<10:
            return ("00"+str(angle))
        return ("0"+str(angle))
    
def final_angleKneeLeft(angle):
    angle  = 180-int(angle)
    if angle==0:
        return "180"
    if angle<=90:
        return "090"
    if angle  > 90 and angle<180:
        return ("0"+str(angle))

            


with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        
        
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
      
        
        results = pose.process(image)
    
        
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        
        try:
            landmarks = results.pose_landmarks.landmark
            
            
            lshoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            lelbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            lwrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            rshoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            relbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            rwrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            lhip= [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            rhip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            rknee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            lknee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            lankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            rankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

            lkneeOut = final_angle(calculate_angle(lhip,lknee,lankle))
            rkneeOut = final_angleB(calculate_angle(rhip,rknee,rankle))
            lhipOut = final_anglelimitedB(calculate_angle(lshoulder, lhip, lknee))
            rhipOut = final_anglelimited(calculate_angle(rshoulder, rhip, rknee))
            lshoulderOut = final_angle(calculate_angle(lelbow, lshoulder, lhip))
            rshoulderOut = final_angleB(calculate_angle(relbow, rshoulder, rhip))
            lelbowOut = final_angleB(calculate_angle(lshoulder, lelbow, lwrist))
            relbowOut = final_angle(calculate_angle(rshoulder, relbow, rwrist))
            print(lshoulderOut+" "+rshoulderOut+" "+lelbowOut+" "+relbowOut+" "+lhipOut+" "+rhipOut+" "+lkneeOut+" "+rkneeOut)
            finalOut ="$"+lshoulderOut+rshoulderOut+lelbowOut+relbowOut+lhipOut+rhipOut+lkneeOut+rkneeOut
            


            print(finalOut)
            mySerial.write(finalOut.encode('utf-8'))


            # cv2.putText(image, str(angle), 
            #                tuple(np.multiply(elbow, [640, 480]).astype(int)), 
            #                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
            #                     )
                       
        except:
            pass
        
        
        
        mp_drawing.draw_landmarks(image, results.pose_landmarks
                                 )             
        
        cv2.imshow('Mediapipe Feed', image)

        
        # if angleOut<100 and angleOut>0:
        #     output = "$0"+str(angleOut)
        #     mySerial.write(output.encode('utf-8'))
        #     print(output)
        # if angleOut>=100:
        #     output = "$"+str(angleOut)
        #     mySerial.write(output.encode('utf-8'))
        #     print(output)
        

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


