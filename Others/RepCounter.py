import cv2
import mediapipe as mp 
import numpy as np 

mp_drawing = mp.solutions.drawing_utils
mp_posture = mp.solutions.pose

def AngleCalculator(x,y,z):
    x = np.array(x)
    y = np.array(y)
    z = np.array(z)

    rad = np.arctan2(z[1]-y[1], z[0]-y[0]) - np.arctan2(x[1]-y[1], x[0]-y[0])
    angle = np.abs(rad*180.0/np.pi)

    if angle>180.0:
        angle = 360 - angle

    return angle



cap = cv2.VideoCapture(0)


counter = 0
counterL = 0 
counterR = 0
stage = None
stageL = None
stageR = None

with mp_posture.Pose(min_detection_confidence = 0.5, min_tracking_confidence = 0.5) as pose:
    while cap.isOpened():
        ok, frame = cap.read()

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        results = pose.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark
            shoulder = [landmarks[mp_posture.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_posture.PoseLandmark.RIGHT_SHOULDER.value].y]
            elbow = [landmarks[mp_posture.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_posture.PoseLandmark.RIGHT_ELBOW.value].y]
            wrist = [landmarks[mp_posture.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_posture.PoseLandmark.RIGHT_WRIST.value].y]

            shoulder1 = [landmarks[mp_posture.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_posture.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow1 = [landmarks[mp_posture.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_posture.PoseLandmark.LEFT_ELBOW.value].y]
            wrist1 = [landmarks[mp_posture.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_posture.PoseLandmark.LEFT_WRIST.value].y]

            angle = AngleCalculator(shoulder,elbow,wrist)
            angle1 = AngleCalculator(shoulder1,elbow1,wrist1)

            cv2.putText(image, str(angle),  
                        tuple(np.multiply(elbow, [640,700]).astype(int)),
                        cv2.FONT_HERSHEY_DUPLEX,0.5,(0,0,255),2,cv2.LINE_AA
                        )
            

            cv2.putText(image, str(angle1),  
                        tuple(np.multiply(elbow1, [1300,700]).astype(int)),
                        cv2.FONT_HERSHEY_DUPLEX,0.5,(0,0,255),2,cv2.LINE_AA
                        )
            

            if angle > 160 and angle1 > 160:
                stage = "Down"
            
            if (angle < 30  and angle1 < 30) and stage == "Down":
                stage = "up"
                counter += 1
                print(counter)
               
        except:
            pass
    

        #Display Text
        cv2.putText(image, 'REPS', (15,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter), 
                    (10,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 2, cv2.LINE_AA)
        
        
        cv2.putText(image, 'STAGE', (65,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, stage, 
                    (60,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 2, cv2.LINE_AA)
        
        
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_posture.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(247,255,0), thickness = 2, circle_radius = 2),
                                  mp_drawing.DrawingSpec(color=(0,0,0), thickness = 2, circle_radius = 2))
        
        cv2.imshow("Exercise monitor", image)

        if cv2.waitKey(10) & 0xFF == ord("x"):
            break

cap.release()
cv2.destroyAllWindows()