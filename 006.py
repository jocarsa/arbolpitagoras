import cv2
import numpy as np

# Define the recursive function for drawing the tree with progressive depth
def draw_branch(x1, y1, angle, depth, thickness, img, frames, max_depth):
    if depth > 0:
        # Calculate the endpoint of the branch based on the angle and depth
        length = depth * 4  # Scale the length by the depth to shorten upper branches
        x2 = int(x1 + length * np.cos(np.radians(angle)))
        y2 = int(y1 - length * np.sin(np.radians(angle)))

        # Draw the branch line
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), thickness)

        # Capture each frame at different depth levels
        if depth <= max_depth:
            frames.append(img.copy())

        # Reduce thickness for the next level
        new_thickness = max(1, thickness - 1)

        # Recursive calls to create branches at different angles
        draw_branch(x2, y2, angle - 30, depth - 1, new_thickness, img, frames, max_depth)
        draw_branch(x2, y2, angle + 30, depth - 1, new_thickness, img, frames, max_depth)

# Initialize a blank image
width, height = 512, 512
img = np.zeros((height, width, 3), dtype=np.uint8)
img[:] = (255, 255, 255)  # Set background to white

# Initial coordinates, angle, depth, and thickness
start_x, start_y = width // 2, height - 100
initial_angle = 90  # Start angle pointing upwards
initial_depth = 10
initial_thickness = 10

# List to store frames
frames = []

# Generate frames of the tree growth
draw_branch(start_x, start_y, initial_angle, initial_depth, initial_thickness, img, frames, initial_depth)

# Set up the video writer
fps = 60
out = cv2.VideoWriter('tree_fractal_animation.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

# Write frames to the video
for frame in frames:
    out.write(frame)

# Release the video writer
out.release()

# Display the saved video file path
print("The animation has been saved as 'tree_fractal_animation.mp4'.")

# Optionally, you can show the animation in a window with OpenCV
for frame in frames:
    cv2.imshow("Tree Fractal Animation", frame)
    cv2.waitKey(10)  # Adjust delay for smoother playback

cv2.destroyAllWindows()
