from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from general_utils.models import TimeStampedModel


TIERS = (
    ('Basic', 'Basic'),
    ('Premium', 'Premium'),
    ('Enterprise', 'Enterprise'),
)


class ImageSize(models.Model):
    height = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    width = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['height', 'width'], name='unique_height_width'),
        ]

    def clean(self):
        """
        At least one value must be defined. There must be no undefined record in the database
        """
        if not self.height and not self.width:
            raise ValidationError("At least one value must be defined.")

    def __str__(self):
        def check_value(value: models.IntegerField) -> str:
            """
            The function returns _ for an argument that is not given
            """
            return str(value) if value else '_'

        return f"{check_value(self.height)} px x {check_value(self.width)} px"


class CustomSubscription(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_size = models.ManyToManyField(ImageSize)
    name = models.CharField(max_length=100, unique=True)
    original_file = models.BooleanField(default=False)
    expiring_links = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    custom_subscription = models.ForeignKey(CustomSubscription, on_delete=models.SET_NULL, null=True, blank=True)
    standard_subscription = models.CharField(choices=TIERS, max_length=100, null=True, blank=True)

    def clean(self):
        """
        The function validates whether the user does not already have a subscription.
        If you want to change your subscription, you must first remove the previous one
        """
        if self.custom_subscription and self.standard_subscription:
            raise ValidationError("Only one subscription type can be selected.")
