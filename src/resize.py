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