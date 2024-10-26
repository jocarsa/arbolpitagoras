import cv2
import numpy as np

# Define the recursive function for drawing the tree
def draw_branch(x1, y1, angle, depth, thickness, img):
    if depth > 0:
        # Calculate the endpoint of the branch based on the angle and depth
        length = depth * 4  # Scale the length by the depth to shorten upper branches
        x2 = int(x1 + length * np.cos(np.radians(angle)))
        y2 = int(y1 - length * np.sin(np.radians(angle)))

        # Draw the branch line
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), thickness)

        # Reduce thickness for the next level
        new_thickness = max(1, thickness - 1)

        # Recursive calls to create branches at different angles
        # Left branch
        draw_branch(x2, y2, angle - 30, depth - 1, new_thickness, img)  
        # Right branch
        draw_branch(x2, y2, angle + 30, depth - 1, new_thickness, img)

# Initialize a blank image
width, height = 512, 512
img = np.zeros((height, width, 3), dtype=np.uint8)
img[:] = (255, 255, 255)  # Set background to white

# Initial coordinates, angle, depth, and thickness
start_x, start_y = width // 2, height - 100
initial_angle = 90  # Start angle pointing upwards
initial_depth = 10
initial_thickness = 10

# Start the fractal generation
draw_branch(start_x, start_y, initial_angle, initial_depth, initial_thickness, img)

# Display the result
cv2.imshow("Tree Fractal Pattern", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
