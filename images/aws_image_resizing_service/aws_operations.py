import mimetypes

import boto3

from config.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME
from general_utils.aws_service.aws_operations import SaveOperationsAWS
from general_utils.path_operations import PathDetails


class OperationsAWSUploadResizedImages(SaveOperationsAWS):
    """
    The class manages operations with the AWS service
    """

    def save_file(self, path: PathDetails) -> None:
        """
        Saving the file to the AWS server. The file will be placed in the appropriate folder
        """
        with open(path.full_path, 'rb') as file:
            s3 = boto3.client(
                's3',
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY
            )
            content_type, _ = self.get_file_extension(path)

            s3.upload_fileobj(
                file,
                AWS_STORAGE_BUCKET_NAME,
                path.get_last_folder_with_filename(), ExtraArgs={'ContentType': content_type}
            )

    @staticmethod
    def get_file_extension(path: PathDetails) -> tuple[str, str]:
        """
        The function returns the extension of the given file
        """
        return mimetypes.guess_type(path.get_file_name())
