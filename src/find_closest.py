from typing import Tuple, Callable, Any

from PIL import Image, ImageStat
from scipy.spatial.distance import cosine

def generate_color_variations(color_dict, max_abs_difference=16):
	'''Creates color combinations in given max_abs_difference.'''
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

class Method:
	def __init__(self, blocks, compression_level: int = 16) -> None:
		self.compression_level = compression_level
		self.cache = dict()
		self.blocks = blocks

	def add_to_caching(self, median_rgb: Tuple[int, int, int], closest_block: str):
		self.cache[median_rgb] = closest_block
		new_dict = dict()
		new_dict[median_rgb] = closest_block
		all_permutations = generate_color_variations(new_dict, self.compression_level)
		self.cache.update(all_permutations)

	def check_caching(func: Callable[..., Any]):
		'''Checks if chunk was already cached, and if so returns cached closest block.'''
		def wrapper(self, chunk, *args, **kwargs):
			img_median = tuple(ImageStat.Stat(chunk).median)
			if img_median in self.cache:
				return self.cache[img_median]
			else:
				return func(self, chunk, *args, **kwargs)
		return wrapper

	@check_caching
	def find_closest_block_rgb_abs_diff(self, chunk: Image) -> str:
		'''Calculates the median value of an input image.
		Then compares this median to the medians for each block,
		and returns the block with the closest match based on the sum of absolute differences between its RGB values and the median of the input image.
		If there are multiple blocks with equal minimum difference, it will return the first one encountered.
		'''
		img_median = tuple(ImageStat.Stat(chunk).median)

		rgb_closests_diff = []
		for channel in range(3):
			min_diff = float('inf')
			for block in self.blocks:
				diff = abs(img_median[channel] - self.blocks[block]["median"][channel])
				if diff < min_diff:
					min_diff = diff
					min_diff_block = block
			rgb_closests_diff.append(min_diff_block)
		
		lowest_difference = float("inf")
		closest_block = None
		for block in rgb_closests_diff:
			difference = sum(abs(a - b) for a, b in zip(self.blocks[block]["median"], img_median))
			if difference < lowest_difference:
				lowest_difference = difference
				closest_block = block
		
		self.add_to_caching(img_median, closest_block)
		return closest_block

	@check_caching
	def find_closest_block_cosine_similarity(self, chunk: Image) -> str:
		'''Calculates the median value of an input image.
		Then compares this median to the medians for each block,
		and returns the block with the closest match based on the cosine similarity between its RGB values and the median of the input image.
		If there are multiple blocks with equal maximum similarity, it will return the first one encountered.
		'''
		img_median = tuple(ImageStat.Stat(chunk).median)

		closest_block = None
		max_similarity = -1
		
		for block in self.blocks:
			block_rgb = self.blocks[block]["median"]
			similarity = 1 - cosine(img_median, block_rgb)
			
			if similarity > max_similarity:
				max_similarity = similarity
				closest_block = block
		
		self.add_to_caching(img_median, closest_block)
		return closest_block

	@check_caching
	def find_closest_block_minkowski_distance(self, chunk: Image, p: int=2) -> str:
		'''Calculates the median value of an input image.
		Then compares this median to the medians for each block,
		and returns the block with the closest match based on the Minkowski distance between its RGB values and the median of the input image.
		If there are multiple blocks with equal minimum distance, it will return the first one encountered.
		'''
		img_median = tuple(ImageStat.Stat(chunk).median)
		closest_block = None
		min_distance = float('inf')

		for block in self.blocks:
			block_rgb = self.blocks[block]["median"]
			distance = sum(abs(a - b) ** p for a, b in zip(img_median, block_rgb)) ** (1 / p)

			if distance < min_distance:
				min_distance = distance
				closest_block = block

		self.add_to_caching(img_median, closest_block)
		return closest_block

	def find_closest_block_manhattan_distance(self, chunk: Image) -> str:
		return self.find_closest_block_minkowski_distance(chunk, 1)

	def find_closest_block_euclidean_distance(self, chunk: Image) -> str:
		return self.find_closest_block_minkowski_distance(chunk, 2)

	def find_closest_block_chebyshev_distance(self, chunk: Image) -> str:
		return self.find_closest_block_minkowski_distance(chunk, 3)

	def find_closest_block_taxicab_distance(self, chunk: Image) -> str:
		return self.find_closest_block_minkowski_distance(chunk, 4)

	@check_caching
	def find_closest_block_hamming_distance(self, chunk: Image) -> str:
		'''Calculates the median value of an input image.
		Then compares this median to the medians for each block,
		and returns the block with the closest match based on the Hamming distance between its RGB values and the median of the input image.
		If there are multiple blocks with equal minimum distance, it will return the first one encountered.
		'''
		img_median = tuple(ImageStat.Stat(chunk).median)

		closest_block = None
		min_distance = float('inf')

		for block in self.blocks:
			block_rgb = self.blocks[block]["median"]
			distance = sum(a != b for a, b in zip(img_median, block_rgb))

			if distance < min_distance:
				min_distance = distance
				closest_block = block

		self.add_to_caching(img_median, closest_block)
		return closest_block

	@check_caching
	def find_closest_block_canberra_distance(self, chunk: Image) -> str:
		'''Calculates the median value of an input image.
		Then compares this median to the medians for each block,
		and returns the block with the closest match based on the Canberra distance between its RGB values and the median of the input image.
		If there are multiple blocks with equal minimum distance, it will return the first one encountered.
		'''
		img_median = tuple(ImageStat.Stat(chunk).median)
		closest_block = None
		min_distance = float('inf')

		for block in self.blocks:
			block_rgb = self.blocks[block]["median"]
			distance = sum(
				abs(a - b) / (abs(a) + abs(b)) if abs(a) + abs(b) != 0 else float('inf')
				for a, b in zip(img_median, block_rgb)
			)

			if distance < min_distance:
				min_distance = distance
				closest_block = block

		self.add_to_caching(img_median, closest_block)
		return closest_block