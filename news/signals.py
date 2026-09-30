from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mass_mail
from django.conf import settings
from django.utils.html import strip_tags
from .models import NewsArticle, Subscriber
from .models import Event
from core.models import ChapelEvent
from core.models import Notice

def _notify_subscribers(subject, content, url):
    subscribers = Subscriber.objects.all()
    if not subscribers.exists():
        return

    message = f"""Hello,

{content}

Read it here: {settings.SITE_URL}{url}

Blessings,
ANTS Communication Team"""
    mail_messages = [
        (subject, message, settings.DEFAULT_FROM_EMAIL, [subscriber.email])
        for subscriber in subscribers
    ]
    send_mass_mail(mail_messages, fail_silently=True)


@receiver(post_save, sender=NewsArticle)
def send_new_post_notification(sender, instance, created, **kwargs):
    if created:
        summary = instance.summary.strip() or strip_tags(instance.content).strip()
        summary = " ".join(summary.split())[:500]
        _notify_subscribers(
            f"New article from ANTS: {instance.title}",
            f"Title: {instance.title}\n\nSummary: {summary}",
            f"/news/{instance.slug}/",
        )


@receiver(post_save, sender=Event)
def send_new_event_notification(sender, instance, created, **kwargs):
    if created:
        _notify_subscribers(
            f"New ANTS Event: {instance.title}",
            f"A new event has been announced for {instance.date} at {instance.location}:",
            f"/news/events/{instance.slug}/",
        )


@receiver(post_save, sender=ChapelEvent)
def send_new_chapel_event_notification(sender, instance, created, **kwargs):
    if created:
        _notify_subscribers(
            f"New ANTS Chapel Event: {instance.title}",
            f"A new chapel event has been announced for {instance.date}:",
            "/news/events/",
        )


@receiver(pre_save, sender=Notice)
def remember_notice_published_state(sender, instance, **kwargs):
    if instance.pk:
        instance._was_published = sender.objects.filter(pk=instance.pk).values_list(
            'is_published', flat=True
        ).first()
    else:
        instance._was_published = False


@receiver(post_save, sender=Notice)
def send_new_notice_notification(sender, instance, created, **kwargs):
    if instance.is_published and (created or not getattr(instance, '_was_published', False)):
        category = instance.get_category_display()
        if instance.category == 'jobs':
            subject = f"New job opportunity from ANTS: {instance.title}"
        else:
            subject = f"New ANTS Notice: {instance.title}"
        content = strip_tags(instance.content)
        _notify_subscribers(
            subject,
            f"{category}\n\n{content}",
            instance.get_absolute_url(),
        )