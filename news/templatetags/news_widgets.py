from django import template
from django.utils import timezone
from news.models import NewsArticle, Event

register = template.Library()

@register.inclusion_tag('news/sidebar_widget.html')
def show_latest_news(count=3):
    today = timezone.now().date()
    
    # If count is 0, we send an empty list for news
    if count > 0:
        latest_news = NewsArticle.objects.all()[:count]
    else:
        latest_news = [] # Empty list
    
    upcoming_events = Event.objects.filter(date__gte=today).order_by('date')[:3]
    
    return {
        'latest_news': latest_news,
        'upcoming_events': upcoming_events
    }