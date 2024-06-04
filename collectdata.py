import os
import cv2
import numpy as np

# Define directory for saving images
directory = 'SignImage48x48/'

# Create directories if they do not exist
if not os.path.exists(directory):
    os.mkdir(directory)
if not os.path.exists(f'{directory}/blank'):
    os.mkdir(f'{directory}/blank')
for i in range(65, 91):
    letter = chr(i)
    if not os.path.exists(f'{directory}/{letter}'):
        os.mkdir(f'{directory}/{letter}')

# Capture video from webcam
cap = cv2.VideoCapture(0)

# Define sharpening kernel
sharpening_kernel = np.array([[-1, -1, -1],
                              [-1,  9, -1],
                              [-1, -1, -1]])

while True:
    # Read frame from camera
    _, frame = cap.read()
    
    # Count the number of images in each directory
    count = {chr(i): len(os.listdir(f'{directory}/{chr(i)}')) for i in range(65, 91)}
    count['blank'] = len(os.listdir(f'{directory}/blank'))
    
    # Draw rectangle for region of interest
    cv2.rectangle(frame, (0, 40), (300, 300), (255, 255, 255), 2)
    cv2.imshow("data", frame)
    
    # Extract region of interest
    frame = frame[40:300, 0:300]
    cv2.imshow("ROI", frame)
    
    # Convert to grayscale
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Resize to 48x48
    frame = cv2.resize(frame, (48, 48))
    
    # Apply sharpening filter
    frame = cv2.filter2D(frame, -1, sharpening_kernel)
    
    # Handle keypress events to save images
    interrupt = cv2.waitKey(10)
    if interrupt & 0xFF in range(ord('a'), ord('z') + 1):
        letter = chr(interrupt & 0xFF).upper()
        cv2.imwrite(f'{directory}/{letter}/{count[letter]}.jpg', frame)
    elif interrupt & 0xFF == ord('.'):
        cv2.imwrite(f'{directory}/blank/{count["blank"]}.jpg', frame)
    elif interrupt & 0xFF == 27:  # Esc key to stop
        break

cap.release()
cv2.destroyAllWindows()
