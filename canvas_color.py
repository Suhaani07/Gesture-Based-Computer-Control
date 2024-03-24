import cv2
import numpy as np
from screeninfo import get_monitors

# Get the screen resolution
screen = get_monitors()[0]
canvas = np.zeros((screen.height, screen.width, 3), dtype=np.uint8)

# Set the lower and upper bounds for green color in HSV format
lower_green = np.array([40, 40, 40])
upper_green = np.array([80, 255, 255])

# Open the camera (0 corresponds to the default camera)
cap = cv2.VideoCapture(0)

while True:
    # Capture a frame from the camera
    ret, frame = cap.read()

    # Flip the frame horizontally
    frame = cv2.flip(frame, 1)

    # Resize the frame to match the canvas size
    frame = cv2.resize(frame, (screen.width, screen.height))

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask to extract the green color
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Check if any contours are found
    if contours:
        # Get the largest contour (assuming it's the object of interest)
        largest_contour = max(contours, key=cv2.contourArea)

        # Draw the contour on the canvas
        cv2.drawContours(canvas, [largest_contour], -1, (0, 255, 0), 2)

    # Display the flipped frame and full-screen canvas
    cv2.imshow('Flipped Frame', frame)
    cv2.imshow('Canvas', canvas)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
