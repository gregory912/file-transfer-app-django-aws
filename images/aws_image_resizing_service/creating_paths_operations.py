import os
from dataclasses import dataclass
import uuid


@dataclass
class CreateNewPathsForImages:
    """
    The class creates new paths based on the required image sizes
    """
    base_path: str
    user: int
    sizes: list

    def get_paths_for_images(self) -> list[str]:
        """
        The function returns a list with updated paths
        """
        list_of_paths = []
        for h, w in self.sizes:
            path = self.base_path.replace('original', self._get_folder_name(h, w))
            _, extension = os.path.splitext(path)
            list_of_paths.append(f"{os.path.dirname(path)}/{uuid.uuid4()}_{self.user}{extension}")
        return list_of_paths

    def _get_folder_name(self, height: int, width: int) -> str:
        """
        The function returns the name of the folder in the appropriate format
        """
        return f'{self._check_if_positive_value(height)}px_x_{self._check_if_positive_value(width)}px'

    @staticmethod
    def _check_if_positive_value(value: int) -> str:
        """
        The function checks if a given value is greater than zero. If it is zero it will be returned _
        """
        return str(value) if value else '_'



