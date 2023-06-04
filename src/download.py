import requests
import re

from typing import List, Tuple

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
				valid_blocks.append(line.removeprefix("\t").removesuffix(","))
			if line == self.NBTDOC_START:
				start = True
		return valid_blocks

	def _get_valid_blocks_list_from_atlas(self) -> List[Tuple[str, int, int]]:
		'''Parses txt atlas file, and returns list of blocks.'''
		blocks = list()
		changed_blocks = list()
		with open(self.TXT_ATLAS_FILENAME, "r") as atlas_fp:
			blocks = re.findall(self.BLOCK_INFO_PLACE_PATTERN, atlas_fp.read())
			for name, x, y in blocks:
				changed_blocks.append([name, int(x), int(y)])
		return changed_blocks

	def exclude_invalid_blocks(self) -> List[Tuple[str, int, int]]:
		'''Gets block list from get_valid_blocks_list_from_atlas function
		and from get_valid_blocks_list_from_response, then excludes everything that's not in the
		list from get_valid_blocks_list_from_response'''
		valid = list()

		for block in self._get_valid_blocks_list_from_atlas():
			for valid_block in self._get_valid_blocks_list_from_response():
				if block[0] in valid_block:
					valid.append(block)
					break
		return valid

