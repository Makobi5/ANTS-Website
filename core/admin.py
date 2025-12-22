from django.contrib import admin
from .models import Policy, DailySchedule, PageBanner,SliderImage  # Import it here

@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')
    search_fields = ('title',)

@admin.register(DailySchedule)
class DailyScheduleAdmin(admin.ModelAdmin):
    list_display = ('day_category', 'period', 'start_time', 'activity', 'location')
    list_filter = ('day_category', 'period')
    list_editable = ('activity', 'location')
    
    # Modern Time Picker override
    from django.db import models
    from django import forms
    formfield_overrides = {
        models.TimeField: {'widget': forms.TimeInput(attrs={'type': 'time'})},
    }

@admin.register(PageBanner)
class PageBannerAdmin(admin.ModelAdmin):
    list_display = ('page', 'caption')

@admin.register(SliderImage)
class SliderImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')    