<center>
<img src="https://github.com/Vazno/Image2MCBlock/assets/96925396/b81e703f-14b4-434e-835b-6926649f0971" alt="Image2MCBlock">
</center>
<h6 align="center">Convert images to minecraft blockerized image</h6>

---
## Installation
To install Image2MCBlock, download repo, and simply use pip:

`pip install -r requirements.txt`

## How to run:
```
usage: main.py [-h] [--png_atlas_filename PNG_ATLAS_FILENAME]
               [--txt_atlas_filename TXT_ATLAS_FILENAME]
               path_to_old_image path_to_new_image

Launch application

positional arguments:
  path_to_old_image     Path to the old image
  path_to_new_image     Path to the new image

optional arguments:
  -h, --help            show this help message and exit
  --png_atlas_filename PNG_ATLAS_FILENAME
                        PNG atlas filename (default: minecraft_textures_atlas_blocks.png_0.png)
  --txt_atlas_filename TXT_ATLAS_FILENAME
                        TXT atlas filename (default: minecraft_textures_atlas_blocks.png.txt)
```
### Example:
`python main.py old_image.png blockerized_image.png`
