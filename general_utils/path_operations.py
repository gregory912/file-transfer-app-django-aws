import os
from dataclasses import dataclass
from abc import ABC


@dataclass
class PathDetails(ABC):
    """
    A class that returns the appropriate elements from the entered path
    """

    full_path: str

    def get_file_name(self) -> str:
        """
        The function return file name from a path
        '/home/user/Documents/project/file.txt' ---> file.txt
        """
        return os.path.basename(self.full_path)

    def get_last_folder(self) -> str:
        """
        The function return file name from a path
        '/home/user/Documents/project/file.txt' ---> project
        """
        return os.path.basename(os.path.dirname(self.full_path))

    def get_path_without_filename(self) -> str:
        """
        The function return full path without filename
        '/home/user/Documents/project/file.txt' ---> /home/user/Documents/projekt
        """
        return os.path.dirname(self.full_path)

    def get_path_without_last_folder_and_filename(self) -> str:
        """
        The function remove filename and the last folder
        '/home/user/Documents/project/file.txt' ---> /home/user/Documents
        """
        return os.path.dirname(os.path.dirname(self.full_path))

    def get_last_folder_with_filename(self) -> str:
        """
        The function returns the folder where the file is located
        '/home/user/Documents/project/file.txt' ---> project/file.txt
        """
        return f"{self.get_last_folder()}/{self.get_file_name()}"