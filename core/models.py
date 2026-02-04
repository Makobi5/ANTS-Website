from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from staff.models import StaffMember
import re
from django.utils import timezone

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
class PageBanner(models.Model):
    PAGE_CHOICES = [
        ('WHO_WE_ARE', 'Who We Are'),
        ('STATEMENT', 'Statement of Faith'),
        ('POLICIES', 'University Policies'),
        ('SCHEDULE', 'Daily Schedule'),
        ('GUILD', 'Students Guild')
    ]
    
    page = models.CharField(max_length=50, choices=PAGE_CHOICES, unique=True, help_text="Select which page this banner belongs to")
    image = models.ImageField(upload_to='page_banners/', help_text="Upload a wide image (approx 1200x400px)")
    caption = models.CharField(max_length=200, blank=True, help_text="Optional text to display on the image")

    def __str__(self):
        return self.get_page_display()    
class SliderImage(models.Model):
    title = models.CharField(max_length=100, blank=True, help_text="Main heading on the slide")
    subtitle = models.CharField(max_length=200, blank=True, help_text="Smaller text below heading")
    image = models.ImageField(upload_to='home_slider/', help_text="Upload a large, high-quality image (1920x800px recommended)")
    link = models.CharField(max_length=200, blank=True, help_text="Link for the button (e.g., /admissions/apply/)")
    button_text = models.CharField(max_length=50, default="Learn More", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or "Untitled Slide"    
    
    
class Partner(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='partners/')
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, help_text="e.g. Journalism Alumnus (2024)")
    photo = models.ImageField(upload_to='testimonials/')
    quote = models.TextField(help_text="Short quote for the card (approx 30 words)")
    full_story = RichTextUploadingField(help_text="The full detailed story (Notebook view)") # Uses CKEditor
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name    
# ... existing imports ...

class ContactDepartment(models.Model):
    name = models.CharField(max_length=100, help_text="e.g. Admissions, Students' Welfare")
    order = models.IntegerField(default=0, help_text="Order of display on the page")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class ContactPerson(models.Model):
    department = models.ForeignKey(ContactDepartment, on_delete=models.CASCADE, related_name='people')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, help_text="e.g. 077... / 070...")
    email = models.EmailField()
    
    def __str__(self):
        return self.name    
    
    
class StudentLeader(models.Model):
    CABINET_YEARS = [
        ('2026', '2026/2027 Cabinet'),
        ('2025', '2025/2026 Cabinet'),
        ('2024', '2024/2025 Cabinet'),
    ]

    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, help_text="e.g. Guild President")
    photo = models.ImageField(upload_to='student_leaders/')
    cabinet_year = models.CharField(max_length=10, choices=CABINET_YEARS, default='2026')
    email = models.EmailField(blank=True, null=True, help_text="Optional: Official email (e.g. guild@ants.ac.ug)")
    order = models.IntegerField(default=0, help_text="1 for President, 2 for VP, etc.")

    class Meta:
        ordering = ['-cabinet_year', 'order'] # Show newest cabinet first, then by rank

    def __str__(self):
        return f"{self.name} - {self.role} ({self.cabinet_year})" 

class AlumniMember(models.Model):
    # Personal Info
    full_name = models.CharField(max_length=200)
    graduation_year = models.CharField(max_length=4, help_text="Year of Graduation")
    program = models.CharField(max_length=200, help_text="Course studied at ANTS")
    
    # Professional Info
    current_job = models.CharField(max_length=200, blank=True, help_text="Current Job Title")
    employer = models.CharField(max_length=200, blank=True, help_text="Company or Church Name")
    
    # Contact (Private for Admin, unless you want to show email publicly)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # Public Profile
    photo = models.ImageField(upload_to='alumni_photos/', blank=True, null=True)
    testimonial = models.TextField(blank=True, help_text="A short message about their time at ANTS")
    
    # Approval Logic
    is_approved = models.BooleanField(default=False, verbose_name="Approve for Website")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.graduation_year})"       
    
    
