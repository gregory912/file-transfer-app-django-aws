import re
import uuid
import os

from rest_framework import serializers
from django.core.validators import FileExtensionValidator

from .models import Image, Link, ImageSize
from .tasks import save_resized_images_to_aws
from config.settings import AWS_STORAGE_BUCKET_NAME


class ImageSerializer(serializers.ModelSerializer):

    image = serializers.ImageField(write_only=True, required=True, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])

    class Meta:
        model = Image
        fields = [
            'id',
            'name',
            'image'
        ]

    def create(self, validated_data: dict[str, any]) -> Image:
        """
        The function saves validated data to the database.
        The method for saving data on AWS will be called based on the uploaded file
        """
        image_instance = Image.objects.create(user=validated_data['user'], name=validated_data['name'])

        request = self.context.get('request')
        image = request.FILES.get('image')

        link_instance = Link(image=image_instance, url=image, is_original=True)
        _, extension = os.path.splitext(link_instance.url.name)
        link_instance.url.name = f"{str(uuid.uuid4())}_{validated_data['user'].id}{extension}"
        link_instance.save()

        image_url = link_instance.url.url

        save_resized_images_to_aws.delay(image_url, validated_data['user'].id, image_instance.id)

        return image_instance

    def validate(self, data: dict[str, any]) -> dict[str, any]:
        """
        The function checks if the user already has an image with this title
        """
        user = self.context['request'].user
        name = data.get('name')

        if Image.objects.filter(user=user, name=name).exists():
            raise serializers.ValidationError("An image with the given title already exists")

        return data

    @staticmethod
    def validate_image(value):
        """
        The function validates whether the uploaded file does not contain prohibited elements
        """
        if re.search(r'[<>:"/\\|?*]', str(value)):
            raise serializers.ValidationError("The filename entered is not valid")
        return value


class ImageSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageSize
        fields = [
            'id',
            'height',
            'width'
        ]


class LinkSerializer(serializers.ModelSerializer):

    size = ImageSizeSerializer(required=False)
    url = serializers.SerializerMethodField()

    class Meta:
        model = Link
        fields = [
            'id',
            'size',
            'url',
            'is_original',
            'link_expiration_time',
        ]

    @staticmethod
    def get_url(obj) -> str:
        """
        The function returns the full url to a resource on aws
        """
        return f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{obj.url}'
