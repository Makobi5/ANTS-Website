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
    MARITAL_CHOICES = [
        ('Single', 'Single'), 
        ('Married', 'Married'), 
        ('Separated', 'Separated'),
        ('Widowed', 'Widowed')
    ]
    
    full_name = models.CharField(max_length=200, verbose_name="Full Name")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(help_text="YYYY-MM-DD")
    marital_status = models.CharField(max_length=20, choices=MARITAL_CHOICES)
    place_of_birth = models.CharField(max_length=100, default="")
    tribe = models.CharField(max_length=100, blank=True, default="")
    nationality = models.CharField(max_length=100, default="Ugandan")
    
    phone = models.CharField(max_length=20, verbose_name="Telephone No.")
    email = models.EmailField(verbose_name="Email Address")
    permanent_address = models.TextField(verbose_name="Permanent Address")

    family_contact_1 = models.CharField(max_length=100, verbose_name="Contact of Family (1)", default="")
    family_contact_2 = models.CharField(max_length=100, blank=True, verbose_name="Contact of Family (2)", default="")
    # Individual family counts (Mirroring the paper form)
    num_father = models.PositiveIntegerField(default=0, verbose_name="Father")
    num_mother = models.PositiveIntegerField(default=0, verbose_name="Mother")
    num_brother = models.PositiveIntegerField(default=0, verbose_name="Brother")
    num_sister = models.PositiveIntegerField(default=0, verbose_name="Sister")
    num_wife = models.PositiveIntegerField(default=0, verbose_name="Wife")
    num_husband = models.PositiveIntegerField(default=0, verbose_name="Husband")
    num_son = models.PositiveIntegerField(default=0, verbose_name="Son")
    num_daughter = models.PositiveIntegerField(default=0, verbose_name="Daughter")
    num_others = models.PositiveIntegerField(default=0, verbose_name="Others")
    # --- 2. CHURCH & RELIGIOUS INFO ---
    attending_church = models.CharField(max_length=200, verbose_name="Attending Church")
    location_of_church = models.CharField(max_length=200, verbose_name="Location of Church", default="")
    church_title = models.CharField(max_length=100, blank=True, verbose_name="Title (e.g. Pastor/Elder)", default="")
    time_of_baptism = models.CharField(max_length=100, blank=True, verbose_name="Time of Baptism", default="")
    senior_pastor = models.CharField(max_length=200, verbose_name="Senior Pastor's Name")
    pastor_contact = models.CharField(max_length=100, verbose_name="Pastor's Contact")
    denomination = models.CharField(max_length=100, blank=True, verbose_name="Denomination", default="")
    person_known_to_ants = models.CharField(max_length=200, blank=True, verbose_name="Name of person known to ANTS", default="")
    
    is_first_study = models.BooleanField(default=True, verbose_name="Is this your first study?")
    english_instruction = models.BooleanField(default=True, verbose_name="Was English the language of instruction?")

    # --- 3. ACADEMIC PRIZES ---
    academic_prizes = models.TextField(blank=True, verbose_name="Academic Prizes and Distinctions", default="")

    # --- 4. PROGRAM & FINANCE ---
    program_choice = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, verbose_name="Program Applied For")
    
    FINANCE_CHOICES = [
        ('Private', 'Private Funds'),
        ('Scholarship', 'Scholarship from ANTS'),
        ('Sponsor', 'Sponsorship through Sponsor'),
    ]
    finance_method = models.CharField(max_length=20, choices=FINANCE_CHOICES, default='Private')
    sponsor_name = models.CharField(max_length=200, blank=True, verbose_name="Sponsor Name", default="")

    # --- 5. SOURCE & PLANS ---
    SOURCE_CHOICES = [
        ('Website', 'Website'),
        ('Social Media', 'Social Media'),
        ('Brochure', 'Brochure/Prospectus'),
        ('Student', 'Student of ANTS'),
        ('Professor', 'Professor of ANTS'),
        ('Missionary', 'Missionary'),
        ('Pastor', 'Pastor of my church'),
        ('Poster', 'Poster'),
        ('Advertisement', 'Advertisement'),
        ('Other', 'Other'),
    ]
    source_of_info = models.CharField(max_length=50, choices=SOURCE_CHOICES, default='Website')
    # THE MISSING FIELD ADDED HERE:
    source_details = models.CharField(max_length=200, blank=True, default='', verbose_name="Specify Source details")
    
    purpose_of_study = models.TextField(verbose_name="Purpose of studying at ANTS", default='')
    future_plan = models.TextField(verbose_name="Future plan after studying at ANTS", default='')

    # --- 6. ATTACHMENTS CHECKLIST ---
    has_certificates = models.BooleanField(default=False)
    has_transcripts = models.BooleanField(default=False)
    has_recommendation = models.BooleanField(default=False)
    has_testimony = models.BooleanField(default=False)
    
    # --- 7. ACTUAL FILE UPLOADS ---
    passport_photo = models.ImageField(upload_to='applications/photos/', verbose_name="Passport Photo", default='')
    academic_docs_file = models.FileField(upload_to='applications/docs/', verbose_name="Academic Documents (PDF)", default='')
    recommendation_letter = models.FileField(upload_to='applications/docs/', blank=True, null=True, default='')
    testimony_file = models.FileField(upload_to='applications/docs/', blank=True, null=True, verbose_name="Personal Testimony", default='')

    # --- SYSTEM FIELDS ---
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending', choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')])
    official_comment = models.TextField(blank=True, verbose_name="Official Comment (Official Use Only)", default="")

    def __str__(self):
        return f"{self.full_name} - {self.program_choice}"
# --- HELPER MODELS FOR TABULAR DATA ---

class EducationEntry(models.Model):
    """Stores the table: Institute | Period | Certificate/Degree"""
    application = models.ForeignKey(StudentApplication, on_delete=models.CASCADE, related_name='education_entries')
    institute = models.CharField(max_length=255)
    period = models.CharField(max_length=100)
    award = models.CharField(max_length=255, verbose_name="Certificate/Diploma/Degree")

class EmploymentEntry(models.Model):
    """Stores the table: Period | Employer/Company | Post Held"""
    application = models.ForeignKey(StudentApplication, on_delete=models.CASCADE, related_name='employment_entries')
    period = models.CharField(max_length=100)
    employer = models.CharField(max_length=255)
    post_held = models.CharField(max_length=255, verbose_name="Post Held / Main Duties")  