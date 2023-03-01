from abc import ABC, abstractmethod

from general_utils.path_operations import PathDetails


class OperationsAWS(ABC):
    """
    The class manages operations with the AWS service
    """

    @abstractmethod
    def save_file(self, path: PathDetails) -> None:
        """
        General function for saving files in AWS
        """
        pass
