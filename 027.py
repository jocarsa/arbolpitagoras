import cv2
import numpy as np
import random
import os
import time

# Define the recursive function for drawing the tree with progressive depth, gradient color, and leaves at branch tips
def draw_branch(x1, y1, angle, depth, thickness, img, out, max_depth, root_color, tip_color, segments=5, leaf_size_range=(5, 10), angle_variation=60):
    global frames_written
    if depth > 0 and frames_written < total_frames:  # Stop if we reach the frame limit
        # Calculate the total branch length based on the depth
        total_length = depth * random.randint(10, 15)
        segment_length = total_length / segments

        # Calculate target thickness for smooth transition
        target_thickness = max(2, thickness - (initial_thickness - 2) / max_depth)

        # Draw the branch in segments with smooth width and color transitions
        for i in range(segments):
            if frames_written >= total_frames:
                break  # Stop if we reach the total frame count

            # Interpolate color for each segment to create a smooth gradient
            alpha = ((max_depth - depth) + (i / segments)) / max_depth
            current_color = (
                int((1 - alpha) * root_color[0] + alpha * tip_color[0]),
                int((1 - alpha) * root_color[1] + alpha * tip_color[1]),
                int((1 - alpha) * root_color[2] + alpha * tip_color[2]),
            )

            # Interpolate thickness for smooth transition
            current_thickness = thickness - (i / segments) * (thickness - target_thickness)

            # Add a slight rotation for each segment to create a natural curve
            segment_angle = angle + random.uniform(-angle_variation / segments, angle_variation / segments)

            # Calculate endpoint for this segment
            x2 = int(x1 + segment_length * np.cos(np.radians(segment_angle)))
            y2 = int(y1 - segment_length * np.sin(np.radians(segment_angle)))

            # Draw the segment
            cv2.line(img, (x1, y1), (x2, y2), current_color, int(current_thickness))

            # Write each frame directly to the video and increment frame count
            out.write(img.copy())
            frames_written += 1  # Track frames written to video

            # Display the frame in a window for real-time feedback
            cv2.imshow("Tree Fractal Animation", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit early
                frames_written = total_frames
                break

            # Move to the end of this segment
            x1, y1 = x2, y2

        # If depth is 1, draw a leaf (ellipse) at the branch tip with random size
        if depth == 1:
            leaf_width = random.randint(leaf_size_range[0], leaf_size_range[1])
            leaf_height = random.randint(leaf_size_range[0], leaf_size_range[1])
            cv2.ellipse(img, (x1, y1), (leaf_width, leaf_height), angle + 90, 0, 360, current_color, -1)

        # Randomly decide the number of child branches (between 1 and 4)
        num_branches = random.randint(1, 4)
        for _ in range(num_branches):
            random_angle = random.randint(0, angle_variation)
            new_angle = angle + random.randint(-angle_variation, angle_variation)
            draw_branch(x1, y1, new_angle, depth - 1, target_thickness, img, out, max_depth, root_color, tip_color, segments, leaf_size_range, angle_variation)

# Create a 'video' directory if it does not exist
os.makedirs("video", exist_ok=True)

# Video properties
width, height = 1920, 1080
fps = 60
video_duration_seconds = 60  # 1 minute
total_frames = fps * video_duration_seconds

# Generate unique filename with epoch timestamp
epoch_time = int(time.time())
filename = f"video/one_minute_tree_fractal_{epoch_time}.mp4"
out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

# Initialize total frames counter
frames_written = 0
initial_thickness = 50  # Starting thickness

# Define leaf size range (min, max)
leaf_size_range = (5, 15)

while frames_written < total_frames:
    # Initialize a blank white image
    img = np.zeros((height, width, 3), dtype=np.uint8)
    img[:] = (255, 255, 255)

    # Initial coordinates, angle, depth, and thickness
    start_x, start_y = width // 2, height - 100
    initial_angle = 90
    initial_depth = 10

    # Define colors for root and tip
    root_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    tip_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # Set the maximum angle variation between branches
    angle_variation = 30

    # Generate frames for one tree iteration
    draw_branch(start_x, start_y, initial_angle, initial_depth, initial_thickness, img, out, initial_depth, root_color, tip_color, leaf_size_range=leaf_size_range, angle_variation=angle_variation)

# Release video writer and close display window
out.release()
cv2.destroyAllWindows()

print(f"The 1-minute fractal tree animation with random leaf sizes and branch angles has been saved as '{filename}' in the 'video' folder.")