class ServiceDepartment(models.Model):
    name = models.CharField(max_length=100, help_text="e.g. Finance Department, University Library")
    slug = models.SlugField(unique=True, help_text="URL friendly name (e.g. finance-department)")
    
    # The Head of Department (Link to Staff)
    head_of_dept = models.ForeignKey(StaffMember, on_delete=models.SET_NULL, null=True, blank=True, related_name="headed_services")
    head_title = models.CharField(max_length=100, default="Head of Department", help_text="e.g. University Bursar, Librarian")
    
    # Content Tabs
    introduction = RichTextUploadingField(help_text="Main description (Mandate)")
    duties = RichTextUploadingField(blank=True, help_text="Content for 'Duties & Responsibilities' tab")
    staff_content = RichTextUploadingField(blank=True, help_text="Content for 'Staff Members' tab (or list names manually)")
    contact_info = RichTextUploadingField(blank=True, help_text="Address, Email, Phone for this specific department")

    def __str__(self):
        return self.name   
    
    
class Sermon(models.Model):
    title = models.CharField(max_length=200)
    preacher = models.CharField(max_length=100, help_text="e.g. Rev. Victor Jung")
    date_preached = models.DateField()
    youtube_link = models.URLField(help_text="Paste the full YouTube link here")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='sermon_thumbnails/', blank=True, null=True, help_text="Upload a cover photo to display on the Homepage Slider")
    show_on_slider = models.BooleanField(default=False, verbose_name="Show on Homepage Slider")
    
    class Meta:
        ordering = ['-date_preached']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        """Strip whitespace from youtube_link before saving"""
        if self.youtube_link:
            self.youtube_link = self.youtube_link.strip()
        super().save(*args, **kwargs)

    def get_video_id(self):
        """Extract YouTube video ID from various URL formats"""
        if not self.youtube_link:
            return ""
        
        # Strip any whitespace
        link = self.youtube_link.strip()
        
        # Try multiple patterns (in order of likelihood)
        patterns = [
            r'(?:youtube\.com\/watch\?v=)([0-9A-Za-z_-]{11})',  # Standard: youtube.com/watch?v=VIDEO_ID
            r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})',              # Short: youtu.be/VIDEO_ID
            r'(?:youtube\.com\/embed\/)([0-9A-Za-z_-]{11})',    # Embed: youtube.com/embed/VIDEO_ID
            r'(?:youtube\.com\/v\/)([0-9A-Za-z_-]{11})',        # Old: youtube.com/v/VIDEO_ID
            r'(?:youtube\.com\/shorts\/)([0-9A-Za-z_-]{11})',   # Shorts: youtube.com/shorts/VIDEO_ID
        ]
        
        for pattern in patterns:
            match = re.search(pattern, link)
            if match:
                return match.group(1)
        
        # If no pattern matches, return empty string
        return ""
    
    
# Optional: Add these models to your core/models.py if you want to track donations

from django.db import models
from django.utils import timezone

class DonationCategory(models.Model):
    """Categories for different types of donations"""
    CATEGORY_CHOICES = [
        ('SCHOLARSHIP', 'Student Scholarships'),
        ('INFRASTRUCTURE', 'Campus Development'),
        ('LIBRARY', 'Library & Resources'),
        ('GENERAL', 'General Operations'),
        ('OTHER', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    category_type = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='GENERAL')
    description = models.TextField(blank=True)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, 
                                       help_text="Optional fundraising target")
    icon_class = models.CharField(max_length=50, default='fas fa-heart',
                                 help_text="FontAwesome icon class")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text="Display order")
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Donation Categories"
    
    def __str__(self):
        return self.name


