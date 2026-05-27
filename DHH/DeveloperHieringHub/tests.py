from django.test import TestCase
from django.urls import reverse

from .models import BetaJoiner


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
