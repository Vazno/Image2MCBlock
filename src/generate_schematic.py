import os
from typing import List

import mcschematic

def create_2d_schematic(blocks: List[List[str]], output_path: str, bottom_block="end_stone"):
	width = len(blocks[0])
	height = len(blocks)

	schematic = mcschematic.MCSchematic()

	for y in range(height):
		for x in range(width):
			schematic.setBlock((x, 0, y), bottom_block)

	for y in range(height):
		for x in range(width):
			block = blocks[y][x]
			schematic.setBlock((x, 1, y), block)

	schem_name = os.path.splitext(os.path.basename(output_path))[0]
	output_folder = os.path.dirname(output_path)
	schematic.save(output_folder, schem_name, mcschematic.Version.JE_1_20_1)
