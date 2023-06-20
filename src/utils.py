import sys
import os
import mimetypes

from PIL import Image

def has_transparency(img: Image):
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

def is_video_file(file_path):
	video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv']
	extension = file_path[file_path.rfind('.'):].lower()
	if extension in video_extensions:
		return True
	
	file_type, _ = mimetypes.guess_type(file_path)
	return file_type is not None and file_type.startswith('video/')

def resource_path(relative_path):
	""" Get absolute path to resource, works for dev and for PyInstaller """
	try:
		# PyInstaller creates a temp folder and stores path in _MEIPASS
		base_path = sys._MEIPASS
	except Exception:
		base_path = os.path.abspath(".")

	return os.path.join(base_path, relative_path)

def get_execution_folder():
	if getattr(sys, 'frozen', False):
		# If the script is running as a bundled executable (e.g., PyInstaller)
		return os.path.dirname(sys.executable)
	else:
		# If the script is running as a standalone .py file
		return os.path.dirname(os.path.realpath(sys.argv[0]))