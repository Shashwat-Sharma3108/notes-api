from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserModelTestCase(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='password123'
        )
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.check_password('password123'))

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            first_name='Admin',
            last_name='User',
            password='admin123'
        )
        self.assertIsNotNone(superuser)
        self.assertEqual(superuser.username, 'admin')
        self.assertEqual(superuser.email, 'admin@example.com')
        self.assertEqual(superuser.first_name, 'Admin')
        self.assertEqual(superuser.last_name, 'User')
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.check_password('admin123'))

class TokenEndpointsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='Test@1234')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_obtain_token(self):
        url = reverse('token_obtain_pair')
        data = {'username': self.user.username, 'password': 'Test@1234'}
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_refresh_token(self):
        # Generate a refresh token for the test user
        refresh = RefreshToken.for_user(self.user)
        
        url = reverse('token_refresh')
        data = {'refresh': str(refresh)}
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)