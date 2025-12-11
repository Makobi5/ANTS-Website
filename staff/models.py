from django.db import models

class StaffMember(models.Model):
    CATEGORY_CHOICES = [
        ('PRINCIPAL', 'The Principal'),
        ('MANAGEMENT', 'Management & Admin'),
        ('ACADEMIC', 'Academic Staff'),
        ('SUPPORT', 'Support Staff'),
    ]

    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, help_text="e.g. Dean of Students")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='staff_photos/', blank=True, null=True)
    order = models.IntegerField(default=0, help_text="Lower numbers appear first (e.g. Principal = 1)")
    
    # Social links (Optional)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ['order', 'name'] # Sort by importance, then name

    def __str__(self):
        return f"{self.name} - {self.role}"