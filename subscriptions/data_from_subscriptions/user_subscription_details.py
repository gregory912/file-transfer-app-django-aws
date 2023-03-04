from subscriptions.models import Subscription, CustomSubscription
from subscriptions.constants.base_subscriptions import *


class DataBasedOnSubscription:
    """
    The class, based on the subscription, manages the return of information about
    the appropriate opportunities for a given user
    """
    def __init__(self, data: dict[str, any]):
        self.data = data

        self.instance = Subscription.objects.get(user=data['user'])

    def get_image_sizes(self) -> list[tuple]:
        """
        The function returns a list of image-sized tuples for a given user subscription
        """

        if self.instance.standard_subscription:
            return self._get_sizes_for_standard_subscription(self.instance)
        else:
            return self._get_sizes_for_custom_subscription(self.instance)

    def get_is_original_field(self) -> bool:
        """
        The function returns information whether the user should receive a link to the original file
        """
        if self.instance.standard_subscription:
            match self.instance.standard_subscription:
                case Basic.__name__:
                    return Basic.ORIGINAL_FILE.value
                case Premium.__name__:
                    return Premium.ORIGINAL_FILE.value
                case Enterprise.__name__:
                    return Enterprise.ORIGINAL_FILE.value
        else:
            return CustomSubscription.objects.get(id=self.instance.custom_subscription.id).original_file

    def get_expiring_links_field(self) -> bool:
        """
        The function returns information whether the user has the ability
        to generate expiring links to images
        """
        if self.instance.standard_subscription:
            match self.instance.standard_subscription:
                case Basic.__name__:
                    return Basic.EXPIRING_LINKS.value
                case Premium.__name__:
                    return Premium.EXPIRING_LINKS.value
                case Enterprise.__name__:
                    return Enterprise.EXPIRING_LINKS.value
        else:
            return CustomSubscription.objects.get(id=self.instance.custom_subscription.id).expiring_links

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
