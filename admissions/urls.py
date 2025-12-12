from django.urls import path
from . import views

urlpatterns = [
    # Portal Authentication
    path('portal/login/', views.student_login, name='student_login'),
    path('portal/signup/', views.student_signup, name='student_signup'),
    path('portal/logout/', views.student_logout, name='student_logout'),
    
    # Student Dashboard (This replaces the old 'success' page)
    path('portal/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('portal/application/<int:pk>/', views.view_application, name='view_application'),
    
    # The Application Form
    path('apply/', views.apply_now, name='apply_now'),
]