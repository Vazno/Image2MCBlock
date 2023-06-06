from typing import Callable

import moviepy.editor as mp
import numpy as np
from PIL import Image

def process_video_with_pil(video: mp.VideoFileClip, process_frame: Callable) -> mp.VideoFileClip:
	# Get the original frame rate and audio
	audio = video.audio

	# Process each frame using PIL
	def process_pil_frame(frame):
		# Convert the frame to PIL Image
		image = Image.fromarray(frame)

		# Perform custom operations on the image
		processed_image = process_frame(image)

		# Convert the PIL Image back to a NumPy array
		processed_frame = np.array(processed_image)

		return processed_frame

	# Apply the PIL processing function to each frame
	processed_video = video.fl_image(process_pil_frame)

	# Set the original audio to the processed video
	processed_video = processed_video.set_audio(audio)

	# Save the modified video with the same frame rate and audio
	return processed_video