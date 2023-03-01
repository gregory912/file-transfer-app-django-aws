import os
from abc import ABC, abstractmethod


class ResizeImage(ABC):
    """
    The base class for performing operations on images
    """

    @abstractmethod
    def resize_image(self, base_path, size: tuple[int, int], new_path: str) -> None:
        """
        A function that resizes and saves the image with new dimensions
        """
        pass

    @abstractmethod
    def resize_images(self, base_path, sizes: list, new_paths: list[str]) -> None:
        """
        The function, based on the main image, creates several new images for the data entry
        """
        pass

    @staticmethod
    def _check_if_resized_file_exists(path: str) -> bool:
        """
        Checking if the resized file has been saved correctly
        """
        if os.path.isfile(path):
            return True
        raise FileNotFoundError(f"File hasn't been found: {path}")

    @staticmethod
    def calculate_height(original_height: int, original_width: int, width: int) -> int:
        """
        The function calculates the length for the height by proportions
        """
        aspect_ratio = original_width / original_height
        height = round(width / aspect_ratio)
        return height

    @staticmethod
    def calculate_width(original_height: int, original_width: int, height: int) -> int:
        """
        The function calculates the length for the width by proportions
        """
        aspect_ratio = original_width / original_height
        width = round(height * aspect_ratio)
        return width
