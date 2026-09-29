import importlib
import os

from django.core import mail
from django.test import SimpleTestCase, TestCase, override_settings
from django.urls import reverse


class EmailConfigurationTests(SimpleTestCase):
    def test_email_backend_uses_environment_settings(self):
        settings_module = importlib.import_module('ants_project.settings')

        original_backend = os.environ.get('DJANGO_EMAIL_BACKEND')
        original_host = os.environ.get('EMAIL_HOST')
        original_user = os.environ.get('EMAIL_HOST_USER')
        original_password = os.environ.get('EMAIL_HOST_PASSWORD')
        original_default_from = os.environ.get('DEFAULT_FROM_EMAIL')

        try:
            os.environ['DJANGO_EMAIL_BACKEND'] = 'django.core.mail.backends.smtp.EmailBackend'
            os.environ['EMAIL_HOST'] = 'smtp.example.com'
            os.environ['EMAIL_HOST_USER'] = 'newsletter@example.com'
            os.environ['EMAIL_HOST_PASSWORD'] = 'secret'
            os.environ['DEFAULT_FROM_EMAIL'] = 'info@example.com'

            importlib.reload(settings_module)

            self.assertEqual(settings_module.EMAIL_BACKEND, 'django.core.mail.backends.smtp.EmailBackend')
            self.assertEqual(settings_module.EMAIL_HOST, 'smtp.example.com')
            self.assertEqual(settings_module.DEFAULT_FROM_EMAIL, 'info@example.com')
        finally:
            if original_backend is None:
                os.environ.pop('DJANGO_EMAIL_BACKEND', None)
            else:
                os.environ['DJANGO_EMAIL_BACKEND'] = original_backend

            if original_host is None:
                os.environ.pop('EMAIL_HOST', None)
            else:
                os.environ['EMAIL_HOST'] = original_host

            if original_user is None:
                os.environ.pop('EMAIL_HOST_USER', None)
            else:
                os.environ['EMAIL_HOST_USER'] = original_user

            if original_password is None:
                os.environ.pop('EMAIL_HOST_PASSWORD', None)
            else:
                os.environ['EMAIL_HOST_PASSWORD'] = original_password

            if original_default_from is None:
                os.environ.pop('DEFAULT_FROM_EMAIL', None)
            else:
                os.environ['DEFAULT_FROM_EMAIL'] = original_default_from

            importlib.reload(settings_module)


class NewsletterSubscriptionTests(TestCase):
    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_subscription_sends_confirmation_email(self):
        response = self.client.post(reverse('subscribe'), {'email': 'student@example.com'}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Success! An email was just sent to confirm your subscription.', response.content.decode())
