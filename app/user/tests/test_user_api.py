from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
CREATE_TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users API public"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test if creating user with valid payload is successful"""
        payload = {
            'email': 'testmihai@apidev.com',
            'password': 'testpass123',
            'first_name': 'test first_name',
            'last_name': 'test last_name',
            'company': 'test company'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test if the created user already exist in the db"""
        payload = {
            'email': 'testmihai@apidev.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'test last_name',
            'company': 'test company'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """test if te password is shorter than 5 characters"""
        payload = {
            'email': 'testmihai@apidev.com',
            'password': 'pw',
            'first_name': 'Test',
            'last_name': 'test last_name',
            'company': 'test company'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test to check if a token was returned after a valid login"""
        payload = {'email': 'testmihai@apidev.com', 'password': 'testpass123'}
        create_user(**payload)
        res = self.client.post(CREATE_TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Check that token is not given with invalid credentials"""
        payload = {'email': 'testmihai@apidev.com', 'password': 'wrongpass'}
        create_user(email='testmihai@apidev.com', password='testpass123')
        res = self.client.post(CREATE_TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if the user doesn't exist"""
        payload = {'email': 'testmihai@apidev.com', 'password': 'testpass123'}
        res = self.client.post(CREATE_TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_fields(self):
        res = self.client.post(
            CREATE_TOKEN_URL, {'email': 'one', 'password': ''}
            )

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorised(self):
        """Test the authentication is requred for the user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivetUserApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.user = create_user(
            email='testmhai@apidev.com',
            password='testpass123',
            first_name='first_name',
            last_name='test last_name',
            company='test company'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """test retirieving profile for logged in user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'company': self.user.company
        })

    def test_post_me_not_allowed(self):
        """Test that POST is not allowed on the me URL"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(
            res.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
            )

    def test_update_user_profile(self):
        """test updating user profile for authenticated user"""
        payload = {
            'first_name': 'new first_name',
            'password': 'newtestpass123',
            'last_name': 'new last_name',
            'company': 'new company'
            }
        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, payload['first_name'])
        self.assertEqual(self.user.last_name, payload['last_name'])
        self.assertEqual(self.user.company, payload['company'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
