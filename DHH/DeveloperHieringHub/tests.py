from unittest.mock import patch

from django.test import TestCase, override_settings
from django.urls import reverse

from .models import BetaJoiner, EmailOTP, PlatformUser


class PublicPageTests(TestCase):
    def test_public_pages_render(self):
        route_names = [
            'index',
            'developers',
            'companies',
            'pricing',
            'join-beta',
            'dashboard',
            'jobs',
            'github-activity',
            'about',
            'how-it-works',
            'security',
            'shortlist',
            'login',
            'developer-signup',
            'hirer-signup',
        ]

        for name in route_names:
            with self.subTest(name=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 200)

    def test_beta_join_form_creates_joiner(self):
        response = self.client.post(
            reverse('join-beta'),
            {
                'full_name': 'Ada Lovelace',
                'email': 'ada@example.com',
                'role': 'developer',
                'company_name': '',
                'github_username': 'ada',
                'message': 'I want early access.',
            },
        )

        self.assertRedirects(response, reverse('join-beta'))
        self.assertEqual(BetaJoiner.objects.count(), 1)

    def test_profile_and_settings_require_login(self):
        for name in ['profile', 'settings']:
            with self.subTest(name=name):
                response = self.client.get(reverse(name))
                self.assertRedirects(response, reverse('login'))

    @override_settings(RESEND_API_KEY='test-key')
    @patch('DeveloperHieringHub.views.send_otp_email')
    def test_email_login_creates_otp(self, send_otp_email):
        PlatformUser.objects.create(
            full_name='Grace Hopper',
            email='grace@example.com',
            role=PlatformUser.ROLE_DEVELOPER,
        )

        response = self.client.post(reverse('login'), {'email': 'grace@example.com'})

        self.assertRedirects(response, reverse('verify-code'))
        self.assertEqual(EmailOTP.objects.count(), 1)
        send_otp_email.assert_called_once()
