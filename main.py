import sys
import argparse

from src.launch import Launch
from src.gui import GUI
from src.utils import resource_path

def main():
	parser = argparse.ArgumentParser(description='Launch class arguments')
	
	parser.add_argument('-gui', action='store_true')

	# Add the required arguments
	parser.add_argument('--path_to_file', required='-gui' not in sys.argv, type=str, help='Path to the input file')
	parser.add_argument('--output_file', required='-gui' not in sys.argv, type=str, help='Path to the output file')

	# Add the optional arguments
	parser.add_argument('--filter', nargs='+', help='Filter options')
	parser.add_argument('--scale_factor', type=int, help='Scale factor', default=0)
	parser.add_argument('--method', type=str, choices=["abs_diff", "euclidean"], help='Method of finding the closest color to block', default="euclidean", required=False)
	parser.add_argument('--png_atlas_filename', type=str, default=resource_path('minecraft_textures_atlas_blocks.png_0.png'), help='PNG atlas filename')
	parser.add_argument('--txt_atlas_filename', type=str, default=resource_path('minecraft_textures_atlas_blocks.png.txt'), help='TXT atlas filename')

	args = parser.parse_args()

	if(args.gui):
		gui = GUI()
		gui.mainloop()
	else:
		launch = Launch(args.filter,
		args.scale_factor,
		args.method,
		args.png_atlas_filename,
		args.txt_atlas_filename)
		launch.convert(args.path_to_file, args.output_file)

if __name__ == "__main__":
	main()