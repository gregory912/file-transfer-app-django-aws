from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.validators import FileExtensionValidator

from general_utils.models import TimeStampedModel
from subscriptions.models import ImageSize


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('user', 'name')


class Link(TimeStampedModel):
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='links')
    size = models.ForeignKey(ImageSize, blank=True, null=True, on_delete=models.SET_NULL)
    url = models.ImageField(
        upload_to='%d_%H_%M_%S_%f/original',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )
    is_original = models.BooleanField(default=False)
    link_expiration_time = models.IntegerField(validators=[MinValueValidator(0)], default=0)

    def __str__(self):
        return f"{self.image.name} - {self.size}"
