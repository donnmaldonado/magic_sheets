from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

class NavbarTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_navbar_unauthenticated(self):
        """Test navbar elements for unauthenticated users"""
        response = self.client.get(reverse('home'))
        
        self.assertEqual(response.status_code, 200)
        # Check for login and signup buttons
        self.assertContains(response, 'href="/login/"')
        self.assertContains(response, 'href="/signup/"')
        # Verify authenticated-only buttons don't appear
        self.assertNotContains(response, 'Community Sheets')
        self.assertNotContains(response, 'Saved Sheets')
        self.assertNotContains(response, 'Create Sheet')
        self.assertNotContains(response, 'Dashboard')
        self.assertNotContains(response, 'Logout')

    def test_navbar_authenticated(self):
        """Test navbar elements for authenticated users"""
        # Log the user in
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('home'))
        
        self.assertEqual(response.status_code, 200)
        # Check for authenticated user buttons
        self.assertContains(response, 'Community Sheets')
        self.assertContains(response, 'Saved Sheets')
        self.assertContains(response, 'Create Sheet')
        self.assertContains(response, 'Dashboard')
        self.assertContains(response, 'Logout')
        # Verify login/signup buttons don't appear
        self.assertNotContains(response, 'Login</a>')
        self.assertNotContains(response, 'Sign Up</a>')

    def test_navbar_brand(self):
        """Test navbar brand presence"""
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'MagicSheets')

    def test_logout_functionality(self):
        """Test that the logout button works"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('logout'))
        
        # Should redirect after logout
        self.assertEqual(response.status_code, 302)
        
        # Verify user is logged out
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Login</a>')

    def test_navbar_responsive_elements(self):
        """Test presence of responsive elements"""
        response = self.client.get(reverse('home'))
        
        # Check for hamburger menu button
        self.assertContains(response, 'navbar-toggler')
        self.assertContains(response, 'navbar-toggler-icon')
        self.assertContains(response, 'data-bs-toggle="collapse"')