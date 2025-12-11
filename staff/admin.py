from django.contrib import admin
from .models import StaffMember

@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'category', 'order')
    list_filter = ('category',)
    search_fields = ('name', 'role')
    list_editable = ('order',) # Allows you to reorder people quickly