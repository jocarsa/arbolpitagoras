import cv2
import numpy as np

# Set up the canvas
width, height = 800, 800
canvas = np.ones((height, width, 3), dtype=np.uint8) * 255

# Set the base square size and starting position
initial_size = 80
x_start, y_start = width // 2, height - initial_size // 2

def draw_square(img, x, y, size, angle, color):
    # Calculate the coordinates of the rotated square
    half_size = size / 2
    rad = np.radians(angle)
    cos_a, sin_a = np.cos(rad), np.sin(rad)

    # Points of the square
    pts = np.array([
        (x + cos_a * (-half_size) - sin_a * (-half_size), y + sin_a * (-half_size) + cos_a * (-half_size)),
        (x + cos_a * (half_size) - sin_a * (-half_size), y + sin_a * (-half_size) + cos_a * (half_size)),
        (x + cos_a * (half_size) - sin_a * (half_size), y + sin_a * (half_size) + cos_a * (half_size)),
        (x + cos_a * (-half_size) - sin_a * (half_size), y + sin_a * (half_size) + cos_a * (-half_size))
    ], np.int32)

    # Draw the square
    cv2.fillPoly(img, [pts], color)
    return pts[1], pts[2]  # Return top two points for the next branch

def draw_tree(img, x, y, size, angle, depth):
    if depth == 0:
        return

    # Draw the base square
    color = (0, 100 + 15 * depth, 0)
    top_left, top_right = draw_square(img, x, y, size, angle, color)

    # Parameters for the next branches
    new_size = size * 0.707  # Scale down by sqrt(2)/2
    draw_tree(img, *top_left, new_size, angle - 45, depth - 1)   # Left branch
    draw_tree(img, *top_right, new_size, angle + 45, depth - 1)  # Right branch

# Draw the Pythagoras tree fractal
draw_tree(canvas, x_start, y_start, initial_size, -90, 10)

# Display the fractal
cv2.imshow("Pythagoras Tree", canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()
