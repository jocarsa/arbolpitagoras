import cv2
import numpy as np
import random
import os
import time

def draw_branch(x1, y1, angle, depth, thickness, img, out, max_depth, current_color, tip_color, segments=5, leaf_size_range=(5, 10), angle_variation=180, color_variation=5):
    global frames_written
    if depth > 0 and frames_written < total_frames:  # Stop if we reach the frame limit
        # Calculate the base length, with a slight random variation for each branch
        total_length = depth * random.randint(10, 15) + random.randint(-2, 2)
        segment_length = total_length / segments

        # Target thickness for smooth transition
        target_thickness = max(2, thickness - (initial_thickness - 2) / max_depth)

        # Shadow properties
        shadow_offset = 3
        shadow_color = (0, 0, 0)  # Black shadow
        shadow_alpha = 0.4  # Transparency for shadow
        shadow_blur_ksize = (7, 7)  # Kernel size for shadow blur

        # Create a separate layer for the shadow
        shadow_layer = np.zeros_like(img, dtype=np.uint8)

        for i in range(segments):
            if frames_written >= total_frames:
                break  # Stop if we reach the total frame count

            # Accumulative color change with random variation
            alpha = ((max_depth - depth) + (i / segments)) / max_depth
            current_color = (
                int((1 - alpha) * current_color[0] + alpha * tip_color[0] + random.randint(-color_variation, color_variation)),
                int((1 - alpha) * current_color[1] + alpha * tip_color[1] + random.randint(-color_variation, color_variation)),
                int((1 - alpha) * current_color[2] + alpha * tip_color[2] + random.randint(-color_variation, color_variation))
            )

            # Interpolate thickness for smooth transition
            current_thickness = thickness - (i / segments) * (thickness - target_thickness)

            # Slight random rotation for natural curvature and chaos effect
            segment_angle = angle + random.uniform(-angle_variation / segments, angle_variation / segments) + random.uniform(-2, 2)

            # Calculate endpoint for this segment with a little length chaos
            x2 = int(x1 + (segment_length + random.uniform(-1, 1)) * np.cos(np.radians(segment_angle)))
            y2 = int(y1 - (segment_length + random.uniform(-1, 1)) * np.sin(np.radians(segment_angle)))

            # Draw shadow with slight offset
            shadow_start = (x1 + shadow_offset, y1 + shadow_offset)
            shadow_end = (x2 + shadow_offset, y2 + shadow_offset)
            cv2.line(shadow_layer, shadow_start, shadow_end, shadow_color, int(current_thickness), lineType=cv2.LINE_AA)

            # Draw the branch segment on the main image
            cv2.line(img, (x1, y1), (x2, y2), current_color, int(current_thickness), lineType=cv2.LINE_AA)

            # Write frame to video
            out.write(img.copy())
            frames_written += 1  # Track frames written to video

            # Display the frame in real-time
            cv2.imshow("Tree Fractal Animation", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit early
                frames_written = total_frames
                break

            # Move to the next segment's starting point
            x1, y1 = x2, y2

        # Draw leaf with shadow if at the branch tip
        if depth == 1:
            leaf_width = random.randint(leaf_size_range[0], leaf_size_range[1])
            leaf_height = random.randint(leaf_size_range[0], leaf_size_range[1])

            # Leaf shadow on shadow layer
            shadow_leaf_center = (x1 + shadow_offset, y1 + shadow_offset)
            cv2.ellipse(shadow_layer, shadow_leaf_center, (leaf_width, leaf_height), angle + 90, 0, 360, shadow_color, -1)

            # Draw actual leaf
            cv2.ellipse(img, (x1, y1), (leaf_width, leaf_height), angle + 90, 0, 360, current_color, -1)

        # Blur shadow layer and blend
        shadow_layer = cv2.GaussianBlur(shadow_layer, shadow_blur_ksize, 0)
        shadow_mask = cv2.cvtColor(shadow_layer, cv2.COLOR_BGR2GRAY)
        _, shadow_mask = cv2.threshold(shadow_mask, 1, 255, cv2.THRESH_BINARY)
        img[shadow_mask > 0] = cv2.addWeighted(img, 1 - shadow_alpha, shadow_layer, shadow_alpha, 0)[shadow_mask > 0]

        # Recursively draw child branches with inherited color
        num_branches = random.randint(1, 4)
        for _ in range(num_branches):
            new_angle = angle + random.randint(-angle_variation, angle_variation)
            draw_branch(x1, y1, new_angle, depth - 1, target_thickness, img, out, max_depth, current_color, tip_color, segments, leaf_size_range, angle_variation, color_variation)



# Create a 'video' directory if it does not exist
os.makedirs("video", exist_ok=True)

# Video properties
width, height = 1920, 1080
fps = 30
video_duration_seconds = 60*60*6  # 1 minute
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

# Initialize a blank white image outside the loop
img = np.zeros((height, width, 3), dtype=np.uint8)
img[:] = (0, 0, 0)

while frames_written < total_frames:
    # Initial coordinates, angle, depth, and thickness
    start_x = random.randint(0, width)
    start_y = height - 0  # Fixed starting y-coordinate
    initial_angle = 90
    initial_depth = 10

    # Define colors for root and tip
    root_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    tip_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # Set the maximum angle variation between branches
    angle_variation = 40

    # Generate frames for one tree iteration
    draw_branch(start_x, start_y, initial_angle, initial_depth, initial_thickness, img, out, initial_depth, root_color, tip_color, leaf_size_range=leaf_size_range, angle_variation=angle_variation)
# Release video writer and close display window
out.release()
cv2.destroyAllWindows()

print(f"The 1-minute fractal tree animation with blurred shadows has been saved as '{filename}' in the 'video' folder.")
