from django.db import models
from django.utils.text import slugify

class StaffMember(models.Model):
    CATEGORY_CHOICES = [
        ('PRINCIPAL', 'The Principal'),
        ('MANAGEMENT', 'Management & Admin'),
        ('OFFICE', 'Office Staff'),
        ('ACADEMIC', 'Academic Staff'),
        ('SUPPORT', 'Support Staff'),
    ]

    # Basic Info
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, help_text="Auto-generated part of the URL (e.g. prof-joy-kwesiga)")
    role = models.CharField(max_length=100, help_text="e.g. Dean of Students")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    photo = models.ImageField(upload_to='staff_photos/', blank=True, null=True)
    order = models.IntegerField(default=0, help_text="Lower numbers appear first")
    
    # Contact Info
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    
    # Detailed Info (For the "Read More" page)
    bio = models.TextField(blank=True, help_text="Main biography text")
    cv = models.FileField(upload_to='staff_cvs/', blank=True, null=True, help_text="Upload PDF Resume/CV")
    
    # Tabs Data
    qualifications = models.TextField(blank=True, help_text="List qualifications here")
    research_interests = models.TextField(blank=True, help_text="Areas of research")
    publications = models.TextField(blank=True, help_text="List of publications")
    projects = models.TextField(blank=True, help_text="Current or past projects")

    class Meta:
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        # Auto-generate the URL slug from the name if it's empty
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.role}"