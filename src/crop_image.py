from PIL import Image

class CropImage():
	def __init__(self, image: Image) -> None:
		self.image = image
	
	def crop_to_make_divisible(self, chunk_size=16) -> Image:
		x = self.image.size[0]
		y = self.image.size[1]
		while x % chunk_size != 0:
			x -= 1
		while y % chunk_size != 0:
			y -= 1
		cropped = self.image.crop([0,0, x, y])
		return cropped