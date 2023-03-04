from django.db import transaction
from celery import shared_task

from images.aws_image_resizing_service.upload_images import ManageResizingUploadingImages, \
    PathsResizingUploadingImages
from subscriptions.data_from_subscriptions.user_subscription_details import DataBasedOnSubscription
from images.aws_image_resizing_service.image_resizing_operations import ResizeImageKeepRatio
from images.aws_image_resizing_service.aws_operations import OperationsAWSUploadResizedImages
from images.aws_image_resizing_service.creating_paths_operations import CreateNewPathsForImages
from images.models import Image


@shared_task
@transaction.atomic
def save_resized_images_to_aws(image_url: str, user: int, image_instance: int) -> bool:
    """
    A function that triggers the full action of resizing
    images according to the user's subscription and sending them to the AWS server
    """
    image_instance = Image.objects.get(id=image_instance)

    image_sizes_instance = DataBasedOnSubscription({"user": user})

    rough_paths = CreateNewPathsForImages(
            base_path=image_url[1:],
            user=user,
            sizes=image_sizes_instance.get_image_sizes()
        ).get_paths_for_images('original')

    paths_preparations_instance = PathsResizingUploadingImages(image_url[1:], rough_paths)

    resizing_instance = ResizeImageKeepRatio()
    aws_upload_instance = OperationsAWSUploadResizedImages()

    instance = ManageResizingUploadingImages(
        paths_preparations_instance, resizing_instance, aws_upload_instance, user, image_instance, image_sizes_instance)
    instance.creating_resize_images()
    instance.save_data_to_aws()
    instance.remove_folder()
    instance.save_data_to_db()
    instance.update_path_original_file()

    return True
