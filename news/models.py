from django.db import models
from django.contrib.auth.models import User

class NewsArticle(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='news_images/')
    date_posted = models.DateTimeField(auto_now_add=True)
    summary = models.TextField(max_length=500, help_text="Short text for the sidebar (approx 1 paragraph)")
    content = models.TextField(help_text="Full article content")
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date_posted'] # Newest first

    def __str__(self):
        return self.title