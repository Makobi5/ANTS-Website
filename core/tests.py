from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Notice
from news.models import Subscriber


@override_settings(
	EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
	DEFAULT_FROM_EMAIL='info@ants.ac.ug',
	SITE_URL='https://www.ants.ac.ug',
)
class NoticeboardTests(TestCase):
	def setUp(self):
		Subscriber.objects.create(email='subscriber@example.com')

	def test_job_opportunities_category_filters_notices(self):
		Notice.objects.create(
			title='Lecturer vacancy',
			content='Apply by October 15.',
			category='jobs',
		)
		Notice.objects.create(
			title='Semester dates',
			content='The semester starts soon.',
			category='academic',
		)

		response = self.client.get(reverse('notices_list'), {'category': 'jobs'})

		self.assertContains(response, 'Lecturer vacancy')
		self.assertContains(response, 'Job Opportunities')
		self.assertNotContains(response, 'Semester dates')

		home_response = self.client.get(reverse('home'))
		self.assertContains(home_response, '?category=jobs')

	def test_published_job_notice_emails_subscriber_from_school_address(self):
		notice = Notice.objects.create(
			title='Lecturer vacancy',
			content='<p>Apply by October 15.</p>',
			category='jobs',
		)

		self.assertEqual(len(mail.outbox), 1)
		self.assertEqual(mail.outbox[0].from_email, 'info@ants.ac.ug')
		self.assertEqual(mail.outbox[0].subject, 'New job opportunity from ANTS: Lecturer vacancy')
		self.assertIn(f'https://www.ants.ac.ug{notice.get_absolute_url()}', mail.outbox[0].body)
		self.assertIn('Apply by October 15.', mail.outbox[0].body)

	def test_notice_detail_uses_unique_slug_and_redirects_old_numeric_url(self):
		first_notice = Notice.objects.create(
			title='Lecturer vacancy',
			content='Apply by October 15.',
			category='jobs',
		)
		second_notice = Notice.objects.create(
			title='Lecturer vacancy',
			content='A second vacancy.',
			category='jobs',
		)

		self.assertEqual(first_notice.slug, 'lecturer-vacancy')
		self.assertEqual(second_notice.slug, 'lecturer-vacancy-2')
		self.assertContains(self.client.get(first_notice.get_absolute_url()), first_notice.title)

		legacy_response = self.client.get(f'/noticeboard/{first_notice.pk}/')
		self.assertEqual(legacy_response.status_code, 301)
		self.assertEqual(legacy_response['Location'], first_notice.get_absolute_url())

	def test_draft_notice_emails_once_when_published(self):
		notice = Notice.objects.create(
			title='Teaching assistant vacancy',
			content='Apply soon.',
			category='jobs',
			is_published=False,
		)
		self.assertEqual(len(mail.outbox), 0)

		notice.is_published = True
		notice.save()
		self.assertEqual(len(mail.outbox), 1)

		notice.title = 'Updated teaching assistant vacancy'
		notice.save()
		self.assertEqual(len(mail.outbox), 1)


@override_settings(SITE_URL='https://www.ants.ac.ug')
class CanonicalDomainTests(TestCase):
	def test_apex_domain_redirects_to_www_and_preserves_path_and_query(self):
		response = self.client.get(
			'/noticeboard/?category=jobs',
			HTTP_HOST='ants.ac.ug',
		)

		self.assertEqual(response.status_code, 301)
		self.assertEqual(
			response['Location'],
			'https://www.ants.ac.ug/noticeboard/?category=jobs',
		)

	def test_www_domain_serves_site_without_redirect(self):
		response = self.client.get('/', HTTP_HOST='www.ants.ac.ug')

		self.assertEqual(response.status_code, 200)
