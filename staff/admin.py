from django.contrib import admin
from .models import StaffMember

@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'category', 'service_department', 'order')
    list_filter = ('category', 'service_department')
    search_fields = ('name', 'role')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('name',)} # <--- Auto-fills URL based on Name