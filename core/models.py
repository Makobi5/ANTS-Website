from django.db import models

# Create your models here.
class Policy(models.Model):
    title = models.CharField(max_length=200, help_text="e.g. Academic Integrity Policy")
    description = models.TextField(blank=True, help_text="Short summary of what is inside")
    file = models.FileField(upload_to='policies/', help_text="Upload the PDF here")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class DailySchedule(models.Model):
        # Options matching your screenshot
    DAY_CHOICES = [
            ('MONDAY-FRIDAY', 'Monday - Friday'),
            ('MONDAY', 'Monday'),
            ('TUESDAY', 'Tuesday'),
            ('WEDNESDAY', 'Wednesday'),
            ('THURSDAY', 'Thursday'),
            ('FRIDAY', 'Friday'),
            ('SATURDAY', 'Saturday'),
            ('SUNDAY', 'Sunday'),
        ]
    
    PERIOD_CHOICES = [
        ('AM', 'AM'),
        ('PM', 'PM'),
        ('AM/PM', 'AM/PM'), # For whole day events
    ]

    # New Fields for the Layout
    day_category = models.CharField(max_length=20, choices=DAY_CHOICES, default='MONDAY-FRIDAY')
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES, default='AM')
    
    # Existing Fields
    start_time = models.TimeField()
    end_time = models.TimeField()
    activity = models.CharField(max_length=200)
    location = models.CharField(max_length=200, default="Campus")
    is_highlighted = models.BooleanField(default=False)

    class Meta:
        # Sort by Day order (Monday first), then AM/PM, then Time
        ordering = ['day_category', 'start_time'] 

    def __str__(self):
        return f"{self.day_category} - {self.activity}"