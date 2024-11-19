import cv2
import numpy as np
import time
import os

# Create a 'video' directory if it does not exist
os.makedirs("video", exist_ok=True)

# Video properties
width, height = 1920, 1080
fps = 30
duration_seconds = 10  # Shortened to 10 seconds for quick testing

# Set up the video writer for the entire duration
filename = "video/simple_test.mp4"
out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

# Initialize start time
start_time = time.time()

while time.time() - start_time < duration_seconds:
    # Initialize a blank white image
    img = np.zeros((height, width, 3), dtype=np.uint8)
    img[:] = (255, 255, 255)  # Set background to white

    # Draw a single line for testing
    cv2.line(img, (width // 2, height - 100), (width // 2, height - 300), (0, 0, 255), 5)

    # Write the frame to the video
    out.write(img)

    # Display the current frame in a window
    cv2.imshow("Tree Growth Test", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit early
        break

# Release the video writer and destroy the display window
out.release()
cv2.destroyAllWindows()
print("Simple test video generation completed.")
