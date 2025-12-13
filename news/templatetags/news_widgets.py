from django import template
from news.models import NewsArticle

register = template.Library()

@register.inclusion_tag('news/sidebar_widget.html')
def show_latest_news(count=3):
    latest_news = NewsArticle.objects.all()[:count]
    return {'latest_news': latest_news}