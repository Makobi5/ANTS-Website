from django.urls import path
from . import views

urlpatterns = [
    # The main full list (Staff Directory)
    path('', views.staff_list, name='staff_list'),
    
    # New specific routes
    path('principal/', views.principal_profile, name='principal_profile'),
    path('management/', views.management_list, name='management_list'),
    
    # The detail page (Must be last so it doesn't conflict with specific words)
    path('<slug:slug>/', views.staff_detail, name='staff_detail'),
]