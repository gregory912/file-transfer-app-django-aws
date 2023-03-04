from django.urls import path
from . import views

urlpatterns = [
    path('', views.UploadImage.as_view(), name='upload_image'),
    path('links/<int:pk>/', views.ImageLinks.as_view(), name='image_links'),
    path('expiration_link/update/<int:pk>/', views.UpdateExpirationTime.as_view(), name='update_expiration_link'),
    path('expiration_link/<int:pk>/', views.TimedLink.as_view(), name='timed_link'),
]