class Donation(models.Model):
    """Track donations received"""
    PAYMENT_METHOD_CHOICES = [
        ('BANK', 'Bank Transfer'),
        ('MTN', 'MTN Mobile Money'),
        ('AIRTEL', 'Airtel Money'),
        ('CASH', 'Cash'),
        ('CHECK', 'Cheque'),
        ('OTHER', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending Confirmation'),
        ('CONFIRMED', 'Confirmed'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    # Donor Information
    donor_name = models.CharField(max_length=200)
    donor_email = models.EmailField(blank=True)
    donor_phone = models.CharField(max_length=20, blank=True)
    is_anonymous = models.BooleanField(default=False, help_text="Hide donor name publicly")
    
    # Donation Details
    category = models.ForeignKey(DonationCategory, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='UGX')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    transaction_reference = models.CharField(max_length=100, blank=True, 
                                            help_text="Bank reference or mobile money transaction ID")
    
    # Purpose & Notes
    purpose = models.CharField(max_length=255, blank=True, 
                              help_text="Specific purpose if different from category")
    notes = models.TextField(blank=True, help_text="Internal notes")
    donor_message = models.TextField(blank=True, help_text="Message from donor")
    
    # Status & Tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    date_received = models.DateField(default=timezone.now)
    date_confirmed = models.DateField(null=True, blank=True)
    receipt_issued = models.BooleanField(default=False)
    receipt_number = models.CharField(max_length=50, blank=True, unique=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_received', '-created_at']
    
    def __str__(self):
        return f"{self.donor_name} - {self.currency} {self.amount:,.0f} ({self.get_status_display()})"
    
    def save(self, *args, **kwargs):
        # Auto-generate receipt number if confirmed and not already issued
        if self.status == 'CONFIRMED' and not self.receipt_number:
            from datetime import datetime
            year = datetime.now().year
            count = Donation.objects.filter(
                receipt_number__startswith=f'ANTS-{year}'
            ).count() + 1
            self.receipt_number = f'ANTS-{year}-{count:05d}'
        
        super().save(*args, **kwargs)


class DonationTestimonial(models.Model):
    """Testimonials from donors about their giving experience"""
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200, blank=True, 
                            help_text="e.g., 'Ministry Partner since 2015'")
    photo = models.ImageField(upload_to='testimonials/donors/', blank=True)
    quote = models.TextField(help_text="The testimonial text")
    donation_relationship = models.CharField(max_length=255, blank=True,
                                           help_text="e.g., 'Scholarship Sponsor', 'Monthly Partner'")
    is_featured = models.BooleanField(default=False, help_text="Show on donations page")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name_plural = "Donor Testimonials"
    
    def __str__(self):
        return f"{self.name} - {self.title}"


class DonationImpactStory(models.Model):
    """Stories showing the impact of donations"""
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    featured_image = models.ImageField(upload_to='impact_stories/')
    summary = models.TextField(help_text="Brief summary for cards")
    full_story = models.TextField(help_text="Complete story")
    category = models.ForeignKey(DonationCategory, on_delete=models.SET_NULL, 
                                null=True, blank=True)
    
    # Student or beneficiary details (optional)
    beneficiary_name = models.CharField(max_length=200, blank=True)
    beneficiary_photo = models.ImageField(upload_to='impact_stories/beneficiaries/', blank=True)
    
    is_published = models.BooleanField(default=True)
    publish_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-publish_date']
        verbose_name_plural = "Impact Stories"
    
    def __str__(self):
        return self.title    
# 1. Update OutreachProgram
class OutreachProgram(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='outreach/', verbose_name="Cover Image")
    description = RichTextUploadingField()
    location = models.CharField(max_length=200)
    
    # NEW: Checkbox for Homepage
    show_on_slider = models.BooleanField(default=False, verbose_name="Show on Homepage Slider")
    
    def __str__(self):
        return self.title

# 2. NEW: Outreach Gallery Model (Multiple Photos)
class OutreachImage(models.Model):
    program = models.ForeignKey(OutreachProgram, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='outreach_gallery/')
    
    def __str__(self):
        return f"Image for {self.program.title}"     