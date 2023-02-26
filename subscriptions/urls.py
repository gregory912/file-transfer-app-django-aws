from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'', views.ManageCustomSubscription, basename='manage_custom_subscription')

urlpatterns = [
    path('', views.CreateSubscription.as_view(), name='create_subscription'),
    path('custom/', include(router.urls)),
]