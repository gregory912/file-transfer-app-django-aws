import pytest

from images.aws_image_resizing_service.creating_paths_operations import CreateNewPathsForImages


def test_creating_paths_for_both_values(mocker):
    """
    Testing whether the function returns the correct paths for given sizes
    """
    instance = CreateNewPathsForImages('/home/user/Documents/original/file.png', 1, [(100, 200)])
    patcher = mocker.patch("images.aws_image_resizing_service.creating_paths_operations.uuid.uuid4",
                           return_value="b092c8ff-b876-4a11")

    assert instance.get_paths_for_images('original')[0] == '/home/user/Documents/100px_x_200px/b092c8ff-b876-4a11_1.png'
    patcher.stop()


def test_creating_paths_for_height_value(mocker):
    """
    Testing whether the function returns the correct paths for only height size
    """
    instance = CreateNewPathsForImages('/home/user/Documents/original/file.png', 1, [(100, 0)])
    patcher = mocker.patch("images.aws_image_resizing_service.creating_paths_operations.uuid.uuid4",
                           return_value="b092c8ff-b876-4a11")

    assert instance.get_paths_for_images('original')[0] == '/home/user/Documents/100px_x__px/b092c8ff-b876-4a11_1.png'
    patcher.stop()


def test_creating_paths_for_width_value(mocker):
    """
    Testing whether the function returns the correct paths for only width size
    """
    instance = CreateNewPathsForImages('/home/user/Documents/original/file.png', 1, [(0, 100)])
    patcher = mocker.patch("images.aws_image_resizing_service.creating_paths_operations.uuid.uuid4",
                           return_value="b092c8ff-b876-4a11")

    assert instance.get_paths_for_images('original')[0] == '/home/user/Documents/_px_x_100px/b092c8ff-b876-4a11_1.png'
    patcher.stop()
