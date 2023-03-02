import boto3

from images.aws_image_resizing_service.aws_operations import OperationsAWSUploadResizedImages
from general_utils.path_operations import PathDetails
from config.settings import AWS_STORAGE_BUCKET_NAME


def test_uploading_files_to_aws(mocker):
    """
    Testing if a file will be uploaded to AWS
    """
    test_filename = r"test/cutlery.png"

    patcher = mocker.patch(
        "images.aws_image_resizing_service.aws_operations.PathDetails.get_last_folder_with_filename",
        return_value="test/cutlery.png")

    path = PathDetails(r'images/tests/static/cutlery.png')
    OperationsAWSUploadResizedImages().save_file(path)

    s3 = boto3.client('s3')
    try:
        s3.head_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=test_filename)
        assert True
    except:
        assert False


def test_getting_file_extension():
    """
    Testing if the get_file_extension function returns correct data
    """
    path = PathDetails(r'images/tests/static/cutlery.png')
    instance, _ = OperationsAWSUploadResizedImages().get_file_extension(path)

    assert instance == 'image/png'
