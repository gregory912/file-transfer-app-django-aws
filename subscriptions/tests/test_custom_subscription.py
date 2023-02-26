import json

from django.urls import reverse
from rest_framework.test import APIClient
import pytest

from subscriptions.models import ImageSize, CustomSubscription


@pytest.mark.django_db
def test_creating_custom_subscription_with_correct_fields(
        api_client_with_credentials: APIClient,
        custom_subscription_data: dict[str, str | list]):
    """
    Testing the creation of custom subscriptions for valid input
    """
    url = reverse('manage_custom_subscription-list')

    response = api_client_with_credentials.post(url, data=json.dumps(custom_subscription_data), content_type='application/json')

    assert response.status_code == 201
    assert CustomSubscription.objects.all().count() == 1
    assert ImageSize.objects.all().count() == 2


@pytest.mark.django_db
def test_creating_custom_subscription_with_image_size_higher_than_1500(
        api_client_with_credentials: APIClient,
        custom_subscription_data: dict[str, str | list]):
    """
    Testing the creation of custom subscriptions for an image height greater than 1500
    """
    url = reverse('manage_custom_subscription-list')

    custom_subscription_data['image_size'][0]['height'] = 1600

    response = api_client_with_credentials.post(url, data=json.dumps(custom_subscription_data), content_type='application/json')

    assert response.status_code == 400


@pytest.mark.django_db
def test_creating_custom_subscription_with_image_size_heights_less_than_0(
        api_client_with_credentials: APIClient,
        custom_subscription_data: dict[str, str | list]):
    """
    Testing the creation of custom subscriptions for an image heights less than 0
    """
    url = reverse('manage_custom_subscription-list')

    custom_subscription_data['image_size'][0]['height'] = -1

    response = api_client_with_credentials.post(url, data=json.dumps(custom_subscription_data), content_type='application/json')

    assert response.status_code == 400


@pytest.mark.django_db
def test_creating_custom_subscription_without_name_field(
        api_client_with_credentials: APIClient,
        custom_subscription_data: dict[str, str | list]):
    """
    Testing the creation of custom subscriptions without field name
    """
    url = reverse('manage_custom_subscription-list')

    del custom_subscription_data['name']

    response = api_client_with_credentials.post(url, data=json.dumps(custom_subscription_data), content_type='application/json')

    assert response.status_code == 400
