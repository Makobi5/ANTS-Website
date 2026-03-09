from django.db import models
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField

class Program(models.Model):
    # These match the links in your Navbar
    CATEGORY_CHOICES = [
        ('BACHELOR', 'Bachelor Programs'),
        ('DIPLOMA', 'Diploma Programs'),
        ('CERTIFICATE', 'Certificate Programs'),
        ('SHORT', 'Short Courses'),
    ]
    
    is_featured_in_menu = models.BooleanField(
        default=False, 
        help_text="Check this box if you want this specific course to appear directly in the Main Menu dropdown (e.g. ESL, PTC)"
    )

  

    # Basic Info
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, help_text="Auto-generated URL name (e.g. bachelor-of-theology)")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=True, null=True)
    
    # Details
    duration = models.CharField(max_length=100, help_text="e.g. 3 Years")
    study_mode = models.CharField(max_length=100, default="Full-time / Weekend", help_text="e.g. Full-time, Online, Holiday")
    
    # Descriptions
    summary = models.TextField(help_text="Short description for the list page (2-3 sentences)")
    overview = RichTextUploadingField(help_text="Full detailed description of the course")
    what_you_will_learn = models.TextField(
    blank=True, null=True,
    help_text="Describe what students will learn in this program."
)
    requirements = models.TextField(help_text="Admission requirements (e.g. 2 Principal Passes)")
    
    # Files
    image = models.ImageField(upload_to='program_images/', blank=True, null=True, help_text="Cover image for the course")
    hero_image = models.ImageField(
        upload_to='program_banners/', 
        blank=True, 
        null=True, 
        verbose_name="Top Header Banner (Wide)",
        help_text="Upload a wide image (1920x600) for the top background. If empty, a default blue banner is used."
    )
    brochure = models.FileField(upload_to='program_files/', blank=True, null=True, help_text="Upload PDF Fee Structure or Brochure")

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Automatically create the URL slug from the title if missing
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title