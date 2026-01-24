import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import NewsArticle, Event, NewsImage, Category, NewsDocument, Subscriber # Import Subscriber

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
    
class NewsDocumentInline(admin.TabularInline):
    model = NewsDocument
    extra = 2 # Shows 2 empty slots by default
    verbose_name = "Attachment"
    verbose_name_plural = "Attach Documents (PDF, Word, etc.)"

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
            'fields': ('image','thumbnail', 'author'),
        }),
    )
    
    inlines = [NewsDocumentInline, NewsImageInline]

# 4. Register Event
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'location')
    list_filter = ('date',)
    search_fields = ('title',)
    
# --- Custom Action to Export Emails to CSV ---
def export_subscribers_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ants_subscribers.csv"'
    writer = csv.writer(response)
    writer.writerow(['Email', 'Date Subscribed']) # Header row

    for subscriber in queryset:
        writer.writerow([subscriber.email, subscriber.date_subscribed])
    return response

export_subscribers_csv.short_description = "Export Selected to CSV"

# --- Subscriber Admin Configuration ---
@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_subscribed') # Show columns
    search_fields = ('email',)      # Enable search bar
    list_filter = ('date_subscribed',) # Enable date filtering sidebar
    actions = [export_subscribers_csv] # Add the export button    