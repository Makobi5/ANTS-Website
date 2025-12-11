from django.urls import path
from . import views

urlpatterns = [
    # List Page (e.g. /programs/bachelors/)
    path('category/<str:category_slug>/', views.program_list, name='program_list'),
    
    # Detail Page (e.g. /programs/bachelor-of-theology/)
    path('course/<slug:slug>/', views.program_detail, name='program_detail'),
]