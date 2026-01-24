from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mass_mail
from django.conf import settings
from .models import NewsArticle, Subscriber

@receiver(post_save, sender=NewsArticle)
def send_new_post_notification(sender, instance, created, **kwargs):
    # Only send if it's a NEW post (not an edit)
    if created:
        subscribers = Subscriber.objects.all()
        
        if subscribers.exists():
            subject = f"New Update from ANTS: {instance.title}"
            message = f"""
            Hello,

            A new article has been posted on the All Nations Theological College website:

            {instance.title}
            
            Read it here: http://127.0.0.1:8000/news/{instance.pk}/
            
            Blessings,
            ANTS Communication Team
            """
            
            # Prepare emails tuple
            # (subject, message, sender, [recipient])
            messages = [
                (subject, message, settings.DEFAULT_FROM_EMAIL, [sub.email])
                for sub in subscribers
            ]
            
            # Send them all at once
            send_mass_mail(messages, fail_silently=True)