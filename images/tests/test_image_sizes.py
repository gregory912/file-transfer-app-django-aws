from django.contrib.auth.models import User

from subscriptions.data_from_subscriptions.user_subscription_details import DataBasedOnSubscription
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
    sizes = DataBasedOnSubscription({'user': create_user}).get_image_sizes()

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
    sizes = DataBasedOnSubscription({'user': create_user}).get_image_sizes()

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
    sizes = DataBasedOnSubscription({'user': create_user}).get_image_sizes()

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
    sizes = DataBasedOnSubscription({'user': create_user}).get_image_sizes()

    assert sizes == [(200, 200)]
