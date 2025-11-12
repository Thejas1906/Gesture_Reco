import cv2
import time
import threading
import platform
import subprocess
import sys
from cvzone.HandTrackingModule import HandDetector
from directkeys import PressKey, ReleaseKey
from directkeys import (
    up_pressed, down_pressed, right_pressed,
    left_pressed, a_pressed, d_pressed
)
from flask import Flask, render_template

app = Flask(__name__)

# Global toggle for camera flip
doFlip = False


def get_camera():
    """
    Safely detects an available camera index for macOS/Windows.
    Tests both index 0 and 1.
    """
    print("🔍 Searching for available camera...")
    for idx in range(2):
        cap = cv2.VideoCapture(idx, cv2.CAP_AVFOUNDATION if platform.system() == "Darwin" else 0)
        if cap.isOpened():
            # Test frame validity
            ret, frame = cap.read()
            if ret and frame is not None and frame.size > 0:
                cap.release()
                print(f"✅ Camera found at index {idx}")
                return idx
        cap.release()
    print("❌ No working camera detected.")
    return None


def gesture_reco():
    """
    Main Gesture Recognition Function.
    Detects hand gestures and triggers keyboard keys accordingly.
    """

    detector = HandDetector(detectionCon=0.8, maxHands=2)

    # Key mappings
    brake_key_pressed = a_pressed
    accelerator_key_pressed = d_pressed
    left_key_pressed = left_pressed
    right_key_pressed = right_pressed
    up_key_pressed = up_pressed
    down_key_pressed = down_pressed

    current_key_pressed = set()

    # Auto-detect camera index
    cam_index = get_camera()
    if cam_index is None:
        print("❌ Exiting — no camera available.")
        return

    # Initialize camera safely
    if platform.system() == "Darwin":
        video = cv2.VideoCapture(cam_index, cv2.CAP_AVFOUNDATION)
        if not video.isOpened():
            print("⚠️ AVFoundation backend failed — retrying without it...")
            video = cv2.VideoCapture(cam_index)
    else:
        video = cv2.VideoCapture(cam_index)

    if not video.isOpened():
        print("❌ Could not open camera.")
        return

    cv2.namedWindow('Gesture Recognition', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Gesture Recognition', 460, 460)
    print("✅ Camera started. Press 'x' in the window to stop.")

    time.sleep(1.0)

    while True:
        ret, image = video.read()
        if not ret or image is None:
            print("⚠️ Frame not captured, trying again...")
            continue

        # Detect if frame is black/blank
        if image.mean() < 1:
            print("⚠️ Blank frame detected — switching camera backend...")
            video.release()
            gesture_reco()  # Restart detection with fallback
            return

        keyPressed = False
        key_count = 0
        key_pressed = 0

        hands, img = detector.findHands(image)

        # Flip camera if enabled
        if doFlip:
            image = cv2.flip(img, 1)
        else:
            image = img

        # Background rectangles for info display
        cv2.rectangle(image, (470, 640), (0, 750), (50, 50, 255), -2)
        cv2.rectangle(image, (850, 640), (1300, 750), (50, 50, 255), -2)

        if hands:
            lmList = hands[0]
            fingerUp = detector.fingersUp(lmList)

            # Subway Surfers - Jump
            if fingerUp == [0, 1, 0, 0, 0]:
                cv2.putText(image, 'Jump', (30, 695),
                            cv2.FONT_HERSHEY_TRIPLEX, 1.2, (255, 255, 255), 2)
                PressKey(up_key_pressed)
                current_key_pressed.add(up_key_pressed)
                key_pressed = up_key_pressed
                keyPressed = True
                key_count += 1

            # Subway Surfers - Roll
            elif fingerUp == [1, 1, 1, 1, 1]:
                cv2.putText(image, 'Roll', (30, 695),
                            cv2.FONT_HERSHEY_TRIPLEX, 1.2, (255, 255, 255), 2)
                PressKey(down_key_pressed)
                current_key_pressed.add(down_key_pressed)
                key_pressed = down_key_pressed
                keyPressed = True
                key_count += 1

            # Subway Surfers - Left
            elif fingerUp == [1, 0, 0, 0, 0]:
                cv2.putText(image, 'Left', (30, 695),
                            cv2.FONT_HERSHEY_TRIPLEX, 1.2, (255, 255, 255), 2)
                PressKey(left_key_pressed)
                current_key_pressed.add(left_key_pressed)
                key_pressed = left_key_pressed
                keyPressed = True
                key_count += 1

            # Subway Surfers - Right
            elif fingerUp == [0, 0, 0, 0, 1]:
                cv2.putText(image, 'Right', (30, 695),
                            cv2.FONT_HERSHEY_TRIPLEX, 1.2, (255, 255, 255), 2)
                PressKey(right_key_pressed)
                current_key_pressed.add(right_key_pressed)
                key_pressed = right_key_pressed
                keyPressed = True
                key_count += 1

            # Hill Climb Racing - Gas
            elif fingerUp == [0, 1, 1, 1, 1]:
                cv2.putText(image, 'Gas', (30, 695),
                            cv2.FONT_HERSHEY_TRIPLEX, 1.2, (255, 255, 255), 2)
                PressKey(accelerator_key_pressed)
                current_key_pressed.add(accelerator_key_pressed)
                key_pressed = accelerator_key_pressed
                keyPressed = True
                key_count += 1

            # Hill Climb Racing - Brake
            elif fingerUp == [0, 1, 1, 0, 0]:
                cv2.putText(image, 'Brake', (30, 695),
                            cv2.FONT_HERSHEY_TRIPLEX, 1.2, (255, 255, 255), 2)
                PressKey(brake_key_pressed)
                current_key_pressed.add(brake_key_pressed)
                key_pressed = brake_key_pressed
                keyPressed = True
                key_count += 1

            # Stand-By Modes
            elif fingerUp in ([0, 1, 0, 0, 1], [0, 0, 0, 0, 0]):
                cv2.putText(image, 'Stand-By', (30, 695),
                            cv2.FONT_HERSHEY_TRIPLEX, 1.2, (255, 255, 255), 2)

            # Release any inactive keys
            if not keyPressed and len(current_key_pressed) != 0:
                for key in current_key_pressed:
                    ReleaseKey(key)
                current_key_pressed = set()

            elif key_count == 1 and len(current_key_pressed) == 2:
                for key in list(current_key_pressed):
                    if key_pressed != key:
                        ReleaseKey(key)
                current_key_pressed = {key_pressed}

        cv2.imshow("Gesture Recognition", image)
        k = cv2.waitKey(1)
        if k == ord('x'):
            print("❌ Exiting Gesture Recognition...")
            break

    video.release()
    cv2.destroyAllWindows()


# ---------------------- FLASK ROUTES ----------------------

@app.route('/')
def index():
    """Main webpage route"""
    return render_template('index.html')


@app.route('/run_program')
def run_program():
    """
    On macOS: Launch gesture_reco() in a new process.
    On Windows/Linux: run in background thread (safe).
    """
    if platform.system() == "Darwin":
        python_exec = sys.executable
        subprocess.Popen([python_exec, __file__, "--no-flask"])
        return "Gesture recognition started (macOS-safe process)!"
    else:
        threading.Thread(target=gesture_reco).start()
        return "Gesture recognition started!"


# ---------------------- MAIN ENTRY POINT ----------------------

if __name__ == '__main__':
    if "--no-flask" in sys.argv:
        gesture_reco()
    else:
        print("🚀 Flask server running at http://127.0.0.1:5000")
        app.run(debug=True)
