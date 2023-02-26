from rest_framework import serializers
from django.db import transaction

from .models import Subscription, CustomSubscription, ImageSize
from subscriptions.constants.base_subscriptions import *


class SubscriptionSerializer(serializers.ModelSerializer):

    standard_subscription = serializers.CharField(required=True, allow_blank=True)
    custom_subscription = serializers.CharField(required=True, allow_blank=True)

    class Meta:
        model = Subscription
        fields = [
            'standard_subscription',
            'custom_subscription'
        ]

    @transaction.atomic
    def create(self, validated_data: dict[str, str]) -> Subscription:
        """
        Depending on the user data submitted, a standard or custom subscription will be created
        """
        if validated_data.get('standard_subscription', None):
            instance = Subscription.objects.create(
                user=validated_data['user'],
                standard_subscription=validated_data['standard_subscription']
            )
            return instance

        else:
            subscription_instance = CustomSubscription.objects.get(name=validated_data.get('custom_subscription'))

            instance = Subscription.objects.create(
                user=validated_data['user'],
                custom_subscription=subscription_instance
            )
            return instance

    def validate(self, data: dict[str, str]) -> dict[str, str]:
        """
        Validation that allows you to check the following elements:
        - if both subscriptions have been sent
        - if any subscription haven't been sent
        - if user already has a subscription
        """
        if data.get('standard_subscription', None) and data.get('custom_subscription', None):
            raise serializers.ValidationError("Only one field can be provided.")

        if not data.get('standard_subscription', None) and not data.get('custom_subscription', None):
            raise serializers.ValidationError("At least one field must be defined.")

        user = self.context['request'].user
        if Subscription.objects.filter(user=user).exists():
            raise serializers.ValidationError("User already has a subscription")

        return data

    @staticmethod
    def validate_standard_subscription(value: str) -> str:
        """
        Checking if the sent subscription is correct
        """
        if value and value not in (Basic.__name__, Premium.__name__, Enterprise.__name__,):
            raise serializers.ValidationError("The given subscription does not exist.")
        return value

    @staticmethod
    def validate_custom_subscription(value: str) -> str:
        """
        Checking if the custom subscription sent by the user exists in the database
        """
        if value and not CustomSubscription.objects.filter(name=value).exists():
            raise serializers.ValidationError("The given subscription does not exist.")
        return value


class ImageSizeSerializer(serializers.ModelSerializer):

    height = serializers.IntegerField(required=True)
    width = serializers.IntegerField(required=True)

    class Meta:
        model = Subscription
        fields = [
            'id',
            'height',
            'width',
        ]

    def validate(self, data: dict[str, str]) -> dict[str, str]:
        """
        Checking if at least one field has been defined.
        """
        if not data.get('height', None) and not data.get('width', None):
            raise serializers.ValidationError("At least one field must be defined.")
        return data

    @staticmethod
    def validate_height(value: int) -> int:
        """
        Checking if the entered value is in the correct range
        """
        if value > 1500 or value < 0:
            raise serializers.ValidationError("The value for height must be in the range 0 - 1500")
        return value

    @staticmethod
    def validate_width(value: int) -> int:
        """
        Checking if the entered value is in the correct range
        """
        if value > 1500 or value < 0:
            raise serializers.ValidationError("The value for width must be in the range 0 - 1500")
        return value


class CustomSubscriptionSerializer(serializers.ModelSerializer):

    image_size = ImageSizeSerializer(many=True, required=True)

    class Meta:
        model = CustomSubscription
        fields = [
            'name',
            'original_file',
            'expiring_links',
            'is_active',
            'image_size'
        ]

    @transaction.atomic
    def create(self, validated_data: dict[str, str | list]) -> CustomSubscription:
        """
        Create an instance with the required fields from the many-to-many relationship
        """
        image_size = validated_data.pop('image_size')

        instance = CustomSubscription.objects.create(**validated_data)
        instance.image_size.add(*self._create_obj_name_field(image_size, ImageSize))

        return instance

    @staticmethod
    def _create_obj_name_field(items: list[dict[str, int]], obj: ImageSize) -> tuple:
        """
        Create tuples of objects that can be assigned to any field in a many-to-many relationship
        """
        instances = []
        for item in items:
            instance, _ = obj.objects.get_or_create(height=item['height'], width=item['width'])
            instance.save()
            instances.append(instance)
        return tuple(instances)
