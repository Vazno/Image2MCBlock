import json
import pathlib
import math
from typing import List, Tuple, Literal

import argparse
from PIL import Image, ImageStat

from src import calculate_minecraft_blocks_median
from src import crop_image
from src import download
from src import resize

class Launch:
	def __init__(self, path_to_old_image:str, path_to_new_image:str,
	      	filter: List[str] = None, scale_factor: int = 0,
		    method: Literal["abs_diff", "euclidean"] = "euclidean",
			png_atlas_filename: str="minecraft_textures_atlas_blocks.png_0.png",
			txt_atlas_filename:str="minecraft_textures_atlas_blocks.png.txt") -> None:

		self.PNG_ATLAS_FILENAME = png_atlas_filename
		self.TXT_ATLAS_FILENAME = txt_atlas_filename
		self.path_to_old_image = path_to_old_image
		self.path_to_new_image = path_to_new_image
		self.CACHE_FILENAME = "blocks.json"
		self.scale_factor = scale_factor
		self.method = method

		blocks = self._get_blocks_cached()

		if filter:
			filtered_blocks = list()
			for block in blocks:
				if block[0] in filter:
					filtered_blocks.append(block)
			blocks = filtered_blocks

		self.blocks = blocks

		self.old_image = crop_image.CropImage(path_to_old_image)
		self.cropped_old_image = self.old_image.crop_to_make_divisible()

		if scale_factor > 0:
			self.cropped_old_image = resize.resize_image(self.cropped_old_image, self.scale_factor)


	def _get_blocks_cached(self) -> List[Tuple[str, int, int, Tuple[int, int, int]]]:
		'''Gets the blocks from cache, and if it doesn't exist, re-validate everything from internet,
		and cache blocks and their medians.'''
		if pathlib.Path(self.CACHE_FILENAME).exists():
			with open(self.CACHE_FILENAME, "r") as f:
				blocks = json.load(f)
		else:
			valid_client = download.ValidBlocksClient(self.TXT_ATLAS_FILENAME)
			blocks = valid_client.exclude_invalid_blocks()

			calculate_median = calculate_minecraft_blocks_median.CalculateMinecraftBlocksMedian(blocks, self.PNG_ATLAS_FILENAME)
			blocks = calculate_median.get_blocks_with_rgb_medians()

			with open(self.CACHE_FILENAME, "w") as f:
				json.dump(blocks, f, indent=4)
		return blocks

	def find_closest_block_rgb_abs_diff(self, chunk: Image):
		'''Calculates the median value of an input image.
		Then compares this median to the medians for each block,
		and returns the block with the closest match based on the sum of absolute differences between its RGB values and the median of the input image.
		If there are multiple blocks with equal minimum difference, it will return the first one encountered.
		'''
		og_median = ImageStat.Stat(chunk).median

		rgb_closests_diff = list()
		for channel in range(3):
			min_diff_block = min(self.blocks, key=lambda x: abs(og_median[channel] - x[3][channel]))
			rgb_closests_diff.append(min_diff_block)

		closest_block = min(rgb_closests_diff, key=lambda x: sum(abs(a - b) for a, b in zip(x[3], og_median)))
		return closest_block

	def find_closest_block_euclidean_distance(self, chunk: Image):
		# Calculate the median RGB values of the input image
		og_median = ImageStat.Stat(chunk).median

		# Initialize variables for tracking the closest block
		closest_block = None
		min_distance = math.inf

		# Iterate over each block and calculate the Euclidean distance
		for block in self.blocks:
			block_rgb = block[3]
			distance = math.sqrt(sum((a - b) ** 2 for a, b in zip(og_median, block_rgb)))

			# Update closest block if a closer match is found
			if distance < min_distance:
				min_distance = distance
				closest_block = block

		return closest_block

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

				if self.method == "euclidean":
					lowest_block = self.find_closest_block_euclidean_distance(chunk)
				elif self.method == "abs_diff":
					lowest_block = self.find_closest_block_rgb_abs_diff(chunk)

				self.cropped_old_image.paste(blocks_image.crop([lowest_block[1], lowest_block[2], lowest_block[1]+16, lowest_block[2]+16]), [left,upper,right,lower])

		self.cropped_old_image.save(self.path_to_new_image)

def main():
	parser = argparse.ArgumentParser(description='Launch class arguments')

	# Add the required arguments
	parser.add_argument('path_to_old_image', type=str, help='Path to the old image')
	parser.add_argument('path_to_new_image', type=str, help='Path to the new image')

	# Add the optional arguments
	parser.add_argument('--filter', nargs='+', help='Filter options')
	parser.add_argument('--scale_factor', type=int, help='Scale factor', default=0)
	parser.add_argument('--method', type=str, choices=["abs_diff", "euclidean"], help='Method of finding the closest color to block', default="euclidean", required=False)
	parser.add_argument('--png_atlas_filename', type=str, default='minecraft_textures_atlas_blocks.png_0.png', help='PNG atlas filename')
	parser.add_argument('--txt_atlas_filename', type=str, default='minecraft_textures_atlas_blocks.png.txt', help='TXT atlas filename')

	args = parser.parse_args()

	launch = Launch(args.path_to_old_image,
		args.path_to_new_image, args.filter,
		args.scale_factor, args.method,
		args.png_atlas_filename,
		args.txt_atlas_filename)
	launch.create_new_image()

if __name__ == "__main__":
	main()