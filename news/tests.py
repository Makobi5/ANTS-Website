import importlib
import os

from django.core import mail
from django.test import SimpleTestCase, TestCase, override_settings
from django.urls import reverse
from unittest.mock import patch
from django.contrib.auth.models import User
from .models import Event, NewsArticle, Subscriber
from core.models import ChapelEvent


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
        self.assertTrue(Subscriber.objects.filter(email='student@example.com').exists())
        self.assertIn('You are subscribed! A welcome email has been sent.', response.content.decode())
        self.assertContains(response, '.newsletter-form-wrapper { display: none !important; }')

    def test_duplicate_subscription_is_not_shown_as_success(self):
        Subscriber.objects.create(email='student@example.com')

        response = self.client.post(reverse('subscribe'), {'email': 'STUDENT@example.com'}, follow=True)

        self.assertContains(response, 'You are already subscribed!')
        self.assertNotContains(response, 'Success!')
        self.assertContains(response, 'newsletter-form-wrapper')
        self.assertEqual(Subscriber.objects.count(), 1)

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    @patch('news.views.EmailMultiAlternatives.send', side_effect=OSError('mail unavailable'))
    def test_failed_confirmation_email_does_not_create_subscriber(self, _send_email):
        response = self.client.post(reverse('subscribe'), {'email': 'student@example.com'}, follow=True)

        self.assertContains(response, 'We could not complete your subscription')
        self.assertContains(response, 'newsletter-form-wrapper')
        self.assertFalse(Subscriber.objects.filter(email='student@example.com').exists())

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_new_events_notify_subscribers(self):
        Subscriber.objects.create(email='student@example.com')

        Event.objects.create(
            title='Open Day',
            description='Visit the campus.',
            date='2026-10-10',
            time='09:00',
            location='Main Campus',
        )
        ChapelEvent.objects.create(title='Founders Chapel', date='2026-10-11')

        self.assertEqual(len(mail.outbox), 2)
        self.assertIn('New ANTS Event: Open Day', mail.outbox[0].subject)
        self.assertIn('https://www.ants.ac.ug/news/events/open-day/', mail.outbox[0].body)
        self.assertIn('New ANTS Chapel Event: Founders Chapel', mail.outbox[1].subject)

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_new_article_notification_includes_title_and_summary(self):
        Subscriber.objects.create(email='student@example.com')
        author = User.objects.create_user(username='editor')

        NewsArticle.objects.create(
            title='Graduation Schedule Released',
            image='news_images/graduation.jpg',
            summary='Graduation begins at 10:00 AM on Saturday.',
            content='<p>Full article details.</p>',
            author=author,
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'New article from ANTS: Graduation Schedule Released')
        self.assertIn('Title: Graduation Schedule Released', mail.outbox[0].body)
        self.assertIn('Summary: Graduation begins at 10:00 AM on Saturday.', mail.outbox[0].body)
