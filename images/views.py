from rest_framework import generics

from .models import Image
from .serializers import ImageSerializer


class UploadImage(generics.CreateAPIView):
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
