from typing import Dict

from PIL import Image, ImageStat

from .utils import has_transparency, resource_path

class CalculateMinecraftBlocksMedian:
	def __init__(self, blocks: Dict, png_atlas_filename: str) -> None:
		self.PNG_ATLAS_FILENAME = png_atlas_filename
		self.blocks = blocks

	def get_blocks_with_rgb_medians(self) -> Dict:
		'''Returns list with blocks, and adds list with medians in each channel (RGB)'''
		blocks_with_median = dict()
		with Image.open(resource_path(self.PNG_ATLAS_FILENAME), "r") as blocks_image:
			for block in self.blocks:
				block_val = self.blocks[block]
				cropped = blocks_image.crop([block_val["x"], block_val["y"], block_val["x"]+16, block_val["y"]+16])
				median = ImageStat.Stat(cropped).median
				if not has_transparency(cropped):
					blocks_with_median.update({block: {"x": block_val["x"], "y": block_val["y"], "median": [median[0],median[1], median[2]]}})
				
		return blocks_with_median
