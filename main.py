import argparse

from PIL import Image, ImageStat

from src import calculate_minecraft_blocks_median
from src import crop_image
from src import download

class Launch:
	def __init__(self, path_to_old_image:str, path_to_new_image:str,
			png_atlas_filename: str="minecraft_textures_atlas_blocks.png_0.png",
			txt_atlas_filename:str="minecraft_textures_atlas_blocks.png.txt") -> None:
		self.PNG_ATLAS_FILENAME = png_atlas_filename
		self.TXT_ATLAS_FILENAME = txt_atlas_filename
		self.path_to_old_image = path_to_old_image
		self.path_to_new_image = path_to_new_image

		valid_client = download.ValidBlocksClient(self.TXT_ATLAS_FILENAME)
		blocks = valid_client.exclude_invalid_blocks()

		calculate_median = calculate_minecraft_blocks_median.CalculateMinecraftBlocksMedian(blocks, self.PNG_ATLAS_FILENAME)
		self.blocks = calculate_median.get_blocks_with_rgb_medians()

		self.old_image = crop_image.CropImage(path_to_old_image)
		self.cropped_old_image = self.old_image.crop_to_make_divisible()

	def calculate_median(self, chunk):
		og_median = ImageStat.Stat(chunk).median

		rgb_closests_diff = list()
		for channel in range(3):
			min_diff = float('inf')
			for name, block_x, block_y, median in self.blocks:
				diff = abs(og_median[channel] - median[channel])
				if diff < min_diff:
					min_diff = diff
					min_diff_block = [name, block_x, block_y, median, min_diff]

			rgb_closests_diff.append(min_diff_block)
			min_diff = float('inf')

		lowest_difference = float("inf")
		for block in rgb_closests_diff:
			difference = sum(abs(a - b) for a, b in zip(block[3], og_median))
			if difference < lowest_difference:
				lowest_difference = difference
				lowest_block = block

		return lowest_block

	def create_new_image(self):
		width, height = self.cropped_old_image.size
		chunks_x = width // 16
		chunks_y = height // 16

		blocks_image = Image.open(self.PNG_ATLAS_FILENAME, "r")

		for x in range(chunks_x):
			for y in range(chunks_y):
				left = x * 16
				upper = y * 16
				right = left + 16
				lower = upper + 16
				chunk = self.cropped_old_image.crop((left, upper, right, lower))

				lowest_block = self.calculate_median(chunk)

				self.cropped_old_image.paste(blocks_image.crop([lowest_block[1], lowest_block[2], lowest_block[1]+16, lowest_block[2]+16]), [left,upper,right,lower])

		self.cropped_old_image.save(self.path_to_new_image)


def main():
	parser = argparse.ArgumentParser(description="Launch application")
	parser.add_argument("path_to_old_image", type=str, help="Path to the old image")
	parser.add_argument("path_to_new_image", type=str, help="Path to the new image")
	parser.add_argument("--png_atlas_filename", type=str, default="minecraft_textures_atlas_blocks.png_0.png",
						help="PNG atlas filename (default: minecraft_textures_atlas_blocks.png_0.png)")
	parser.add_argument("--txt_atlas_filename", type=str, default="minecraft_textures_atlas_blocks.png.txt",
						help="TXT atlas filename (default: minecraft_textures_atlas_blocks.png.txt)")
	args = parser.parse_args()

	launch = Launch(args.path_to_old_image, args.path_to_new_image, args.png_atlas_filename)
	launch.create_new_image()

if __name__ == "__main__":
	main()