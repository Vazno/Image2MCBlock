import sys
import os
import mimetypes

from PIL import Image

def resize_image(image: Image, scale_factor: int) -> Image:
	# Calculate the new size based on the scale factor
	if scale_factor >= 0:
		new_width = int(image.width * scale_factor)
		new_height = int(image.height * scale_factor)
	else:
		new_width = int(image.width / abs(scale_factor))
		new_height = int(image.height / abs(scale_factor))
	new_size = (new_width, new_height)

	# Resize the image
	resized_image = image.resize(new_size)

	return resized_image

def crop_to_make_divisible(image: Image, divisible_by=16) -> Image:
	x = image.size[0]
	y = image.size[1]
	while x % divisible_by != 0:
		x -= 1
	while y % divisible_by != 0:
		y -= 1
	cropped = image.crop([0,0, x, y])
	return cropped

def has_transparency(img: Image) -> bool:
	if img.info.get("transparency", None) is not None:
		return True
	if img.mode == "P":
		transparent = img.info.get("transparency", -1)
		for _, index in img.getcolors():
			if index == transparent:
				return True
	elif img.mode == "RGBA":
		extrema = img.getextrema()
		if extrema[3][0] < 255:
			return True

	return False

def is_video_file(file_path: str) -> bool:
	video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv']
	extension = file_path[file_path.rfind('.'):].lower()
	if extension in video_extensions:
		return True
	
	file_type, _ = mimetypes.guess_type(file_path)
	return file_type is not None and file_type.startswith('video/')

def resource_path(relative_path: str) -> str:
	'''Get absolute path to resource, works for dev and for PyInstaller '''
	try:
		# PyInstaller creates a temp folder and stores path in _MEIPASS
		base_path = sys._MEIPASS
	except Exception:
		base_path = os.path.abspath(".")

	return os.path.join(base_path, relative_path)

def get_execution_folder() -> str:
	if getattr(sys, 'frozen', False):
		# If the script is running as a bundled executable (e.g., PyInstaller)
		return os.path.dirname(sys.executable)
	else:
		# If the script is running as a standalone .py file
		return os.path.dirname(os.path.realpath(sys.argv[0]))