from django.db import models
from django.contrib.auth.models import User
from academics.models import Program


# This extends the User to store a Phone Number
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.user.username
    
    
class StudentApplication(models.Model):
    # --- 1. PERSONAL DETAILS ---
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]
    MARITAL_CHOICES = [('Single', 'Single'), ('Married', 'Married'), ('Separated', 'Separated')]
    
    full_name = models.CharField(max_length=200, verbose_name="Full Name")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(help_text="YYYY-MM-DD")
    marital_status = models.CharField(max_length=20, choices=MARITAL_CHOICES)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    place_of_birth = models.CharField(max_length=100)
    tribe = models.CharField(max_length=100, blank=True)
    nationality = models.CharField(max_length=100)
    
    phone = models.CharField(max_length=20, verbose_name="Telephone No.")
    email = models.EmailField(verbose_name="Email Address")
    permanent_address = models.TextField(verbose_name="Permanent Address")

    # Next of Kin / Family Contact
    next_of_kin_name = models.CharField(max_length=200, verbose_name="Next of Kin Name")
    next_of_kin_contact = models.CharField(max_length=100, verbose_name="Next of Kin Phone")
    next_of_kin_relationship = models.CharField(max_length=50, verbose_name="Relationship (e.g. Father/Spouse)")

    # --- 2. CHURCH & RELIGIOUS INFO (From PDF) ---
    attending_church = models.CharField(max_length=200, verbose_name="Attending Church")
    church_location = models.CharField(max_length=200, verbose_name="Location of Church")
    church_title = models.CharField(max_length=100, blank=True, verbose_name="Your Title (e.g. Pastor/Elder)")
    baptism_date = models.CharField(max_length=50, blank=True, verbose_name="Time of Baptism")
    senior_pastor = models.CharField(max_length=200, verbose_name="Senior Pastor's Name")
    pastor_contact = models.CharField(max_length=100, verbose_name="Pastor's Contact")

    # --- 3. EDUCATIONAL BACKGROUND ---
    # We use a text field for simplicity, asking them to list schools
    education_history = models.TextField(
        verbose_name="Educational Background",
        help_text="List your previous schools: Institute, Period, and Certificate/Degree obtained."
    )

    # --- 4. PROGRAM & FINANCE ---
    program_choice = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, verbose_name="Program Applied For")
    
    FINANCE_CHOICES = [
        ('Private', 'Private Funds'),
        ('Scholarship', 'Scholarship from ANTS'),
        ('Sponsor', 'Sponsorship through Sponsor'),
    ]
    finance_method = models.CharField(max_length=20, choices=FINANCE_CHOICES, verbose_name="How do you intend to fund your studies?")
    sponsor_name = models.CharField(max_length=200, blank=True, verbose_name="Sponsor Name (if applicable)")

    # --- 5. ATTACHMENTS ---
    passport_photo = models.ImageField(upload_to='applications/photos/', verbose_name="Passport Photo")
    academic_documents = models.FileField(upload_to='applications/docs/', verbose_name="Academic Transcripts/Certificates (PDF)")
    recommendation_letter = models.FileField(upload_to='applications/docs/', blank=True, null=True, verbose_name="Recommendation Letter (Optional)")

    # System Fields
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending', choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')])

    def __str__(self):
        return f"{self.full_name} - {self.program_choice}"