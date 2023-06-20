import os
import json
import pathlib
import math
from typing import List, Literal, Dict

import argparse
import moviepy.editor as mp
from PIL import Image, ImageStat
from tqdm import tqdm

from src import calculate_minecraft_blocks_median
from src import crop_image
from src import download
from src import resize
from src import convert_video
from src.utils import is_video_file, resource_path, get_execution_folder
from src import generate_schematic

def generate_color_variations(color_dict, max_abs_difference=16):
	new_dict = {}
	
	for rgb_tuple, value in color_dict.items():
		r, g, b = rgb_tuple
		
		for dr in range(-max_abs_difference, max_abs_difference + 1):
			new_r = r + dr
			
			if not 0 <= new_r <= 255:
				continue
			
			for dg in range(-max_abs_difference, max_abs_difference + 1):
				new_g = g + dg
				
				if not 0 <= new_g <= 255:
					continue
				
				for db in range(-max_abs_difference, max_abs_difference + 1):
					new_b = b + db
					
					if 0 <= new_b <= 255:
						total_diff = abs(new_r - r) + abs(new_g - g) + abs(new_b - b)
						
						if total_diff <= max_abs_difference:
							new_rgb_tuple = (new_r, new_g, new_b)
							new_dict[new_rgb_tuple] = value
	
	return new_dict

class Launch:
	def __init__(self, filter: List[str] = None,
			scale_factor: int = 0,
		    method: Literal["abs_diff", "euclidean"] = "euclidean",
		    compression_level: int = 16,
			png_atlas_filename: str=resource_path("minecraft_textures_atlas_blocks.png_0.png"),
			txt_atlas_filename: str=resource_path("minecraft_textures_atlas_blocks.png.txt")) -> None:

		self.PNG_ATLAS_FILENAME = png_atlas_filename
		self.TXT_ATLAS_FILENAME = txt_atlas_filename
		self.CACHE_FILENAME = os.path.join(get_execution_folder(), "blocks.json")
		self.method = method

		if self.method == "euclidean":
			self.method = self.find_closest_block_euclidean_distance
		elif self.method == "abs_diff":
			self.method = self.find_closest_block_rgb_abs_diff

		self.scale_factor = scale_factor
		self.compression_level = compression_level

		self.blocks_image = Image.open(self.PNG_ATLAS_FILENAME, "r")
		self.caching = dict()

		blocks = self._get_blocks_from_cache()

		if filter:
			filtered_blocks = list()
			for block in blocks:
				if block[0] in filter:
					filtered_blocks.append(block)
			blocks = filtered_blocks

		self.blocks = blocks

	def _get_blocks_from_cache(self) -> Dict:
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

	def find_closest_block_rgb_abs_diff(self, chunk: Image) -> str:
		'''Calculates the median value of an input image.
		Then compares this median to the medians for each block,
		and returns the block with the closest match based on the sum of absolute differences between its RGB values and the median of the input image.
		If there are multiple blocks with equal minimum difference, it will return the first one encountered.
		'''
		og_median = tuple(ImageStat.Stat(chunk).median)
		og_median_rgb = tuple([og_median[0], og_median[1], og_median[2]])
		if og_median_rgb in self.caching:
			return self.caching[og_median_rgb]
		else:
			rgb_closests_diff = []
			for channel in range(3):
				min_diff = float('inf')
				for block in self.blocks:
					diff = abs(og_median_rgb[channel] - self.blocks[block]["median"][channel])
					if diff < min_diff:
						min_diff = diff
						min_diff_block = block
				rgb_closests_diff.append(min_diff_block)
			
			lowest_difference = float("inf")
			lowest_block = None
			for block in rgb_closests_diff:
				difference = sum(abs(a - b) for a, b in zip(self.blocks[block]["median"], og_median_rgb))
				if difference < lowest_difference:
					lowest_difference = difference
					lowest_block = block
			
			self.caching[og_median_rgb] = lowest_block
			new_dict = dict()
			new_dict[og_median_rgb] = lowest_block
			all_permutations = generate_color_variations(new_dict, self.compression_level)
			self.caching.update(all_permutations)
			return lowest_block

	def find_closest_block_euclidean_distance(self, chunk: Image) -> str:
		# Calculate the median RGB values of the input image
		og_median = ImageStat.Stat(chunk).median
		og_median_rgb = tuple([og_median[0], og_median[1], og_median[2]])

		# Checking if the median is in caching
		if og_median_rgb in self.caching:
			return self.caching[og_median_rgb]

		else:
			# Initialize variables for tracking the closest block
			closest_block = None
			min_distance = math.inf

			# Iterate over each block and calculate the Euclidean distance
			for block in self.blocks:
				block_rgb = self.blocks[block]["median"]
				distance = math.sqrt(sum((a - b) ** 2 for a, b in zip(og_median, block_rgb)))

				# Update closest block if a closer match is found
				if distance < min_distance:
					min_distance = distance
					closest_block = block

			self.caching[og_median_rgb] = closest_block
			new_dict = dict()
			new_dict[og_median_rgb] = closest_block
			all_permutations = generate_color_variations(new_dict, self.compression_level)
			self.caching.update(all_permutations)
			return closest_block

	def convert(self, path: str, output_path: str, show_progress: bool = True) -> None:
		if output_path.endswith(".schem"):
			with Image.open(path, "r") as img:
				generate_schematic.create_2d_schematic(
					self.get_blocks_2d_matirx(img, show_progress=show_progress),
					output_path)

		elif is_video_file(path):
			video = mp.VideoFileClip(path)
			converted_video = convert_video.process_video_with_pil(video, self.convert_image)
			converted_video.write_videofile(output_path, fps=video.fps, logger=None if not show_progress else "bar")
		else:
			with Image.open(path, "r") as img:
				converted_image = self.convert_image(img, show_progress=show_progress)
				converted_image.save(output_path)

	def preprocess_image(self, image: Image) -> Image:
		image_cropper = crop_image.CropImage(image)
		cropped_image = image_cropper.crop_to_make_divisible()

		if self.scale_factor > 0 or self.scale_factor < 0:
			cropped_image = resize.resize_image(cropped_image, self.scale_factor)

		return cropped_image

	def get_blocks_2d_matirx(self, image: Image, show_progress: bool = False) -> List[List[str]]:
		preprocessed_image = self.preprocess_image(image)
		width, height = preprocessed_image.size
		chunks_x = width // 16
		chunks_y = height // 16

		total_iterations = chunks_x*chunks_y
		# Create a progress bar
		progress_bar = tqdm(total=total_iterations, disable=not show_progress)

		blocks_matrix = list()
		for x in range(chunks_x):
			blocks_matrix.append(list())
			for y in range(chunks_y):
				left = x * 16
				upper = y * 16
				right = left + 16
				lower = upper + 16
				chunk = preprocessed_image.crop((left, upper, right, lower))

				lowest_block = self.method(chunk)
				blocks_matrix[-1].append(lowest_block[0])

				progress_bar.update(1)

		# Close the progress bar
		progress_bar.close()
		return blocks_matrix

	def convert_image(self, image: Image, show_progress: bool = False) -> Image:
		preprocessed_image = self.preprocess_image(image)

		width, height = preprocessed_image.size
		chunks_x = width // 16
		chunks_y = height // 16

		total_iterations = chunks_x * chunks_y
		# Create a progress bar
		progress_bar = tqdm(total=total_iterations, disable=not show_progress)

		for x in range(chunks_x):
			for y in range(chunks_y):
				left = x * 16
				upper = y * 16
				right = left + 16
				lower = upper + 16
				chunk = preprocessed_image.crop((left, upper, right, lower))

				lowest_block = self.method(chunk)
				preprocessed_image.paste(self.blocks_image.crop([self.blocks[lowest_block]["x"], self.blocks[lowest_block]["y"], self.blocks[lowest_block]["x"]+16, self.blocks[lowest_block]["y"]+16]), [left,upper,right,lower])
				progress_bar.update(1)

		# Close the progress bar
		progress_bar.close()
		return preprocessed_image

