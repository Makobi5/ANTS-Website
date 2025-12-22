from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager

# 1. Category Model
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

# 2. News Article Model (Must come BEFORE NewsImage)
class NewsArticle(models.Model):
    title = models.CharField(max_length=200)
    
    # Metadata
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = TaggableManager(help_text="A comma-separated list of tags (e.g. Graduation, Theology)")
    
    # Content
    image = models.ImageField(upload_to='news_images/', verbose_name="Featured Image")
    date_posted = models.DateTimeField(auto_now_add=True)
    summary = models.TextField(max_length=500, help_text="Short summary for the sidebar")
    content = RichTextUploadingField(help_text="Full article content")
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return self.title

# 3. News Image (The Gallery) - THIS WAS CAUSING THE ERROR
class NewsImage(models.Model):
    # This 'article' field is the ForeignKey the error was looking for
    article = models.ForeignKey(NewsArticle, default=None, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='news_gallery/')
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Image for {self.article.title}"

# 4. Event Model (Keep this safe)
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200, default="Main Campus")
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    principal_message = models.TextField(blank=True, null=True, help_text="Optional: Message from the Principal")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return self.title

    @property
    def is_past(self):
        return self.date < timezone.now().date()