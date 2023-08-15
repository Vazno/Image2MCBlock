import os
import json
import pathlib
from typing import List, Literal, Dict

import argparse
import moviepy.editor as mp
from PIL import Image
from tqdm import tqdm

from src import calculate_minecraft_blocks_median
from src import crop_image
from src import download
from src import resize
from src import convert_video
from src.utils import is_video_file, resource_path, get_execution_folder
from src import generate_schematic
from src import find_closest


class Launch:
	def __init__(self, filter: List[str] = None,
			scale_factor: int = 0,
		    method: Literal["abs_diff", "euclidean", "chebyshev_distance", "manhattan_distance", "cosine_similarity", "hamming_distance", "canberra_distance"] = "canberra_distance",
		    compression_level: int = 16,
			png_atlas_filename: str=resource_path("minecraft_textures_atlas_blocks.png_0.png"),
			txt_atlas_filename: str=resource_path("minecraft_textures_atlas_blocks.png.txt")) -> None:

		self.PNG_ATLAS_FILENAME = png_atlas_filename
		self.TXT_ATLAS_FILENAME = txt_atlas_filename
		self.CACHE_FILENAME = os.path.join(get_execution_folder(), "blocks.json")
		self.method = method

		self.scale_factor = scale_factor

		self.blocks_image = Image.open(self.PNG_ATLAS_FILENAME, "r")
		

		blocks = self._get_blocks_from_cache()

		if filter:
			filtered_blocks = list()
			for block in blocks:
				if block[0] in filter:
					filtered_blocks.append(block)
			blocks = filtered_blocks

		self.blocks = blocks


		method_settings = find_closest.Method(self.blocks, compression_level=compression_level)
		if self.method == "euclidean":
			self.method = method_settings.find_closest_block_euclidean_distance
		elif self.method == "abs_diff":
			self.method = method_settings.find_closest_block_rgb_abs_diff
		elif self.method == "chebyshev_distance":
			self.method = method_settings.find_closest_block_chebyshev_distance
		elif self.method == "manhattan_distance":
			self.method = method_settings.find_closest_block_manhattan_distance
		elif self.method == "cosine_similarity":
			self.method = method_settings.find_closest_block_cosine_similarity
		elif self.method == "hamming_distance":
			self.method = method_settings.find_closest_block_hamming_distance
		elif self.method == "canberra_distance":
			self.method = method_settings.find_closest_block_canberra_distance

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

	def convert(self, path: str, output_path: str, show_progress: bool = True) -> None:
		if is_video_file(path):
			video = mp.VideoFileClip(path)
			converted_video = convert_video.process_video_with_pil(video, self.convert_image)
			converted_video.write_videofile(output_path, fps=video.fps, logger=None if not show_progress else "bar")

		elif output_path.endswith(".schem"):
			with Image.open(path, "r") as img:
				generate_schematic.create_2d_schematic(
					self.get_blocks_2d_matirx(img, show_progress=show_progress),
					output_path)

		else:
			with Image.open(path, "r") as img:
				converted_image = self.convert_image(img, show_progress=show_progress)
				converted_image.save(output_path)

	def preprocess_image(self, image: Image) -> Image:
		image_cropper = crop_image.CropImage(image)
		cropped_image = image_cropper.crop_to_make_divisible()
		if cropped_image.mode != 'RGB':
			cropped_image = cropped_image.convert('RGB')
		if self.scale_factor > 0 or self.scale_factor < 0:
			cropped_image = resize.resize_image(cropped_image, self.scale_factor)

		return cropped_image

	def get_blocks_2d_matirx(self, image: Image, show_progress: bool = False) -> List[List[str]]:
		'''Returns a matrix of strings containing block names.'''
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

				closest_block = self.method(chunk)
				blocks_matrix[-1].append(closest_block[0])

				progress_bar.update(1)

		# Close the progress bar
		progress_bar.close()
		return blocks_matrix

	def convert_image(self, image: Image, show_progress: bool = False) -> Image:
		# TODO: Use get_blocks_2d_matirx to not repeat the code
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

				closest_block = self.method(chunk)
				preprocessed_image.paste(
					self.blocks_image.crop([self.blocks[closest_block]["x"],
					self.blocks[closest_block]["y"], self.blocks[closest_block]["x"]+16,
					self.blocks[closest_block]["y"]+16]), [left,upper,right,lower]
					)
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
	parser.add_argument('--compression_level', type=int, help='Compression level, greatly improves conversion speed, and loses some information along the way, do not set higher then 20, as it will cause very high memory consumption.', default=16)
	parser.add_argument('--method', type=str,
		    choices=["abs_diff", "euclidean", "chebyshev_distance", "manhattan_distance", "cosine_similarity", "hamming_distance", "canberra_distance"], help='Method of finding the closest color to block', default="canberra_distance", required=False)
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