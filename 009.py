import cv2
import numpy as np
import random
import time
import os

# Function to create a color gradient between two colors based on the depth
def interpolate_color(start_color, end_color, ratio):
    return tuple(int(start + (end - start) * ratio) for start, end in zip(start_color, end_color))

# Define the recursive function for drawing the tree with random depth and color gradients
def draw_branch(x1, y1, angle, depth, thickness, img, frames, max_depth, branch_length, start_color, end_color):
    if depth > 0:
        # Calculate the endpoint of the branch based on the angle and randomized length
        length = depth * branch_length  # Scale length by depth
        x2 = int(x1 + length * np.cos(np.radians(angle)))
        y2 = int(y1 - length * np.sin(np.radians(angle)))

        # Interpolate the color based on the depth level to create a gradient
        color_ratio = (max_depth - depth) / max_depth
        branch_color = interpolate_color(start_color, end_color, color_ratio)

        # Draw the branch line with the interpolated color
        cv2.line(img, (x1, y1), (x2, y2), branch_color, thickness)

        # Capture each frame at different depth levels
        if depth <= max_depth:
            frames.append(img.copy())

        # Reduce thickness for the next level
        new_thickness = max(1, thickness - 1)

        # Recursive calls to create branches at different angles
        draw_branch(x2, y2, angle - 30, depth - 1, new_thickness, img, frames, max_depth, branch_length, start_color, end_color)
        draw_branch(x2, y2, angle + 30, depth - 1, new_thickness, img, frames, max_depth, branch_length, start_color, end_color)

# Create a 'video' directory if it does not exist
os.makedirs("video", exist_ok=True)

# Video properties
width, height = 1920, 1080
fps = 60
duration_seconds = 600  # 10 minutes

# Initialize start time
start_time = time.time()
iteration = 1

while time.time() - start_time < duration_seconds:
    # Initialize a blank white image
    img = np.zeros((height, width, 3), dtype=np.uint8)
    img[:] = (255, 255, 255)  # Set background to white

    # Initial coordinates, angle, and thickness
    start_x, start_y = width // 2, height - 100
    initial_angle = 90  # Start angle pointing upwards
    initial_thickness = 10

    # Randomize branch length and depth
    branch_length = random.randint(4, 16)
    initial_depth = random.randint(5, 20)

    # Randomize start and end colors for gradient effect
    start_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    end_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # List to store frames for one iteration
    frames = []

    # Generate frames of the tree growth
    draw_branch(start_x, start_y, initial_angle, initial_depth, initial_thickness, img, frames, initial_depth, branch_length, start_color, end_color)

    # Set up the video writer for the current iteration
    epoch_time = int(time.time())
    filename = f"video/tree_fractal_{epoch_time}.mp4"
    out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    # Write frames of this iteration to the video and display in the framebuffer
    for frame in frames:
        out.write(frame)
        cv2.imshow("Tree Fractal Animation", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit early
            break

    # Release the video writer for the current iteration
    out.release()

    # Display statistics
    elapsed_time = time.time() - start_time
    print(f"Iteration {iteration}: Saved {filename}, elapsed time: {elapsed_time:.2f} seconds")
    print(f" - Depth: {initial_depth}, Branch Length: {branch_length}")
    print(f" - Start Color: {start_color}, End Color: {end_color}")

    # Increment the iteration counter
    iteration += 1

# Close the display window after completion
cv2.destroyAllWindows()

print("The 10-minute fractal tree animation has been saved in the 'video' folder.")
