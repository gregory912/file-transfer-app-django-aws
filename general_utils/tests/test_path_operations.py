import pytest


from general_utils.path_operations import PathDetails


@pytest.fixture
def get_path_details() -> PathDetails:
    """
    The function returns a Path Details object for the indicated path
    """
    return PathDetails('home/user/Documents/project/file.txt')


def test_get_file_name(get_path_details: PathDetails):
    """
    Testing if the get_file_name function returns the name of the file with the extension
    """
    assert get_path_details.get_file_name() == "file.txt"


def test_get_last_folder(get_path_details: PathDetails):
    """
    Testing if the get_last_folder function returns the name of the last folder in the file
    """
    assert get_path_details.get_last_folder() == "project"


def test_get_path_without_filename(get_path_details: PathDetails):
    """
    Testing if get_path_without filename returns pathname without filename
    """
    assert get_path_details.get_path_without_filename() == "home/user/Documents/project"


def test_get_path_without_last_folder_and_filename(get_path_details: PathDetails):
    """
    Testing if get_path_without_last_folder_and filename returns path
    without filename and without last folder name
    """
    assert get_path_details.get_path_without_last_folder_and_filename() == "home/user/Documents"


def test_get_last_folder_with_filename(get_path_details: PathDetails):
    """
    Testing if function get_last_folder_with filename returns last folder name filename
    """
    assert get_path_details.get_last_folder_with_filename() == "project/file.txt"
