from subscriptions.models import Subscription, CustomSubscription
from subscriptions.constants.base_subscriptions import *


class ImageSizesBasedOnSubscription:
    """
    The class manages the extraction and return of all
    image sizes for a given standard or custom subscription
    """
    # def __init__(self, data: dict[str, any]):
    #     self.data = data

    def get_image_sizes(self, data: dict[str, any]) -> list[tuple]:
        """
        The function returns a list of image-sized tuples for a given user subscription
        """
        instance = Subscription.objects.get(user=data['user'])

        if instance.standard_subscription:
            return self._get_sizes_for_standard_subscription(instance)
        else:
            return self._get_sizes_for_custom_subscription(instance)

    def _get_sizes_for_standard_subscription(self, instance: Subscription) -> list[tuple]:
        """
        The function checks the user's standard subscriptions
        """
        match instance.standard_subscription:
            case Basic.__name__:
                return self._get_enum_sizes(Basic)
            case Premium.__name__:
                return self._get_enum_sizes(Premium)
            case Enterprise.__name__:
                return self._get_enum_sizes(Enterprise)

    def _get_sizes_for_custom_subscription(self, instance: Subscription) -> list[tuple]:
        """
        The function returns sizes for a custom subscription
        """
        instance = CustomSubscription.objects.get(id=instance.custom_subscription.id)
        return self._get_query_set_sizes(instance)

    @staticmethod
    def _get_enum_sizes(instance: Enum) -> list[tuple]:
        """
        The function extracts data from Enum and returns in the form of a list of tuples
        """
        return [(size.HEIGHT.value, size.WIDTH.value) for size in instance.SIZE.value]

    @staticmethod
    def _get_query_set_sizes(instance: CustomSubscription) -> list[tuple]:
        """
        The function extracts data from database and returns in the form of a list of tuples
        """
        return [(size.height, size.width) for size in instance.image_size.all()]
