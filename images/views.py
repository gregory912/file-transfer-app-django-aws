from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework import generics
from django.db.models import Q, QuerySet
from django.shortcuts import get_object_or_404

from .models import Image, Link, ImageSize
from .serializers import ImageSerializer, LinkSerializer
from subscriptions.data_from_subscriptions.user_subscription_details import DataBasedOnSubscription
from general_utils.permissions import IsOwner, IsOwnerLink
from general_utils.aws_service.aws_operations import create_presigned_url
from general_utils.path_operations import PathDetails


class UploadImage(generics.ListCreateAPIView):
    """
    The class manages the transfer of images to the application
    """
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def perform_create(self, serializer):
        """
        The function sends the logged-in user to the serializer
        """
        serializer.save(user=self.request.user)


class ImageLinks(APIView):
    """
    The class, based on the user's subscription, manages the return of all links to a given image
    """
    permission_classes = [IsOwner]

    def get(self, request: Request, pk: int) -> Response:
        """
        If the image exists and the user has access to it, all links to
        the image will be returned based on the subscription
        """
        image_instance = self.get_object(pk)

        user_subs_instance = DataBasedOnSubscription({"user": self.request.user})

        user_subs_data = user_subs_instance.get_image_sizes()

        image_sizes = ImageSize.objects.filter(
            Q(height__in=[s[0] for s in user_subs_data]) & Q(width__in=[s[1] for s in user_subs_data]))

        if user_subs_instance.get_is_original_field():
            combined_filter = Q(size__in=image_sizes) | Q(is_original=True)
            links = Link.objects.filter(image_id=image_instance).filter(combined_filter)
        else:
            links = Link.objects.filter(image_id=image_instance, size__in=image_sizes)

        return Response(self.get_serialized_data(links), status=status.HTTP_200_OK)

    def get_object(self, pk: int) -> Image:
        """
        The function returns an Image object or a 404 error.
        The function checks whether the user has access to the resource
        """
        obj = get_object_or_404(Image, id=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    @staticmethod
    def get_serialized_data(links: list[QuerySet]) -> list[LinkSerializer]:
        """
        The function returns a list with data to be sent by the user
        """
        return [LinkSerializer(image).data for image in links]


class UpdateExpirationTime(generics.UpdateAPIView):
    """
    The class manages updating the link_expiration_time field for a given link
    """
    permission_classes = [IsOwnerLink]
    queryset = Link.objects.all()
    serializer_class = LinkSerializer


class TimedLink(APIView):
    """
    The class manages to return an expiring link to a file
    """
    permission_classes = [IsOwnerLink]

    def get(self, request: Request, pk: int) -> Response:
        """
        The function returns an expiring link to a file if the user has permission to access it
        """
        link_instance = self.get_object(pk)

        user_subs_instance = DataBasedOnSubscription({"user": self.request.user})

        if user_subs_instance.get_expiring_links_field():
            url = PathDetails(link_instance.url.url).get_last_folder_with_filename()
            link = create_presigned_url(url, link_instance.link_expiration_time)

            return Response({"expiration_link": link}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Subscription does not allow expiring links"}, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, pk: int) -> Link:
        """
        The function returns Link object or a 404 error.
        The function checks whether the user has access to the resource
        """
        obj = get_object_or_404(Link, id=pk)
        self.check_object_permissions(self.request, obj)
        return obj
