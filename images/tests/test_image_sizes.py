from django.contrib.auth.models import User

from images.aws_image_resizing_service.image_sizes import ImageSizesBasedOnSubscription
from subscriptions.models import Subscription, CustomSubscription


def test_image_sizes_for_basic_subscription(create_user: User):
    """
    Testing that the get image sizes function returns the correct sizes for a standard Basic subscription
    """
    Subscription.objects.create(
        user=create_user,
        custom_subscription=None,
        standard_subscription="Basic"
    )
    sizes = ImageSizesBasedOnSubscription().get_image_sizes({'user': create_user})

    assert sizes == [(200, 0)]


def test_image_sizes_for_premium_subscription(create_user: User):
    """
    Testing that the get image sizes function returns the correct sizes for a standard Premium subscription
    """
    Subscription.objects.create(
        user=create_user,
        custom_subscription=None,
        standard_subscription="Premium"
    )
    sizes = ImageSizesBasedOnSubscription().get_image_sizes({'user': create_user})

    assert sizes == [(200, 0), (400, 0)]


def test_image_sizes_for_enterprise_subscription(create_user: User):
    """
    Testing that the get image sizes function returns the correct sizes for a standard Enterprise subscription
    """
    Subscription.objects.create(
        user=create_user,
        custom_subscription=None,
        standard_subscription="Enterprise"
    )
    sizes = ImageSizesBasedOnSubscription().get_image_sizes({'user': create_user})

    assert sizes == [(200, 0), (400, 0)]


def test_image_sizes_for_custom_subscription(create_user: User, create_custom_subscription: CustomSubscription):
    """
    Testing if the get image sizes function returns the correct sizes for a custom subscription
    """
    Subscription.objects.create(
        user=create_user,
        custom_subscription=create_custom_subscription,
        standard_subscription=None
    )
    sizes = ImageSizesBasedOnSubscription().get_image_sizes({'user': create_user})

    assert sizes == [(200, 200)]
