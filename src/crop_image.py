from PIL import Image

class CropImage():
	def __init__(self, path_to_image) -> None:
		self.image = path_to_image
	
	def crop_to_make_divisible(self, chunk_size=16) -> Image:
		with Image.open(self.image, "r") as img:
			x = img.size[0]
			y = img.size[1]
			while x % chunk_size != 0:
				x -= 1
			while y % chunk_size != 0:
				y -= 1
			cropped = img.crop([0,0, x, y])
			return cropped