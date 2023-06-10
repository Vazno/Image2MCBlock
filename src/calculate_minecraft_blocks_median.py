from typing import List, Tuple

from PIL import Image, ImageStat

from .utils import has_transparency, resource_path

class CalculateMinecraftBlocksMedian:
	def __init__(self, blocks: List[Tuple[str, int, int]], png_atlas_filename: str) -> None:
		self.PNG_ATLAS_FILENAME = png_atlas_filename
		self.blocks = blocks

	def get_blocks_with_rgb_medians(self) -> List[Tuple[str, int, int, Tuple[int, int, int]]]:
		'''Returns list with blocks, and adds list with medians in each channel (RGB)'''
		blocks_with_median = list()
		with Image.open(resource_path(self.PNG_ATLAS_FILENAME), "r") as blocks_image:
			for name, x, y in self.blocks:
				cropped = blocks_image.crop([x, y, x+16, y+16])
				median = ImageStat.Stat(cropped).median
				if not has_transparency(cropped):
					blocks_with_median.append([name, x, y, [median[0],median[1], median[2]]])
		return blocks_with_median
