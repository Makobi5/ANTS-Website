from django.shortcuts import render, get_object_or_404
from .models import NewsArticle

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