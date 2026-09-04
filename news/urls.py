from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_list, name='news_list'),
    
        # NEW Events Path
    path('events/', views.events_list, name='events_list'),
    path('events/<slug:slug>/', views.event_detail, name='event_detail'),
    path('gallery/', views.gallery, name='gallery'),
    path('subscribe/', views.subscribe_newsletter, name='subscribe'),
    path('<slug:slug>/', views.news_detail, name='news_detail'),
]