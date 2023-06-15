<center>
<img src="https://github.com/Vazno/Image2MCBlock/assets/96925396/b81e703f-14b4-434e-835b-6926649f0971" alt="Image2MCBlock">
</center>
<h6 align="center">Convert images or videos to minecraft blockerized file</h6>

---
## Installation
To install Image2MCBlock, download repo, and simply use pip:

`pip install -r requirements.txt`

## How to run:
```
usage: main.py [-h] [-gui] --path_to_file PATH_TO_FILE --output_file OUTPUT_FILE
               [--filter FILTER [FILTER ...]] [--scale_factor SCALE_FACTOR]
               [--method {abs_diff,euclidean}] [--png_atlas_filename PNG_ATLAS_FILENAME]
               [--txt_atlas_filename TXT_ATLAS_FILENAME]

Launch class arguments

options:
  -h, --help            show this help message and exit
  -gui                  Should the GUI be used?
  --path_to_file PATH_TO_FILE
                        Path to the input file
  --output_file OUTPUT_FILE
                        Path to the output file
  --filter FILTER [FILTER ...]
                        Filter options
  --scale_factor SCALE_FACTOR
                        Scale factor
  --method {abs_diff,euclidean}
                        Method of finding the closest color to block
  --png_atlas_filename PNG_ATLAS_FILENAME
                        PNG atlas filename
  --txt_atlas_filename TXT_ATLAS_FILENAME
                        TXT atlas filename
```
### Example:
`python main.py old_image.png blockerized_image.png`

### Filter example:
`python .\main.py old_image.png blockerized_image.png --filter gray_wool black_wool light_gray_wool`
<img src="https://github.com/Vazno/Image2MCBlock/assets/96925396/116781f7-a7f0-41b8-910b-931129c9f843" alt="Image2MCBlock">
</center>

### How to use textures from newer versions?
Code uses [Texture atlas](https://minecraft.fandom.com/wiki/Texture_atlas) from minecraft. (1.19.4)

To get the new textures of current latest update, you need to go in the last version of the game and press `F3+S`, that will generate output in chat, press it, and then copy&paste `minecraft_textures_atlas_blocks.png_0.png`, `minecraft_textures_atlas_blocks.png.txt` to the root folder.
