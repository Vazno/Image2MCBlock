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