import re
from typing import List, Dict
import requests

from .utils import resource_path

class ValidBlocksClient:
	def __init__(self, txt_atlas_filename: str) -> None:
		self.LINK_TO_BLOCKS_LIST = "https://raw.githubusercontent.com/Yurihaia/mc-nbtdoc/master/minecraft/generated/item.nbtdoc"
		self.BLOCK_INFO_PLACE_PATTERN = r"minecraft:block/([\w]+)	x=(\d+)	y=(\d+)"
		self.NBTDOC_START = '::minecraft::item::blockitem::BlockItem describes minecraft:item['
		self.NBTDOC_END = '];'
		self.TXT_ATLAS_FILENAME = txt_atlas_filename
		self.response = requests.get(self.LINK_TO_BLOCKS_LIST)

	def _get_valid_blocks_list_from_response(self) -> List[str]:
		'''Function for reading .nbtdoc file, and getting list of all valid blocks (that can be placed)'''
		start = False
		valid_blocks = list()
		for line in self.response.text.split("\n"):
			if line == self.NBTDOC_END:
				start = False
			if start:
				valid_blocks.append(line.removeprefix("\tminecraft:").removesuffix(","))
			if line == self.NBTDOC_START:
				start = True
		return valid_blocks

	def _get_valid_blocks_list_from_atlas(self) -> Dict:
		'''Parses txt atlas file, and returns list of blocks.'''
		blocks = list()
		changed_blocks = dict()
		with open(resource_path(self.TXT_ATLAS_FILENAME), "r") as atlas_fp:
			blocks = re.findall(self.BLOCK_INFO_PLACE_PATTERN, atlas_fp.read())
			for name, x, y in blocks:
				changed_blocks.update({name: {"x": int(x), "y": int(y)}})
		return changed_blocks

	def exclude_invalid_blocks(self) -> Dict:
		'''Gets block list from get_valid_blocks_list_from_atlas function
		and from get_valid_blocks_list_from_response, then excludes everything that's not in the
		list from get_valid_blocks_list_from_response'''
		valid = dict()

		response_blocks = self._get_valid_blocks_list_from_response()
		atlas_blocks: Dict = self._get_valid_blocks_list_from_atlas()
		for valid_block in response_blocks:
			try:
				valid.update({valid_block: atlas_blocks[valid_block]})
			except KeyError:
				pass
		return valid
