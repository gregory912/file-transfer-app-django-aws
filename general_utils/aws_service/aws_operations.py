from abc import ABC, abstractmethod

import boto3

from general_utils.path_operations import PathDetails
from config.settings import AWS_STORAGE_BUCKET_NAME


class SaveOperationsAWS(ABC):
    """
    The class manages operations with the AWS service
    """

    @abstractmethod
    def save_file(self, path: PathDetails) -> None:
        """
        General function for saving files in AWS
        """
        pass


def create_presigned_url(file_aws_path: str, expiration: int) -> str:
    """
    The function creates expiring links based on the file path and expiration time information
    """
    s3_client = boto3.client('s3', region_name="eu-west-2", config=boto3.session.Config(signature_version='s3v4'))
    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': AWS_STORAGE_BUCKET_NAME,
                    'Key': file_aws_path,
                    'ResponseContentDisposition': f'attachment; filename="{file_aws_path}"'},
            ExpiresIn=expiration)
    except Exception as e:
        print(e)
        return "Error"
    return response
