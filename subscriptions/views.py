from rest_framework import generics
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets

from .models import Subscription, CustomSubscription
from .serializers import SubscriptionSerializer, CustomSubscriptionSerializer


class CreateSubscription(generics.CreateAPIView):
    """
    The class manages the creation of subscriptions
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def perform_create(self, serializer):
        """
        The function sends the logged-in user to the serializer
        """
        serializer.save(user=self.request.user)


class ManageCustomSubscription(CreateModelMixin,
                               ListModelMixin,
                               RetrieveModelMixin,
                               viewsets.GenericViewSet):
    """
    The class manages the creation and retrieving of
    custom subscription data by the admin
    """
    permission_classes = [IsAdminUser]

    queryset = CustomSubscription.objects.all()
    serializer_class = CustomSubscriptionSerializer

    def perform_create(self, serializer):
        """
        The function sends the logged-in user to the serializer
        """
        serializer.save(user=self.request.user)
