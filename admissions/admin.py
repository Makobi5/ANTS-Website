from django.contrib import admin
from .models import StudentApplication, StudentProfile

# 1. Configuration for Student Applications
@admin.register(StudentApplication)
class StudentApplicationAdmin(admin.ModelAdmin):
    # Columns to show in the list
    list_display = ('full_name', 'program_choice', 'email', 'status', 'submitted_at')
    
    # Sidebar filters
    list_filter = ('status', 'program_choice', 'submitted_at')
    
    # Search bar (Search by name or email)
    search_fields = ('full_name', 'email', 'phone')
    
    # Allow changing status (Pending -> Approved) directly from the list
    list_editable = ('status',)
    
    # Default sorting (Newest first)
    ordering = ('-submitted_at',)

# 2. Configuration for Student Profiles (Phone Numbers)
@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    search_fields = ('user__username', 'phone_number')