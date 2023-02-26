import json

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from subscriptions.models import CustomSubscription


@pytest.mark.django_db
def test_standard_subscription_with_correct_field(api_client_with_credentials: APIClient):
    """
    Test if the correct status code will be returned for the correct standard subscription name
    """
    url = reverse('create_subscription')

    data = {
        "standard_subscription": "Basic",
        "custom_subscription": ""
    }
    response = api_client_with_credentials.post(url, data=json.dumps(data), content_type='application/json')

    assert response.status_code == 201


@pytest.mark.django_db
def test_standard_subscription_with_incorrect_field(api_client_with_credentials: APIClient):
    """
    Test if the correct status code will be returned for the invalid standard subscription name
    """
    url = reverse('create_subscription')

    data = {
        "standard_subscription": "NotCorrectValue",
        "custom_subscription": ""
    }
    response = api_client_with_credentials.post(url, data=json.dumps(data), content_type='application/json')

    assert response.status_code == 400


@pytest.mark.django_db
def test_custom_subscription_with_correct_field(
        api_client_with_credentials: APIClient,
        create_custom_subscription: CustomSubscription):
    """
    Test if the correct status code will be returned for the correctly entered custom_subscription field
    """
    url = reverse('create_subscription')

    data = {
        "standard_subscription": "",
        "custom_subscription": create_custom_subscription.name
    }
    response = api_client_with_credentials.post(url, data=json.dumps(data), content_type='application/json')

    assert response.status_code == 201


@pytest.mark.django_db
def test_custom_subscription_with_incorrect_field(api_client_with_credentials: APIClient):
    """
    Test if the correct status code will be returned for the incorrectly entered custom_subscription field
    """
    url = reverse('create_subscription')

    data = {
        "standard_subscription": "",
        "custom_subscription": "NotCorrectValue",
    }
    response = api_client_with_credentials.post(url, data=json.dumps(data), content_type='application/json')

    assert response.status_code == 400


@pytest.mark.django_db
def test_creating_subscription_for_both_empty_fields(api_client_with_credentials: APIClient):
    """
    Test if an error is returned for both empty fields
    """
    url = reverse('create_subscription')

    data = {
        "standard_subscription": "",
        "custom_subscription": "",
    }
    response = api_client_with_credentials.post(url, data=json.dumps(data), content_type='application/json')

    assert response.status_code == 400


@pytest.mark.django_db
def test_creating_subscription_for_both_correct_fields(
        api_client_with_credentials: APIClient,
        create_custom_subscription: CustomSubscription):
    """
    Test if an error is returned for both entered fields
    """
    url = reverse('create_subscription')

    data = {
        "standard_subscription": "Basic",
        "custom_subscription": create_custom_subscription.name
    }
    response = api_client_with_credentials.post(url, data=json.dumps(data), content_type='application/json')

    assert response.status_code == 400


@pytest.mark.django_db
def test_creating_subscription_for_missing_custom_subscription_field(api_client_with_credentials: APIClient):
    """
    Test if an error is returned for missing custom_subscription field
    """
    url = reverse('create_subscription')

    data = {
        "standard_subscription": "Basic",
    }
    response = api_client_with_credentials.post(url, data=json.dumps(data), content_type='application/json')

    assert response.status_code == 400


@pytest.mark.django_db
def test_creating_subscription_for_missing_standard_subscription_field(
        api_client_with_credentials: APIClient,
        create_custom_subscription: CustomSubscription):
    """
    Test if an error is returned for missing standard_subscription field
    """
    url = reverse('create_subscription')

    data = {
        "custom_subscription": create_custom_subscription.name,
    }
    response = api_client_with_credentials.post(url, data=json.dumps(data), content_type='application/json')

    assert response.status_code == 400


@pytest.mark.django_db
def test_creating_subscription_for_missing_both_fields(
        api_client_with_credentials: APIClient,
        create_custom_subscription: CustomSubscription):
    """
    Test if an error is returned for missing both fields
    """
    url = reverse('create_subscription')

    data = {}
    response = api_client_with_credentials.post(url, data=json.dumps(data), content_type='application/json')

    assert response.status_code == 400
