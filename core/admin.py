from django.contrib import admin
from .models import Policy, DailySchedule, PageBanner,SliderImage  # Import it here
from django.utils.html import mark_safe
from .models import  Partner, Testimonial # <--- Add imports
from .models import ContactDepartment, ContactPerson
from .models import StudentLeader

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
    
    
@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'created_at') # Added created_at to see when it was added
    list_display_links = ('name',) # <--- This makes the name clickable for editing  
    
class ContactPersonInline(admin.TabularInline):
    model = ContactPerson
    extra = 1

@admin.register(ContactDepartment)
class ContactDepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    inlines = [ContactPersonInline]  
    
@admin.register(StudentLeader)
class StudentLeaderAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'cabinet_year', 'order')
    list_filter = ('cabinet_year',)
    list_editable = ('order',)      