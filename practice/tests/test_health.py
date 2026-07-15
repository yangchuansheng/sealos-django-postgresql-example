import secrets

from django.conf import settings
from django.test import SimpleTestCase


class HealthEndpointTests(SimpleTestCase):
    def test_health_returns_safe_deterministic_identity(self):
        response = self.client.get('/health/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {'status': 'ok', 'service': 'django', 'framework': 'Django'},
        )

    def test_production_settings_contract_uses_secure_environment_values(self):
        with self.settings(
            SECRET_KEY=secrets.token_urlsafe(32),
            DEBUG=False,
            ALLOWED_HOSTS=['example.test'],
            SECURE_SSL_REDIRECT=True,
            SESSION_COOKIE_SECURE=True,
            CSRF_COOKIE_SECURE=True,
            SECURE_HSTS_SECONDS=3600,
            SECURE_HSTS_INCLUDE_SUBDOMAINS=True,
            STATIC_ROOT=settings.BASE_DIR / 'staticfiles',
            MEDIA_ROOT=settings.BASE_DIR / 'media',
        ):
            self.assertFalse(settings.DEBUG)
            self.assertEqual(settings.ALLOWED_HOSTS, ['example.test'])
            self.assertTrue(settings.SECURE_SSL_REDIRECT)
            self.assertTrue(settings.SESSION_COOKIE_SECURE)
            self.assertTrue(settings.CSRF_COOKIE_SECURE)
            self.assertGreater(settings.SECURE_HSTS_SECONDS, 0)
            self.assertTrue(settings.SECURE_HSTS_INCLUDE_SUBDOMAINS)
            self.assertEqual(settings.SECURE_PROXY_SSL_HEADER[1], 'https')
            self.assertTrue(str(settings.STATIC_ROOT).endswith('staticfiles'))
            self.assertTrue(str(settings.MEDIA_ROOT).endswith('media'))
