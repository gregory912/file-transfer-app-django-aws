import mimetypes

import boto3

from config.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME
from general_utils.aws_service.aws_operations import OperationsAWS


class OperationsAWSUploadResizedImages(OperationsAWS):
    """
    The class manages operations with the AWS service
    """

    def save_file(self, path) -> None:
        """
        Saving the file to the AWS server. The file will be placed in the appropriate folder
        """
        with open(path.full_path, 'rb') as file:
            s3 = boto3.client(
                's3',
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY
            )
            content_type, _ = mimetypes.guess_type(path.get_file_name())

            s3.upload_fileobj(
                file,
                AWS_STORAGE_BUCKET_NAME,
                path.get_last_folder_with_filename(), ExtraArgs={'ContentType': content_type}
            )
