from django.urls import path
from . import views

urlpatterns = [
    path('', views.UploadImage.as_view(), name='upload_image'),
]