from django.shortcuts import render, get_object_or_404
from .models import NewsArticle
from .models import NewsArticle, Event # <--- Import Event
from django.utils import timezone # <--- Import timezone


def news_list(request):
    # Get all news, newest first
    articles = NewsArticle.objects.all().order_by('-date_posted')
    return render(request, 'news/news_list.html', {'articles': articles})

def news_detail(request, pk):
    # Get specific article by ID (pk)
    article = get_object_or_404(NewsArticle, pk=pk)
    
    # Get recent articles for the sidebar (excluding the current one)
    recent_articles = NewsArticle.objects.exclude(pk=pk).order_by('-date_posted')[:3]
    
    context = {
        'article': article,
        'recent_articles': recent_articles
    }
    return render(request, 'news/news_detail.html', context)

def events_list(request):
    today = timezone.now().date()
    
    # Events happening today or in the future
    upcoming_events = Event.objects.filter(date__gte=today).order_by('date', 'time')
    
    # Events that already happened
    past_events = Event.objects.filter(date__lt=today).order_by('-date', '-time')
    
    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events
    }
    return render(request, 'news/events_list.html', context)

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'news/event_detail.html', {'event': event})

def gallery(request):
    # Fetch articles that have at least one gallery image OR a featured image
    # We prefetch_related to allow grabbing the sub-images efficiently
    articles = NewsArticle.objects.prefetch_related('gallery_images').order_by('-date_posted')
    return render(request, 'news/gallery.html', {'articles': articles})