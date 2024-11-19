import cv2
import numpy as np
import random
import os
import time
from multiprocessing import Process, Queue, Value

# Recursive branch drawing function that works in parallel
def draw_branch(x1, y1, angle, depth, thickness, queue, max_depth, root_color, tip_color, segments=5, leaf_size_range=(5, 10), angle_variation=40):
    if depth > 0:  # Draw branch only if depth is positive
        total_length = depth * random.randint(10, 15)
        segment_length = total_length / segments

        target_thickness = max(2, thickness - (initial_thickness - 2) / max_depth)
        shadow_offset = 3
        shadow_color = (0, 0, 0)
        shadow_alpha = 0.4
        shadow_blur_ksize = (7, 7)
        
        # Create an array for shadow effect
        branch_img = np.zeros((height, width, 3), dtype=np.uint8)

        for i in range(segments):
            alpha = ((max_depth - depth) + (i / segments)) / max_depth
            current_color = (
                int((1 - alpha) * root_color[0] + alpha * tip_color[0]),
                int((1 - alpha) * root_color[1] + alpha * tip_color[1]),
                int((1 - alpha) * root_color[2] + alpha * tip_color[2]),
            )
            current_thickness = thickness - (i / segments) * (thickness - target_thickness)
            segment_angle = angle + random.uniform(-angle_variation / segments, angle_variation / segments)
            x2 = int(x1 + segment_length * np.cos(np.radians(segment_angle)))
            y2 = int(y1 - segment_length * np.sin(np.radians(segment_angle)))

            # Draw the shadow and branch segment
            cv2.line(branch_img, (x1 + shadow_offset, y1 + shadow_offset), (x2 + shadow_offset, y2 + shadow_offset), shadow_color, int(current_thickness), lineType=cv2.LINE_AA)
            cv2.line(branch_img, (x1, y1), (x2, y2), current_color, int(current_thickness), lineType=cv2.LINE_AA)

            x1, y1 = x2, y2

        # If at the tip, draw a leaf
        if depth == 1:
            leaf_width = random.randint(leaf_size_range[0], leaf_size_range[1])
            leaf_height = random.randint(leaf_size_range[0], leaf_size_range[1])
            cv2.ellipse(branch_img, (x1, y1), (leaf_width, leaf_height), angle + 90, 0, 360, current_color, -1)

        # Send the branch image to the main queue
        queue.put(branch_img)

# Main tree drawing function with multiprocessing support
def generate_tree_animation():
    os.makedirs("video", exist_ok=True)
    filename = f"video/one_minute_tree_fractal_{int(time.time())}.mp4"
    out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    frame_queue = Queue()
    processes = []
    frames_written = 0

    while frames_written < total_frames:
        img = np.zeros((height, width, 3), dtype=np.uint8)
        start_x, start_y = width // 2, height - 100
        initial_angle = 90
        initial_depth = 10
        root_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        tip_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        num_branches = random.randint(2, 5)
        for _ in range(num_branches):
            angle_variation = random.randint(-40, 40)
            p = Process(target=draw_branch, args=(start_x, start_y, initial_angle + angle_variation, initial_depth, initial_thickness, frame_queue, initial_depth, root_color, tip_color))
            processes.append(p)
            p.start()

        for p in processes:
            p.join()  # Ensure all processes complete for this frame

        # Combine branches from the queue
        while not frame_queue.empty():
            branch_img = frame_queue.get()
            img = cv2.addWeighted(img, 1, branch_img, 1, 0)

        out.write(img)
        frames_written += 1
        cv2.imshow("Tree Fractal Animation", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            frames_written = total_frames
            break

    out.release()
    cv2.destroyAllWindows()
    print(f"Animation saved as '{filename}'")

# Global settings
width, height = 1920, 1080
fps = 60
video_duration_seconds = 60
total_frames = fps * video_duration_seconds
initial_thickness = 50

generate_tree_animation()
