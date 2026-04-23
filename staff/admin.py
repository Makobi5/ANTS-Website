from django.contrib import admin
from .models import StaffMember
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import StaffMember, UserProfile

@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'category', 'service_department', 'order')
    list_filter = ('category', 'service_department')
    search_fields = ('name', 'role')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('name',)} # <--- Auto-fills URL based on Name
    
# Define an inline for the Profile so it shows up on the User page
class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'UI Preferences & Staff Link'

# Unregister the default User admin and register our customized one
admin.site.unregister(User)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_theme')
    
    def get_theme(self, instance):
        return instance.profile.get_ui_theme_display()
    get_theme.short_description = 'UI Theme'    
    
    # 2. THIS INJECTS THE THEME CLASS INTO THE BODY
    class Media:
        css = {
            'all': ('admin/css/admin_custom.css',)
        }
