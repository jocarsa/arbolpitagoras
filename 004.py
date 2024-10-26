import cv2
import numpy as np

# Define the recursive function for drawing the levels
def level(ax, ay, bx, by, depth, img):
    if depth > 0:
        dx, dy = bx - ax, ay - by
        x3, y3 = bx - dy, by - dx
        x4, y4 = ax - dy, ay - dx
        x5, y5 = x4 + (dx - dy) / 2, y4 - (dx + dy) / 2

        # Draw the base shape with lines
        cv2.line(img, (int(ax), int(ay)), (int(bx), int(by)), (0, 0, 255), 1)  # Red line
        cv2.line(img, (int(bx), int(by)), (int(x3), int(y3)), (0, 0, 255), 1)  # Red line
        cv2.line(img, (int(x3), int(y3)), (int(x4), int(y4)), (0, 0, 255), 1)  # Red line
        cv2.line(img, (int(x4), int(y4)), (int(ax), int(ay)), (0, 0, 255), 1)  # Red line

        # Recursive calls for the fractal levels
        level(x4, y4, x5, y5, depth - 1, img)
        level(x5, y5, x3, y3, depth - 1, img)

# Initialize a blank image
width, height = 1000, 1000
img = np.zeros((height, width, 3), dtype=np.uint8)
img[:] = (255, 255, 255)  # Set background to white

# Initial coordinates and depth
start_x, start_y = 400, 800
end_x, end_y = 600, 800
depth = 12

# Start the fractal generation
level(start_x, start_y, end_x, end_y, depth, img)

# Display the result
cv2.imshow("Fractal Pattern", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
