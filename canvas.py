# All the imports go here
import cv2
import numpy as np
import mediapipe as mp
from collections import deque
import requests
from google.cloud import vision_v1  
from google.cloud.vision_v1 import types
from collections import deque
from gtts import gTTS
import os

# Set the path to the Google Cloud credentials file
credentials_path = 'upheld-conduit-413318-f5dc7272910e.json'
client = vision_v1.ImageAnnotatorClient.from_service_account_file(credentials_path)

# Giving different arrays to handle color points of different colors
bpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]

# These indexes will be used to mark the points in particular arrays of specific colors
blue_index = 0
red_index = 0
yellow_index = 0

# The kernel to be used for dilation purpose
kernel = np.ones((5, 5), np.uint8)

colors = [(255, 0, 0), (0, 0, 255), (0, 255, 255), (0, 255, 255)]
colorIndex = 0

# Here is code for Canvas setup
paintWindow = np.zeros((471, 636, 3), dtype=np.uint8)
paintWindow[67:, :, :] = 0

cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)

# initialize mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

# Initialize the webcam
cap = cv2.VideoCapture(0)
ret = True

# Initialize a flag to check if the screenshot has been taken
screenshot_taken = False

while ret:
    # Read each frame from the webcam
    ret, frame = cap.read()

    x, y, c = frame.shape

    # Flip the frame vertically
    frame = cv2.flip(frame, 1)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    frame = cv2.rectangle(frame, (40, 1), (140, 65), (0, 0, 0), 2)
    frame = cv2.rectangle(frame, (160, 1), (255, 65), (255, 0, 0), 2)
    frame = cv2.rectangle(frame, (275, 1), (370, 65), (0, 0, 255), 2)
    frame = cv2.rectangle(frame, (390, 1), (485, 65), (0, 255, 255), 2)
    frame = cv2.rectangle(frame, (505, 1), (600, 65), (0, 255, 0), 2)  # Rectangle for "DONE" button

    cv2.putText(frame, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "RED", (289, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "YELLOW", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "DONE", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2, cv2.LINE_AA)  # Text for "DONE"

    # Get hand landmark prediction
    result = hands.process(framergb)

    # post process the result
    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                lmx = int(lm.x * 640)
                lmy = int(lm.y * 480)
                landmarks.append([lmx, lmy])

            # Drawing landmarks on frames
            mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)
        fore_finger = (landmarks[8][0], landmarks[8][1])
        center = fore_finger
        thumb = (landmarks[4][0], landmarks[4][1])
        cv2.circle(frame, center, 3, (0, 255, 0), -1)

        # Adding functionality for "DONE" button
        if 505 <= center[0] <= 600 and 1 <= center[1] <= 65 and not screenshot_taken:
            print("DONE button pressed")
            # Take a screenshot of the canvas
            cv2.imwrite("canvas_screenshot.png", paintWindow)
            print("Canvas screenshot saved.")

            # Read the saved screenshot
            screenshot_path = "canvas_screenshot.png"
            with open(screenshot_path, 'rb') as image_file:
                content = image_file.read()

            # Create a Google Cloud Vision API image instance
            image = types.Image(content=content)

            # Use the Vision API to detect text
            response = client.text_detection(image=image)
            texts = response.text_annotations

            if texts:
                # Extract and print the detected text
                detected_text = texts[0].description
                print("Text in screenshot:", detected_text)
                
                # Convert text to speech
                tts = gTTS(text=detected_text, lang='en')
                tts.save("detected_text.mp3")
                
                # Play the generated audio file
                os.system("start detected_text.mp3")
                print("Speaking:", detected_text )
            else:
                print("No text found in the screenshot.")

            screenshot_taken = True  # Set the flag to True to indicate the screenshot has been taken

        elif (thumb[1] - center[1] < 30):
            bpoints.append(deque(maxlen=512))
            blue_index += 1
            rpoints.append(deque(maxlen=512))
            red_index += 1
            ypoints.append(deque(maxlen=512))
            yellow_index += 1

        elif center[1] <= 65:
            if 40 <= center[0] <= 140:  # Clear Button
                bpoints = [deque(maxlen=512)]
                rpoints = [deque(maxlen=512)]
                ypoints = [deque(maxlen=512)]

                blue_index = 0
                red_index = 0
                yellow_index = 0

                paintWindow[67:, :, :] = 0

                screenshot_taken = False  # Reset the flag when clearing the canvas
            elif 160 <= center[0] <= 255:
                colorIndex = 0  # Blue
            elif 275 <= center[0] <= 370:
                colorIndex = 2  # Red
            elif 390 <= center[0] <= 485:
                colorIndex = 3  # Yellow

        else:
            if colorIndex == 0:
                bpoints[blue_index].appendleft(center)
            elif colorIndex == 2:
                rpoints[red_index].appendleft(center)
            elif colorIndex == 3:
                ypoints[yellow_index].appendleft(center)

    # Append the next deques when nothing is detected to avoid messing up
    else:
        bpoints.append(deque(maxlen=512))
        blue_index += 1
        rpoints.append(deque(maxlen=512))
        red_index += 1
        ypoints.append(deque(maxlen=512))
        yellow_index += 1

    # Draw lines of all the colors on the canvas and frame
    points = [bpoints, rpoints, ypoints]
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k - 1] is None or points[i][j][k] is None:
                    continue
                cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)

    cv2.imshow("Output", frame)
    cv2.imshow("Paint", paintWindow)

    if cv2.waitKey(1) == ord('q'):
        break

# Release the webcam and destroy all active windows
cap.release()
cv2.destroyAllWindows()
