import os

from PIL import Image

from general_utils.image_service.resizing_operations import ResizeImage


class ResizeImageKeepRatio(ResizeImage):
    """
    A class that manages the resizing of an image or several images. The image ratio should be maintained
    """

    def resize_image(self, base_path: str, size: tuple[int, int], new_path: str) -> None:
        """
        The function creates a new image based on the base image and saves it to the previously created folder
        """
        with Image.open(base_path) as im:
            self._create_folder_before_saving_file(new_path)

            size = self._get_image_ratio(size, im.height, im.width)

            new_image = im.resize(size[::-1])
            new_image.save(new_path)

            self._check_if_resized_file_exists(new_path)

    def resize_images(self, base_path: str, sizes: list[tuple[int, int]], new_paths: list[str]) -> None:
        """
        The function based on the base image creates new images based on
        the entered data and saves them to previously created folders
        """
        with Image.open(base_path) as im:
            for size, path in zip(sizes, new_paths):
                self._create_folder_before_saving_file(path)

                size = self._get_image_ratio(size, im.height, im.width)

                new_image = im.resize(size[::-1])
                new_image.save(path)

                self._check_if_resized_file_exists(path)

    def _get_image_ratio(self, size: tuple[int | None, int | None], height: int, width: int) -> tuple[int, int]:
        """
        The function checks whether both sides are given for the new image,
        if not, the side is determined based on the proportions
        """
        if size[0] == 0:
            return self.calculate_height(height, width, size[1]), size[1]
        elif size[1] == 0:
            return size[0], self.calculate_width(height, width, size[0])
        return size

    @staticmethod
    def _create_folder_before_saving_file(path: str) -> None:
        """
        The function creates a folder based on the given path
        """
        os.makedirs(os.path.dirname(path))
