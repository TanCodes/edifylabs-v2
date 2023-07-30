from django.test import TestCase

# Create your tests here.
#Test code for Login Authentication

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class LoginPageTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
        self.login_url = reverse('loginPage')
        self.logout_url = reverse('logoutPage')
        self.ourstory_url = reverse('ourstory')
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_signup(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)

        data = {
            'name': 'testuser',
            'email': 'testuser@example.com',
            'pwd': 'testpassword',
            'pwdfinal': 'testpassword'
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'LOGIN')

    def test_login_page(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

        data = {
            'login_username': 'testuser',
            'login_pass': 'testpassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

        # Attempt login with incorrect credentials
        data = {
            'login_username': 'testuser',
            'login_pass': 'incorrectpassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Error_message_unauthorized')

    def test_logout_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('loginPage'))

    def test_ourstory_page(self):
        response = self.client.get(self.ourstory_url)
        self.assertEqual(response.status_code, 200)

    def test_authenticated_home_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'OkNoted | HOME')

    def test_unauthenticated_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('loginPage'))


class SignupPageTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')

    def test_signup_page(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)


