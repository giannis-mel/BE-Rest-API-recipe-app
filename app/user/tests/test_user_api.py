"""
Tests for the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

# Not used for now
# import logging

# Define the URL for creating a new user
CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    """Helper function to create a new user with given parameters"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """
        Test class for the public features of the user API
        (public are the ones that don't require authentication)
    """
    # Set up the test client before each test
    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        # Define the data payload for creating a user
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        # Make a POST request to the user creation URL with the payload
        res = self.client.post(CREATE_USER_URL, payload)

        # Assert that the response status code is 201 (created)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Retrieve the created user from the database
        user = get_user_model().objects.get(email=payload['email'])
        # Added logging for later testing
        # logging.info(f"User created - Email:{user.email}, Name:{user.name}")

        # Assert that the user's password matches the provided password
        self.assertTrue(user.check_password(payload['password']))

        # Assert that the response data does not contain the password keyword
        self.assertNotIn('password', res.data)

        # Assert that the response data does not contain the password's value
        self.assertNotIn('testpass123', res.data)

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists."""
        # Create a user with the specified email
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        # get_user_model().objects.create(**payload)
        create_user(**payload)
        # Make a POST request to the user creation URL with the same payload
        # as the previous test
        res = self.client.post(CREATE_USER_URL, payload)

        # Assert that the response status code is 400 (bad request)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 chars."""
        # Define the data payload with a short password
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test name',
        }
        # Make a POST request to the user creation URL with the payload
        res = self.client.post(CREATE_USER_URL, payload)

        # Assert that the response status code is 400 (bad request)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that a user with the specified email does not exist
        # in the database
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)
