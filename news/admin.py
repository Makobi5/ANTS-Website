from django.contrib import admin
from .models import NewsArticle, Event, NewsImage, Category

# 1. Register Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

# 2. Inline for Gallery (10 slots for bulk-like uploading)
class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 10 
    min_num = 0
    max_num = 20
    verbose_name = "Gallery Photo"
    verbose_name_plural = "Add Gallery Photos (Select one for each row)"

# 3. Register Article with the Inline
@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date_posted', 'author')
    list_filter = ('category', 'tags', 'date_posted')
    search_fields = ('title', 'content')
    
    # Organize Layout
    fieldsets = (
        ('Main Content', {
            'fields': ('title', 'category', 'content')
        }),
        ('SEO & Metadata', {
            'fields': ('tags', 'summary')
        }),
        ('Featured Image', {
            'fields': ('image', 'author'),
        }),
    )
    
    inlines = [NewsImageInline]

# 4. Register Event
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'location')
    list_filter = ('date',)
    search_fields = ('title',)