def main():
	parser = argparse.ArgumentParser(description='Launch class arguments')

	# Add the required arguments
	parser.add_argument('path_to_file', type=str, help='Path to the input file')
	parser.add_argument('output_file', type=str, help='Path to the output file')

	# Add the optional arguments
	parser.add_argument('--filter', nargs='+', help='Filter options')
	parser.add_argument('--scale_factor', type=int, help='Scale factor', default=0)
	parser.add_argument('--compression_level', type=int, help='Compression level, greatly improves conversion speed, and loses some information along the way, do not go higher than 20, as it will cause very high memory consumption.', default=16)
	parser.add_argument('--method', type=str, choices=["abs_diff", "euclidean"], help='Method of finding the closest color to block', default="euclidean", required=False)
	parser.add_argument('--png_atlas_filename', type=str, default=resource_path('minecraft_textures_atlas_blocks.png_0.png'), help='PNG atlas filename')
	parser.add_argument('--txt_atlas_filename', type=str, default=resource_path('minecraft_textures_atlas_blocks.png.txt'), help='TXT atlas filename')

	args = parser.parse_args()

	launch = Launch(args.filter,
		args.scale_factor,
		args.method,
		args.compression_level,
		args.png_atlas_filename,
		args.txt_atlas_filename)
	launch.convert(args.path_to_file, args.output_file)

if __name__ == "__main__":
	main()