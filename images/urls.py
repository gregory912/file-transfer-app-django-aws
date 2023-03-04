from django.urls import path
from . import views

urlpatterns = [
    path('', views.UploadImage.as_view(), name='upload_image'),
    path('links/<int:pk>/', views.ImageLinks.as_view(), name='image_links'),
]