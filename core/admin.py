from django.contrib import admin
from .models import Policy, DailySchedule
from django.db import models  # <--- Import this
from django import forms 

@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')
    search_fields = ('title',)

@admin.register(DailySchedule)
class DailyScheduleAdmin(admin.ModelAdmin):
    list_display = ('day_category', 'period', 'start_time', 'activity', 'location')
    list_filter = ('day_category', 'period') # Adds a sidebar filter
    list_editable = ('activity', 'location')
    
    # ⬇️ ADD THIS BLOCK ⬇️
    formfield_overrides = {
        models.TimeField: {'widget': forms.TimeInput(attrs={'type': 'time'})},
    }