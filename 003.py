import cv2
import numpy as np
import math

# Initialize the canvas
width, height = 800, 800
canvas = np.ones((height, width, 3), dtype=np.uint8) * 255

# Function to draw the Pythagoras Tree recursively
def draw_pythagoras_tree(canvas, x, y, angle, size, depth):
    if depth == 0:
        return

    # Calculate the points of the square
    x1 = x + int(math.cos(angle) * size)
    y1 = y - int(math.sin(angle) * size)
    x2 = x1 + int(math.cos(angle - math.pi / 2) * size)
    y2 = y1 - int(math.sin(angle - math.pi / 2) * size)
    x3 = x + int(math.cos(angle - math.pi / 2) * size)
    y3 = y - int(math.sin(angle - math.pi / 2) * size)

    # Draw the square
    points = np.array([[x, y], [x1, y1], [x2, y2], [x3, y3]], np.int32)
    cv2.fillPoly(canvas, [points], (0, 128, 0))

    # Recursive calls for the branches
    new_size = size * 0.707  # size * sqrt(2) / 2
    draw_pythagoras_tree(canvas, x3, y3, angle + math.pi / 4, new_size, depth - 1)
    draw_pythagoras_tree(canvas, x2, y2, angle - math.pi / 4, new_size, depth - 1)

# Parameters for the Pythagoras Tree
initial_size = 100
initial_depth = 10

# Start drawing the tree
draw_pythagoras_tree(canvas, 400, 700, -math.pi / 2, initial_size, initial_depth)

# Display the result
cv2.imshow("Pythagoras Tree Fractal", canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()
