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
    path('testimonial/<int:pk>/', views.testimonial_detail, name='testimonial_detail'),
    path('contact/', views.contact, name='contact'),
     path('students/guild/', views.student_guild, name='student_guild'),
    path('students/alumni/', views.alumni, name='alumni'),
    path('students/life/', views.life_at_ants, name='life_at_ants'),
    path('students/fees/', views.fees_structure, name='fees_structure'),
    path('students/manual/', views.student_manual, name='student_manual'),
]