from django.contrib import admin
from .models import StudentApplication, StudentProfile
from django.urls import path, reverse  # Cleaned up duplicate imports
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from .views import download_application_pdf

# 1. Configuration for Student Applications
@admin.register(StudentApplication)
class StudentApplicationAdmin(admin.ModelAdmin):
    # 1. We moved 'download_pdf_link' to the front so it's visible without scrolling
    list_display = ('full_name', 'download_pdf_link', 'program_choice', 'email', 'status', 'submitted_at')
    
    list_filter = ('status', 'program_choice', 'submitted_at')
    search_fields = ('full_name', 'email', 'phone')
    list_editable = ('status',)
    ordering = ('-submitted_at',)
    
    # 2. This ensures the "Download Headed PDF" appears in the Action dropdown
    actions = ['export_to_pdf']

    def download_pdf_link(self, obj):
        url = reverse('admin:admin_download_pdf', args=[obj.pk])
        return format_html(
            '<a class="button" href="{}" target="_blank" '
            'style="background-color: #4a148c; color: white; padding: 4px 12px; '
            'border-radius: 20px; font-size: 11px; white-space: nowrap; '
            'display: inline-block; text-align: center; min-width: 100px;">'
            'Download PDF'
            '</a>', 
            url
        )
        download_pdf_link.short_description = "Form"

    # Bulk Action Logic
    def export_to_pdf(self, request, queryset):
        # If multiple are selected, for now we download the first one. 
        # (I can show you how to zip them all together later if needed!)
        if queryset.count() >= 1:
            return download_application_pdf(request, queryset.first().id)
    export_to_pdf.short_description = "Download Headed PDF (First Selected)"

    # Custom URL Registration
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('<int:application_id>/pdf/', self.admin_site.admin_view(download_application_pdf), name='admin_download_pdf'),
        ]
        return my_urls + urls
@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    search_fields = ('user__username', 'phone_number')