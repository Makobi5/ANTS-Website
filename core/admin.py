from django.contrib import admin
from .models import Policy, DailySchedule, PageBanner,SliderImage  # Import it here
from django.utils.html import mark_safe

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
    # Update list_display to show the preview first
    list_display = ('image_preview', 'title', 'created_at')
    
    # Enable clicking on the image to edit
    list_display_links = ('image_preview', 'title')

    # Create the function to render the image
    def image_preview(self, obj):
        if obj.image:
            # Renders a small 150px wide image
            return mark_safe(f'<img src="{obj.image.url}" width="150" style="border-radius:5px; border:1px solid #ccc;" />')
        return "No Image"
    
    image_preview.short_description = 'Slide Preview'   