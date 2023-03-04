import shutil

from subscriptions.data_from_subscriptions.user_subscription_details import DataBasedOnSubscription
from .image_resizing_operations import ResizeImage
from .aws_operations import OperationsAWS
from ..models import Link
from subscriptions.models import ImageSize
from general_utils.path_operations import PathDetails


class PathsResizingUploadingImages:
    """
    A class that manages the preparation of all required image paths
    """
    def __init__(self, file_path: str, rough_paths: list[str]):

        self.file_path = file_path
        self.rough_paths = rough_paths

        self.paths_obj = [PathDetails(full_path=path) for path in self.rough_paths]
        self.paths_obj_with_original = self.paths_obj + [PathDetails(self.file_path)]


class ManageResizingUploadingImages:
    """
    A class that manages operations to create images based on subscription sizes,
    upload to AWS, and save to the database
    """
    def __init__(self, paths: PathsResizingUploadingImages, resize_img: ResizeImage, aws_obj: OperationsAWS,
                 logged_in_user: int, image: int, image_sizes_obj: DataBasedOnSubscription):
        self.paths = paths
        self.resize_img_obj = resize_img
        self.aws_obj = aws_obj
        self.logged_in_user = logged_in_user
        self.image = image
        self.image_sizes_obj = image_sizes_obj

    def creating_resize_images(self) -> None:
        """
        Calling a function to resize images according to the user's subscription
        """
        self.resize_img_obj.resize_images(
            self.paths.file_path,
            self.image_sizes_obj.get_image_sizes(),
            self.paths.rough_paths
        )

    def save_data_to_aws(self) -> None:
        """
        Sending the paths to the aws object which will send the images to the server
        """
        [self.aws_obj.save_file(path) for path in self.paths.paths_obj_with_original]

    def remove_folder(self) -> None:
        """
        Deleting the folder together with subfolders and files after uploading the files to the AWS server
        """
        shutil.rmtree(self.paths.paths_obj_with_original[0].get_path_without_last_folder_and_filename())

    def save_data_to_db(self) -> None:
        """
        Saving paths to aws for newly created images to the database
        """
        link_instances = []
        for path, size in zip(self.paths.paths_obj, self.image_sizes_obj.get_image_sizes()):
            image_size_instance, _ = ImageSize.objects.get_or_create(height=size[0], width=size[1])

            link_instances.append(
                Link(image=self.image, size=image_size_instance, url=path.get_last_folder_with_filename()))

        Link.objects.bulk_create(link_instances)

    def update_path_original_file(self) -> None:
        """
        Update url for original file to same as on aws
        """
        instance = Link.objects.get(image=self.image, is_original=True)
        new_path = PathDetails(instance.url.url).get_last_folder_with_filename()
        instance.url = new_path
        instance.save()
