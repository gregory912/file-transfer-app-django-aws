from django.contrib.auth.models import User
from django.db import transaction

from images.aws_image_resizing_service.upload_images import ManageResizingUploadingImages, \
    PathsResizingUploadingImages
from images.aws_image_resizing_service.image_sizes import ImageSizesBasedOnSubscription
from images.aws_image_resizing_service.image_resizing_operations import ResizeImageKeepRatio
from images.aws_image_resizing_service.aws_operations import OperationsAWSUploadResizedImages
from images.aws_image_resizing_service.creating_paths_operations import CreateNewPathsForImages
from images.models import Image


@transaction.atomic
def save_resized_images_to_aws(image_url: str, user: User, image_instance: Image) -> bool:
    """
    A function that triggers the full action of resizing
    images according to the user's subscription and sending them to the AWS server
    """
    image_sizes_instance = ImageSizesBasedOnSubscription()

    rough_paths = CreateNewPathsForImages(
            base_path=image_url[1:],
            user=user.id,
            sizes=image_sizes_instance.get_image_sizes({"user": user})
        ).get_paths_for_images('original')

    paths_preparations_instance = PathsResizingUploadingImages(
        image_url[1:], user, image_instance, rough_paths, image_sizes_instance)

    resizing_instance = ResizeImageKeepRatio()
    aws_upload_instance = OperationsAWSUploadResizedImages()

    instance = ManageResizingUploadingImages(
        paths_preparations_instance, resizing_instance, aws_upload_instance)
    instance.creating_resize_images()
    instance.save_data_to_aws()
    instance.remove_folder()
    instance.save_data_to_db()

    return True
