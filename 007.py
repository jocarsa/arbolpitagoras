import cv2
import numpy as np
import random
import time

# Define the recursive function for drawing the tree with progressive depth
def draw_branch(x1, y1, angle, depth, thickness, img, frames, max_depth, branch_color):
    if depth > 0:
        # Calculate the endpoint of the branch based on the angle and depth
        length = depth * 4  # Scale the length by the depth to shorten upper branches
        x2 = int(x1 + length * np.cos(np.radians(angle)))
        y2 = int(y1 - length * np.sin(np.radians(angle)))

        # Draw the branch line
        cv2.line(img, (x1, y1), (x2, y2), branch_color, thickness)

        # Capture each frame at different depth levels
        if depth <= max_depth:
            frames.append(img.copy())

        # Reduce thickness for the next level
        new_thickness = max(1, thickness - 1)

        # Recursive calls to create branches at different angles
        draw_branch(x2, y2, angle - 30, depth - 1, new_thickness, img, frames, max_depth, branch_color)
        draw_branch(x2, y2, angle + 30, depth - 1, new_thickness, img, frames, max_depth, branch_color)

# Video properties
width, height = 1920, 1080
fps = 60
duration_seconds = 600  # 10 minutes

# Set up the video writer
out = cv2.VideoWriter('tree_fractal_animation.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

# Initialize start time
start_time = time.time()

while time.time() - start_time < duration_seconds:
    # Initialize a blank white image
    img = np.zeros((height, width, 3), dtype=np.uint8)
    img[:] = (255, 255, 255)  # Set background to white

    # Initial coordinates, angle, depth, and thickness
    start_x, start_y = width // 2, height - 100
    initial_angle = 90  # Start angle pointing upwards
    initial_depth = 10
    initial_thickness = 10

    # Randomize branch color
    branch_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # List to store frames for one iteration
    frames = []

    # Generate frames of the tree growth
    draw_branch(start_x, start_y, initial_angle, initial_depth, initial_thickness, img, frames, initial_depth, branch_color)

    # Write frames of this iteration to the video
    for frame in frames:
        out.write(frame)

# Release the video writer
out.release()

print("The 10-minute fractal tree animation has been saved as 'tree_fractal_animation.mp4'.")
