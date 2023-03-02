import os
import shutil

import pytest
from PIL import Image

from images.aws_image_resizing_service.image_resizing_operations import ResizeImageKeepRatio


@pytest.mark.parametrize(
    "original_height,original_width,height,result",
    [
        (100, 100, 50, 50),
        (200, 100, 100, 200),
        (300, 100, 70, 210),
        (150, 120, 70, 88)
    ]
)
def test_function_calculate_height(original_height: int, original_width: int, height: int, result: int):
    """
    The function calculates the aspect ratio based on the entered image and height data
    """
    assert ResizeImageKeepRatio().calculate_height(original_height, original_width, height) == result


@pytest.mark.parametrize(
    "original_height,original_width,width,result",
    [
        (100, 100, 50, 50),
        (200, 100, 100, 50),
        (300, 100, 70, 23),
        (150, 120, 70, 56)
    ]
)
def test_function_calculate_width(original_height: int, original_width: int, width: int, result: int):
    """
    The function calculates the aspect ratio based on the entered image and width data
    """
    assert ResizeImageKeepRatio().calculate_width(original_height, original_width, width) == result


def test_resizing_image_for_values_100_100():
    """
    Testing if the resized image is 100x100
    """
    new_path = r'images/tests/static_100_100/cutlery.png'

    ResizeImageKeepRatio().resize_image(r'images/tests/static/cutlery.png', (100, 100), new_path)

    with Image.open(new_path) as img:
        width, height = img.size
        assert (height, width) == (100, 100)
    shutil.rmtree(os.path.dirname(new_path))


def test_resizing_image_for_values_123_193():
    """
    Testing if the resized image is 123x193
    """
    new_path = r'images/tests/static_123_193/cutlery.png'

    ResizeImageKeepRatio().resize_image(r'images/tests/static/cutlery.png', (123, 193), new_path)

    with Image.open(new_path) as img:
        width, height = img.size
        assert (height, width) == (123, 193)
    shutil.rmtree(os.path.dirname(new_path))
