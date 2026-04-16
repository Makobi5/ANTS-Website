from django.urls import path
from . import views
from .views import notices_list, notice_detail
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
    path('students/life/sports/', views.life_sports, name='life_sports'),
    path('students/life/housing/', views.life_housing, name='life_housing'),
    path('students/life/dining/', views.life_dining, name='life_dining'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),
    path('chapel/', views.ants_chapel, name='ants_chapel'),
    path('donations/', views.donations, name='donations'),
    path('community-outreach/', views.community_outreach, name='community_outreach'),
    path('noticeboard/',          notices_list,  name='notices_list'),
    path('noticeboard/<int:pk>/', notice_detail, name='notice_detail'),
]