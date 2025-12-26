from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('who-we-are/', views.who_we_are, name='who_we_are'),
    path('statement-of-faith/', views.statement_of_faith, name='statement_of_faith'),
    path('policies/', views.policies, name='policies'),
    path('schedule/', views.daily_schedule, name='daily_schedule'),
    path('search/', views.global_search, name='global_search'),
]