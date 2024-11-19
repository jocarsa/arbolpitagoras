import cv2
import numpy as np
import random
import time
import os

# Define the recursive function for drawing the tree with progressive depth and gradient color
def draw_branch(x1, y1, angle, depth, thickness, img, frames, max_depth, root_color, tip_color):
    if depth > 0:
        # Calculate the endpoint of the branch based on the angle and depth
        length = depth * random.randint(4, 20)  # Scale the length by the depth to shorten upper branches
        x2 = int(x1 + length * np.cos(np.radians(angle)))
        y2 = int(y1 - length * np.sin(np.radians(angle)))

        # Interpolate between root and tip colors based on depth
        alpha = (max_depth - depth) / max_depth  # Scale alpha to vary from 0 at the root to 1 at the tips
        branch_color = (
            int((1 - alpha) * root_color[0] + alpha * tip_color[0]),
            int((1 - alpha) * root_color[1] + alpha * tip_color[1]),
            int((1 - alpha) * root_color[2] + alpha * tip_color[2]),
        )

        # Draw the branch line
        cv2.line(img, (x1, y1), (x2, y2), branch_color, int(thickness))

        # Capture each frame at different depth levels
        if depth <= max_depth:
            frames.append(img.copy())

        # Calculate the new thickness for the next branch level (gradient of widths)
        new_thickness = max(2, thickness - (initial_thickness - 2) / max_depth)

        # Recursive calls to create branches at different angles
        draw_branch(x2, y2, angle - 30, depth - 1, new_thickness, img, frames, max_depth, root_color, tip_color)
        draw_branch(x2, y2, angle + 30, depth - 1, new_thickness, img, frames, max_depth, root_color, tip_color)

# Create a 'video' directory if it does not exist
os.makedirs("video", exist_ok=True)

# Video properties
width, height = 1920, 1080
fps = 60
video_duration_seconds = 60  # 1 minute
total_frames = fps * video_duration_seconds

# Set up the video writer for the entire session
filename = "video/one_minute_tree_fractal.mp4"
out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

# Initialize total frames counter
frames_written = 0
initial_thickness = 50  # Starting thickness

while frames_written < total_frames:
    # Initialize a blank white image
    img = np.zeros((height, width, 3), dtype=np.uint8)
    img[:] = (255, 255, 255)  # Set background to white

    # Initial coordinates, angle, depth, and thickness
    start_x, start_y = width // 2, height - 100
    initial_angle = 90  # Start angle pointing upwards
    initial_depth = random.randint(5, 10)

    # Define colors for the root and tips
    root_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # Random root color
    tip_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # Random tip color

    # List to store frames for one iteration
    frames = []

    # Generate frames of the tree growth
    draw_branch(start_x, start_y, initial_angle, initial_depth, initial_thickness, img, frames, initial_depth, root_color, tip_color)

    # Write frames of this tree growth to the video and display in the framebuffer
    for frame in frames:
        if frames_written >= total_frames:
            break
        out.write(frame)
        cv2.imshow("Tree Fractal Animation", frame)  # Show each frame in a window
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit early
            frames_written = total_frames  # Exit the loop
            break
        frames_written += 1

# Release the video writer and close display window
out.release()
cv2.destroyAllWindows()

print(f"The 1-minute fractal tree animation has been saved as '{filename}' in the 'video' folder.")
