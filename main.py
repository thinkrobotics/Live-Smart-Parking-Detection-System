import cv2
import pickle
import cvzone
import numpy as np

# Video feed (0 for webcam)
cap = cv2.VideoCapture(0)

# Load marked parking spots from the file
with open('ParkingSpaces', 'rb') as f:
    polygons = pickle.load(f)

def checkParkingSpace(imgPro):
    spaceCounter = 0

    for polygon in polygons:
        # Create a mask for the polygon
        mask = np.zeros_like(imgPro)
        cv2.fillPoly(mask, [np.array(polygon)], 255)

        # Count non-zero pixels in the masked region
        count = cv2.countNonZero(cv2.bitwise_and(imgPro, imgPro, mask=mask))

        # Determine if the space is free
        if count < 900:  # Adjust threshold as needed
            color = (0, 255, 0)  # Green for free
            spaceCounter += 1
        else:
            color = (0, 0, 255)  # Red for occupied

        # Draw the polygon
        cv2.polylines(img, [np.array(polygon)], isClosed=True, color=color, thickness=2)

    # Display the number of free spaces
    cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(polygons)}', (100, 50), scale=3,
                       thickness=5, offset=20, colorR=(0, 200, 0))

while True:
    # Read a frame from the video feed
    success, img = cap.read()
    if not success:
        break

    # Preprocess the frame
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    # Check parking spaces
    checkParkingSpace(imgDilate)

    # Display the frame
    cv2.imshow("Image", img)

    # Exit on 'q' key press
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()