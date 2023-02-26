from django.contrib import admin
from .models import Subscription, CustomSubscription, ImageSize

admin.site.register(Subscription)
admin.site.register(CustomSubscription)
admin.site.register(ImageSize)
