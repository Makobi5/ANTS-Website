from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_list, name='news_list'),
    path('<int:pk>/', views.news_detail, name='news_detail'),
        # NEW Events Path
    path('events/', views.events_list, name='events_list'),
    path('event/<int:pk>/', views.event_detail, name='event_detail'),
    path('gallery/', views.gallery, name='gallery'),
]