from colorsys import rgb_to_hsv

from PIL import Image, ImageStat
from scipy.spatial.distance import cosine

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

class Method:
	def __init__(self, blocks, compression_level: int = 16) -> None:
		self.compression_level = compression_level
		self.caching = dict()
		self.blocks = blocks

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

	def find_closest_block_cosine_similarity(self, chunk: Image) -> str:
		'''Calculates the median value of an input image.
		Then compares this median to the medians for each block,
		and returns the block with the closest match based on the cosine similarity between its RGB values and the median of the input image.
		If there are multiple blocks with equal maximum similarity, it will return the first one encountered.
		'''
		og_median = tuple(ImageStat.Stat(chunk).median)
		og_median_rgb = tuple([og_median[0], og_median[1], og_median[2]])
		
		if og_median_rgb in self.caching:
			return self.caching[og_median_rgb]
		else:
			closest_block = None
			max_similarity = -1
			
			for block in self.blocks:
				block_rgb = self.blocks[block]["median"]
				similarity = 1 - cosine(og_median_rgb, block_rgb)
				
				if similarity > max_similarity:
					max_similarity = similarity
					closest_block = block
			
			self.caching[og_median_rgb] = closest_block
			new_dict = dict()
			new_dict[og_median_rgb] = closest_block
			all_permutations = generate_color_variations(new_dict, self.compression_level)
			self.caching.update(all_permutations)
			return closest_block

	def find_closest_block_minkowski_distance(self, chunk: Image, p: int=2) -> str:
		'''Calculates the median value of an input image.
		Then compares this median to the medians for each block,
		and returns the block with the closest match based on the Minkowski distance between its RGB values and the median of the input image.
		If there are multiple blocks with equal minimum distance, it will return the first one encountered.
		'''
		og_median = tuple(ImageStat.Stat(chunk).median)
		og_median_rgb = tuple([og_median[0], og_median[1], og_median[2]])

		if og_median_rgb in self.caching:
			return self.caching[og_median_rgb]
		else:
			closest_block = None
			min_distance = float('inf')

			for block in self.blocks:
				block_rgb = self.blocks[block]["median"]
				distance = sum(abs(a - b) ** p for a, b in zip(og_median_rgb, block_rgb)) ** (1 / p)

				if distance < min_distance:
					min_distance = distance
					closest_block = block

			self.caching[og_median_rgb] = closest_block
			new_dict = dict()
			new_dict[og_median_rgb] = closest_block
			all_permutations = generate_color_variations(new_dict, self.compression_level)
			self.caching.update(all_permutations)
			return closest_block

	def find_closest_block_manhattan_distance(self, chunk: Image) -> str:
		return self.find_closest_block_minkowski_distance(chunk, 1)

	def find_closest_block_euclidean_distance(self, chunk: Image) -> str:
		return self.find_closest_block_minkowski_distance(chunk, 2)

	def find_closest_block_chebyshev_distance(self, chunk: Image) -> str:
		return self.find_closest_block_minkowski_distance(chunk, 3)

	def find_closest_block_taxicab_distance(self, chunk: Image) -> str:
		return self.find_closest_block_minkowski_distance(chunk, 4)

	def find_closest_block_hamming_distance(self, chunk: Image) -> str:
		'''Calculates the median value of an input image.
		Then compares this median to the medians for each block,
		and returns the block with the closest match based on the Hamming distance between its RGB values and the median of the input image.
		If there are multiple blocks with equal minimum distance, it will return the first one encountered.
		'''
		og_median = tuple(ImageStat.Stat(chunk).median)
		og_median_rgb = tuple([og_median[0], og_median[1], og_median[2]])

		if og_median_rgb in self.caching:
			return self.caching[og_median_rgb]
		else:
			closest_block = None
			min_distance = float('inf')

			for block in self.blocks:
				block_rgb = self.blocks[block]["median"]
				distance = sum(a != b for a, b in zip(og_median_rgb, block_rgb))

				if distance < min_distance:
					min_distance = distance
					closest_block = block

			self.caching[og_median_rgb] = closest_block
			new_dict = dict()
			new_dict[og_median_rgb] = closest_block
			all_permutations = generate_color_variations(new_dict, self.compression_level)
			self.caching.update(all_permutations)
			return closest_block

	def find_closest_block_canberra_distance(self, chunk: Image) -> str:
		'''Calculates the median value of an input image.
		Then compares this median to the medians for each block,
		and returns the block with the closest match based on the Canberra distance between its RGB values and the median of the input image.
		If there are multiple blocks with equal minimum distance, it will return the first one encountered.
		'''
		og_median = tuple(ImageStat.Stat(chunk).median)
		og_median_rgb = tuple([og_median[0], og_median[1], og_median[2]])

		if og_median_rgb in self.caching:
			return self.caching[og_median_rgb]
		else:
			closest_block = None
			min_distance = float('inf')

			for block in self.blocks:
				block_rgb = self.blocks[block]["median"]
				distance = sum(
					abs(a - b) / (abs(a) + abs(b)) if abs(a) + abs(b) != 0 else float('inf')
					for a, b in zip(og_median_rgb, block_rgb)
				)

				if distance < min_distance:
					min_distance = distance
					closest_block = block

			self.caching[og_median_rgb] = closest_block
			new_dict = dict()
			new_dict[og_median_rgb] = closest_block
			all_permutations = generate_color_variations(new_dict, self.compression_level)
			self.caching.update(all_permutations)
			return closest_block