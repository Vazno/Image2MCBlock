from PIL import Image

def resize_image(image: Image, scale_factor: int) -> Image:
	# Calculate the new size based on the scale factor
	new_size = (int(image.width * scale_factor), int(image.height * scale_factor))

	# Resize the image
	resized_image = image.resize(new_size)

	return resized_image
