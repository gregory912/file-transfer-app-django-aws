from django.contrib.auth.models import User
from rest_framework.test import APIClient
from faker import Faker
import pytest

from subscriptions.models import CustomSubscription, ImageSize


@pytest.fixture
def api_client() -> APIClient:
    """
    The function returns APIClient object
    """
    return APIClient()


@pytest.fixture
def api_client_with_credentials(db, create_user: User, api_client: APIClient) -> APIClient:
    """
    The function returns an APIClient object. The user has been authenticated.
    By using yield the credentials will be cleared after each test
    """
    user = create_user
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)


@pytest.fixture
def faker() -> Faker:
    """
    The function returns Faker object
    """
    return Faker()


@pytest.fixture
def create_user(db) -> User:
    """
    The function creates a new user for the sample data
    """
    return User.objects.create_user(
        username="test-user",
        password="test",
        is_staff=True,
        is_superuser=True,
    )


@pytest.fixture
def create_image_size(db) -> ImageSize:
    """
    The function creates a new ImageSize for the sample data
    """
    return ImageSize.objects.create(
        height=200,
        width=200
    )


@pytest.fixture
def create_custom_subscription(db, create_user: User, create_image_size: ImageSize) -> CustomSubscription:
    """
    The function creates a new custom subscription for the sample data
    """
    instance = CustomSubscription.objects.create(
        user=create_user,
        name="Custom Subscription"
    )
    instance.image_size.add(create_image_size)
    return instance


@pytest.fixture
def custom_subscription_data(db) -> dict[str, str | list]:
    """
    The function returns sample data for custom subscription
    """
    return {
        "image_size": [
            {
                "height": 100,
                "width": 150
            },
            {
                "height": 0,
                "width": 10
            }
        ],
        "name": "Custom subscription",
        "original_file": True,
        "expiring_links": True
    }
