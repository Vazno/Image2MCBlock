import os
import json
import pathlib
import math
from typing import List, Tuple, Literal

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

def generate_color_variations(color_dict, max_abs_difference):
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
		self.blocks_image = Image.open(self.PNG_ATLAS_FILENAME, "r")
		self.caching = dict()

		blocks = self._get_blocks_cached()

		if filter:
			filtered_blocks = list()
			for block in blocks:
				if block[0] in filter:
					filtered_blocks.append(block)
			blocks = filtered_blocks

		self.blocks = blocks

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
		og_median_rgb = tuple([og_median[0], og_median[1], og_median[2]])

		if og_median_rgb in self.caching:
			return self.caching[og_median_rgb]
		else:

			rgb_closests_diff = list()
			for channel in range(3):
				min_diff_block = min(self.blocks, key=lambda x: abs(og_median[channel] - x[3][channel]))
				rgb_closests_diff.append(min_diff_block)

			closest_block = min(rgb_closests_diff, key=lambda x: sum(abs(a - b) for a, b in zip(x[3], og_median)))
			self.caching[og_median_rgb] = closest_block
			new_dict = dict()
			new_dict[og_median_rgb] = closest_block
			all_permutations = generate_color_variations(new_dict, 15)
			self.caching.update(all_permutations)
			return closest_block

	def find_closest_block_euclidean_distance(self, chunk: Image):
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
				block_rgb = block[3]
				distance = math.sqrt(sum((a - b) ** 2 for a, b in zip(og_median, block_rgb)))

				# Update closest block if a closer match is found
				if distance < min_distance:
					min_distance = distance
					closest_block = block

			self.caching[og_median_rgb] = closest_block
			new_dict = dict()
			new_dict[og_median_rgb] = closest_block
			all_permutations = generate_color_variations(new_dict, 15)
			self.caching.update(all_permutations)
			return closest_block

	def convert(self, path: str, output_path: str, show_progress: bool = True) -> None:
		if is_video_file(path):
			video = mp.VideoFileClip(path)
			converted_video = convert_video.process_video_with_pil(video, self.create_new_image)
			converted_video.write_videofile(output_path, fps=video.fps, progressbar=show_progress)
		else:
			with Image.open(path, "r") as img:
				converted_image = self.create_new_image(img, show_progress=show_progress)
				converted_image.save(output_path)

	def create_new_image(self, image: Image, show_progress: bool = False) -> Image:
		image_cropper = crop_image.CropImage(image)
		cropped_old_image = image_cropper.crop_to_make_divisible()

		if self.scale_factor > 0 or self.scale_factor < 0:
			cropped_old_image = resize.resize_image(cropped_old_image, self.scale_factor)

		width, height = cropped_old_image.size
		chunks_x = width // 16
		chunks_y = height // 16

		total_iterations = chunks_x*chunks_y
		# Create a progress bar
		progress_bar = tqdm(total=total_iterations, disable=not show_progress)

		for x in range(chunks_x):
			for y in range(chunks_y):
				left = x * 16
				upper = y * 16
				right = left + 16
				lower = upper + 16
				chunk = cropped_old_image.crop((left, upper, right, lower))

				lowest_block = self.method(chunk)

				cropped_old_image.paste(self.blocks_image.crop([lowest_block[1], lowest_block[2], lowest_block[1]+16, lowest_block[2]+16]), [left,upper,right,lower])
				progress_bar.update(1)

		# Close the progress bar
		progress_bar.close()
		return cropped_old_image

def main():
	parser = argparse.ArgumentParser(description='Launch class arguments')

	# Add the required arguments
	parser.add_argument('path_to_file', type=str, help='Path to the input file')
	parser.add_argument('output_file', type=str, help='Path to the output file')

	# Add the optional arguments
	parser.add_argument('--filter', nargs='+', help='Filter options')
	parser.add_argument('--scale_factor', type=int, help='Scale factor', default=0)
	parser.add_argument('--method', type=str, choices=["abs_diff", "euclidean"], help='Method of finding the closest color to block', default="euclidean", required=False)
	parser.add_argument('--png_atlas_filename', type=str, default=resource_path('minecraft_textures_atlas_blocks.png_0.png'), help='PNG atlas filename')
	parser.add_argument('--txt_atlas_filename', type=str, default=resource_path('minecraft_textures_atlas_blocks.png.txt'), help='TXT atlas filename')

	args = parser.parse_args()

	launch = Launch(args.filter,
		args.scale_factor,
		args.method,
		args.png_atlas_filename,
		args.txt_atlas_filename)
	launch.convert(args.path_to_file, args.output_file)

if __name__ == "__main__":
	main()