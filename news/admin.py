import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import NewsArticle, Event, NewsImage, Category, NewsDocument, Subscriber


# 1. Register Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


# 2. Drag-and-drop multi-upload Inline for Gallery
class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 5          # start with 5 empty slots visible
    min_num = 0
    max_num = 100      # effectively unlimited — JS auto-adds rows as needed
    verbose_name = "Gallery Photo"
    verbose_name_plural = "Add Gallery Photos (drag & drop or select multiple)"

    class Media:
       js = ('js/multi_image_upload.js',)


class NewsDocumentInline(admin.TabularInline):
    model = NewsDocument
    extra = 2
    verbose_name = "Attachment"
    verbose_name_plural = "Attach Documents (PDF, Word, etc.)"


# 3. Register Article with the Inline
@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date_posted', 'show_on_slider', 'author')
    list_editable = ('show_on_slider',)
    list_filter = ('show_on_slider', 'category', 'tags', 'date_posted')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Content', {
            'fields': ('title', 'category', 'content')
        }),
        ('Display Settings', {
            'fields': ('show_on_slider', 'tags', 'summary')
        }),
        ('Images', {
            'fields': ('image', 'thumbnail', 'author'),
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
    writer.writerow(['Email', 'Date Subscribed'])
    for subscriber in queryset:
        writer.writerow([subscriber.email, subscriber.date_subscribed])
    return response

export_subscribers_csv.short_description = "Export Selected to CSV"


# --- Subscriber Admin Configuration ---
@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_subscribed')
    search_fields = ('email',)
    list_filter = ('date_subscribed',)
    actions = [export_subscribers_csv]