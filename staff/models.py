from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    service_department = models.ForeignKey('core.ServiceDepartment', on_delete=models.SET_NULL, null=True, blank=True, related_name='staff_list')
    qualifications = models.CharField(max_length=300, blank=True, help_text="e.g. MSc. CS, CCNA, BIT")
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
    
class UserProfile(models.Model):
    THEME_CHOICES = [
        ('default', 'Professional Blue (Default)'),
        ('dark', 'Midnight Dark'),
        ('light', 'Clean Light'),
        ('accent', 'University Gold'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # Links the login user to the public StaffMember record if applicable
    staff_record = models.OneToOneField('StaffMember', on_delete=models.SET_NULL, null=True, blank=True)
    
    # UI Customization
    ui_theme = models.CharField(max_length=20, choices=THEME_CHOICES, default='default')
    
    def __str__(self):
        return f"Profile for {self.user.username}"

# Automatic profile creation when a new User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()    