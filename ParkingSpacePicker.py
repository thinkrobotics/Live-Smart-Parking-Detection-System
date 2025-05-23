import cv2
import numpy as np
import pickle

# Initialize variables
points = []  # List to store points of the polygon
drawing = False  # Flag to indicate if drawing is in progress
polygons = []  # List to store all polygons (parking spaces)

# Mouse callback function
def mouseClick(event, x, y, flags, params):
    global poinats, drawing, polygons

    # Left-click to add points to the polygon
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        drawing = True

    # Right-click to complete the polygon and save it
    if event == cv2.EVENT_RBUTTONDOWN:
        if len(points) > 2:  # A polygon must have at least 3 points
            polygons.append(points)  # Save the polygon
            points = []  # Reset points for the next polygon
            drawing = False
            print("Polygon saved!")

    # Middle-click to delete the last polygon
    if event == cv2.EVENT_MBUTTONDOWN:
        if polygons:
            polygons.pop()  # Remove the last polygon
            print("Last polygon deleted!")

# Load or initialize parking space data
try:
    with open('ParkingSpaces', 'rb') as f:
        polygons = pickle.load(f)
except:
    polygons = []

# Load the static image
img = cv2.imread('test.png')

# Create a window and set the mouse callback
cv2.namedWindow("Image")
cv2.setMouseCallback("Image", mouseClick)

while True:
    # Display the image
    img_display = img.copy()

    # Draw all saved polygons
    for polygon in polygons:
        cv2.polylines(img_display, [np.array(polygon)], isClosed=True, color=(0, 255, 0), thickness=2)

    # Draw the current polygon being drawn
    if drawing and len(points) > 1:
        cv2.polylines(img_display, [np.array(points)], isClosed=False, color=(0, 0, 255), thickness=2)

    # Show the image
    cv2.imshow("Image", img_display)

    # Save the polygons to a file when 's' is pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        with open('ParkingSpaces', 'wb') as f:
            pickle.dump(polygons, f)
        print("Parking spaces saved!")

    # Exit when 'q' is pressed
    if key == ord('q'):
        break

cv2.destroyAllWindows()