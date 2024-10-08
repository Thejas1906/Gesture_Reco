import cv2
from cvzone.HandTrackingModule import HandDetector
from directkeys import PressKey, ReleaseKey
from directkeys import up_pressed,down_pressed,right_pressed,left_pressed,a_pressed,d_pressed
import time

from flask import Flask, render_template, request, url_for
from main import *

app = Flask(__name__)

# Website intialisation
@app.route('/')
def index():
    return render_template('index.html')

# Start button action
@app.route('/run_program')
def run_program():
    gesture_reco()

# Camera flips ?
doFlip = False

if __name__ == '__main__':
    app.run(debug=True)

def gesture_reco():
    # Initialise detector code
    # detectionCon is the sensivity parameter
    detector = HandDetector(detectionCon=0.8, maxHands=2)

    # ASCII codes from "directkey.py"

    #Hill Climb Racing 
    brake_key_pressed = a_pressed
    accelerator_key_pressed = d_pressed

    #Subway Surfers
    left_key_pressed = left_pressed
    right_key_pressed = right_pressed
    up_key_pressed = up_pressed
    down_key_pressed = down_pressed

    # using a set for distinct keys
    current_key_pressed = set()

    # Initialise VideoCapture and Window
    video=cv2.VideoCapture(0)
    cv2.namedWindow('Gesture Recognition', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Gesture Recognition', 460, 460)

    # Wait for window and camera to initialise
    time.sleep(2.0)

    while True:
        ret,image=video.read()

        # Declare/Reset
        keyPressed = False
        spacePressed=False
        key_count=0
        key_pressed=0   

        # List of hands 
        hands,img=detector.findHands(image)

        # Whether to flip the camera or not
        if(doFlip):
            image = cv2.flip(img,1)

        # Rect background for "Finger Count" and "Action"
        cv2.rectangle(image, (470, 640), (0, 750),(50, 50, 255), -2)
        cv2.rectangle(image, (850, 640), (1300, 750),(50, 50, 255), -2)

        # If hands is not empty, run the program.
        if hands:
            lmList=hands[0]
            fingerUp=detector.fingersUp(lmList)

            print(fingerUp)

            # Subway Surfers - Jump 
            if fingerUp==[0,1,0,0,0]:
                # Finger Count and jump text elements
                cv2.putText(image, 'Finger Count: 1', (30,695), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (255,255,255), 2, cv2.LINE_AA)
                cv2.putText(image, 'Jump', (1000,695), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (255,255,255), 2, cv2.LINE_AA)

                PressKey(up_key_pressed)

                # Add key pressed in the set
                current_key_pressed.add(up_key_pressed)
                key_pressed=up_key_pressed
                keyPressed = True
                key_count=key_count+1

            #Subway Surfers - Roll
            if fingerUp==[1,1,1,1,1]:
                cv2.putText(image, 'Finger Count: 0', (30,695), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (255,255,255), 2, cv2.LINE_AA)
                cv2.putText(image, 'Roll', (1000,695), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (255,255,255), 2, cv2.LINE_AA)
                PressKey(down_key_pressed)
                
                current_key_pressed.add(down_key_pressed)
                key_pressed=down_key_pressed
                keyPressed = True
                key_count=key_count+1

            #Subway Surfers - Left    
            if fingerUp==[1,0,0,0,0]:
                cv2.putText(image, 'Finger Count: 1', (30,695), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (255,255,255), 2, cv2.LINE_AA)
                cv2.putText(image, 'Left', (1000,695), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (255,255,255), 2, cv2.LINE_AA)
                PressKey(left_key_pressed)
                
                current_key_pressed.add(left_key_pressed)
                key_pressed=left_key_pressed
                keyPressed = True
                key_count=key_count+1

            #Subway Surfers - Right
            if fingerUp==[0,0,0,0,1]:
                cv2.putText(image, 'Finger Count: 1', (30,695), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (255,255,255), 2, cv2.LINE_AA)
                cv2.putText(image, 'Right', (990,695), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (255,255,255), 2, cv2.LINE_AA)
                PressKey(right_key_pressed)
                
                current_key_pressed.add(right_key_pressed)
                key_pressed=right_key_pressed
                keyPressed = True
                key_count=key_count+1

            #Hill Climb Racing - Gas
            if fingerUp==[0,1,1,1,1]:
                cv2.putText(image, 'Finger Count: 4', (30,695), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (255,255,255), 2, cv2.LINE_AA)
                cv2.putText(image, 'Gas', (1020,695), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (255,255,255), 2, cv2.LINE_AA)
                PressKey(accelerator_key_pressed)
                
                current_key_pressed.add(accelerator_key_pressed)
                key_pressed=accelerator_key_pressed
                keyPressed = True
                key_count=key_count+1

            #Hill Climb Racing - Brake    
            if fingerUp==[0,1,1,0,0]:
                cv2.putText(image, 'Finger Count: 2', (30,695), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (255,255,255), 2, cv2.LINE_AA)
                cv2.putText(image, 'Brake', (980,695), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (255,255,255), 2, cv2.LINE_AA)
                PressKey(brake_key_pressed)
                
                current_key_pressed.add(brake_key_pressed)
                key_pressed=brake_key_pressed
                keyPressed = True
                key_count=key_count+1

            #Virtual Touch
            if fingerUp==[0,1,0,0,1]:
                cv2.putText(image, 'Finger Count: 5', (30,695), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (255,255,255), 2, cv2.LINE_AA)
                cv2.putText(image, 'Stand-By', (950,695), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (255,255,255), 2, cv2.LINE_AA)

                
            # Stand-By
            if fingerUp==[0,0,0,0,0]:
                cv2.putText(image, 'Finger Count: 5', (30,695), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (255,255,255), 2, cv2.LINE_AA)
                cv2.putText(image, 'Stand-By', (950,695), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (255,255,255), 2, cv2.LINE_AA)


            # Release the key and empty the list if the key is not pressed.
            if not keyPressed and len(current_key_pressed) != 0:
                for key in current_key_pressed:
                    ReleaseKey(key)
                current_key_pressed = set()
                print("IF BLOCK")
            elif key_count==1 and len(current_key_pressed)==2:    
                for key in current_key_pressed:             
                    if key_pressed!=key:
                        ReleaseKey(key)
                current_key_pressed = set()
                for key in current_key_pressed:
                    ReleaseKey(key)
                current_key_pressed = set()
                print("ELIF BLOCK")


        cv2.imshow("Gesture Recognition",image)
        k=cv2.waitKey(1)
        if k==ord('x'):
            break

    video.release()
    cv2.destroyAllWindows()