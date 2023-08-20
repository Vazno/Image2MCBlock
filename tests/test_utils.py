import sys
import shutil
import tempfile

import pytest
from PIL import Image

from src.utils import crop_to_make_divisible, resize_image, has_transparency, get_execution_folder

#-------------------------------------------------------------------------
@pytest.mark.parametrize("input_size, divisible_by, expected_size", [
    ((100, 100), 16, (96, 96)),
    ((50, 50), 10, (50, 50)),
    ((200, 150), 20, (200, 140)),
    ((30, 45), 5, (30, 45))])

def test_crop_to_make_divisible(input_size, divisible_by, expected_size):
    # Create a dynamic image for testing
    image = Image.new("RGB", input_size, (255, 255, 255))

    cropped_image = crop_to_make_divisible(image, divisible_by)
    assert cropped_image.size == expected_size

#-------------------------------------------------------------------------
@pytest.mark.parametrize("input_size, scale_factor, expected_size", [
    ((100, 100), 2, (200, 200)),
    ((50, 50), 0.5, (25, 25)),
    ((200, 150), -2, (100, 75)),
    ((500, 256), -4, (125, 64))])

def test_resize_image(input_size, scale_factor, expected_size):
    # Create a dynamic image for testing
    image = Image.new("RGB", input_size, (255, 255, 255))
    
    resized_image = resize_image(image, scale_factor)
    assert resized_image.size == expected_size

#-------------------------------------------------------------------------
@pytest.fixture
def transparent_image():
    img = Image.new("RGBA", (100, 100), (0, 0, 0, 0))
    return img

@pytest.fixture
def opaque_image():
    img = Image.new("RGBA", (100, 100), (255, 255, 255, 255))
    return img

def test_transparent_image(transparent_image):
    assert has_transparency(transparent_image) == True

def test_opaque_image(opaque_image):
    assert has_transparency(opaque_image) == False

def test_indexed_transparent_image():
    # Create an indexed image with transparency
    img = Image.new("P", (100, 100), 0)
    img.info["transparency"] = 0
    assert has_transparency(img) == True

def test_indexed_opaque_image():
    # Create an indexed image without transparency
    img = Image.new("P", (100, 100), 0)
    assert has_transparency(img) == False

def test_no_transparency_info():
    img = Image.new("RGB", (100, 100), (255, 0, 0))
    assert has_transparency(img) == False

def test_low_alpha_value():
    img = Image.new("RGBA", (100, 100), (255, 255, 255, 100))
    assert has_transparency(img) == True

def test_high_alpha_value():
    img = Image.new("RGBA", (100, 100), (255, 255, 255, 255))
    assert has_transparency(img) == False

#-------------------------------------------------------------------------
def test_get_execution_folder_not_frozen_no_argv():
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    # Save the original sys.argv and replace it with a mock
    original_argv = sys.argv
    sys.argv = ['script.py']

    try:
        # Call the function in the temporary environment
        folder = get_execution_folder()

        # Perform assertions on the result
        assert isinstance(folder, str)

    finally:
        # Clean up: restore the original sys.argv and remove the temporary directory
        sys.argv = original_argv
        shutil.rmtree(temp_dir)