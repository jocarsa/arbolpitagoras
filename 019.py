import cv2
import numpy as np
import random
import os

# Define the recursive function for drawing the tree with progressive depth and gradient color
def draw_branch(x1, y1, angle, depth, thickness, img, out, max_depth, root_color, tip_color, segments=5):
    global frames_written
    if depth > 0 and frames_written < total_frames:  # Stop if we reach the frame limit
        # Calculate the total branch length based on the depth
        total_length = depth * random.randint(4, 20)
        segment_length = total_length / segments

        # Interpolate color from root to tip based on depth
        alpha = (max_depth - depth) / max_depth
        branch_color = (
            int((1 - alpha) * root_color[0] + alpha * tip_color[0]),
            int((1 - alpha) * root_color[1] + alpha * tip_color[1]),
            int((1 - alpha) * root_color[2] + alpha * tip_color[2]),
        )

        # Calculate the target thickness for the end of this branch
        target_thickness = max(2, thickness - (initial_thickness - 2) / max_depth)

        # Draw the branch in segments with smooth width reduction
        for i in range(segments):
            if frames_written >= total_frames:
                break  # Stop if we reach the total frame count

            # Interpolate thickness for smooth transition
            current_thickness = thickness - (i / segments) * (thickness - target_thickness)

            # Calculate endpoint for this segment
            x2 = int(x1 + segment_length * np.cos(np.radians(angle)))
            y2 = int(y1 - segment_length * np.sin(np.radians(angle)))

            # Draw the segment
            cv2.line(img, (x1, y1), (x2, y2), branch_color, int(current_thickness))

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

        # Recursive calls for child branches with adjusted angles
        draw_branch(x1, y1, angle - 30, depth - 1, target_thickness, img, out, max_depth, root_color, tip_color)
        draw_branch(x1, y1, angle + 30, depth - 1, target_thickness, img, out, max_depth, root_color, tip_color)

# Create a 'video' directory if it does not exist
os.makedirs("video", exist_ok=True)

# Video properties
width, height = 1920, 1080
fps = 60
video_duration_seconds = 60  # 1 minute
total_frames = fps * video_duration_seconds

# Set up the video writer
filename = "video/one_minute_tree_fractal.mp4"
out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

# Initialize total frames counter
frames_written = 0
initial_thickness = 50  # Starting thickness

while frames_written < total_frames:
    # Initialize a blank white image
    img = np.zeros((height, width, 3), dtype=np.uint8)
    img[:] = (255, 255, 255)

    # Initial coordinates, angle, depth, and thickness
    start_x, start_y = width // 2, height - 100
    initial_angle = 90
    initial_depth = random.randint(5, 10)

    # Define colors for root and tip
    root_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    tip_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # Generate frames for one tree iteration
    draw_branch(start_x, start_y, initial_angle, initial_depth, initial_thickness, img, out, initial_depth, root_color, tip_color)

# Release video writer and close display window
out.release()
cv2.destroyAllWindows()

print(f"The 1-minute fractal tree animation has been saved as '{filename}' in the 'video' folder.")
