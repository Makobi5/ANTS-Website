from django.contrib import admin
from .models import Program

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'duration', 'study_mode', 'is_featured_in_menu')
    list_filter = ('category',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_featured_in_menu',)
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'category', 'duration', 'study_mode', 'summary', 'overview', 'what_you_will_learn', 'requirements', 'image', 'hero_image', 'brochure', 'is_featured_in_menu')
        }),
    )