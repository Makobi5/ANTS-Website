from django import forms
from django.forms import inlineformset_factory # Keep this import for Formsets later
from django.contrib.auth.models import User # Keep this for StudentSignUpForm
from django.contrib.auth.forms import UserCreationForm # Keep this for StudentSignUpForm

# Import your models
from .models import StudentApplication, StudentProfile, EducationEntry, EmploymentEntry

class ApplicationForm(forms.ModelForm):
    # Define YES_NO_CHOICES once at the class level
    YES_NO_CHOICES = [(True, 'Yes'), (False, 'No')]

    # 1. EXPLICITLY DEFINE THESE BOOLEAN FIELDS WITH TypedChoiceField
    # This ensures they render as RadioSelect and handle boolean conversion correctly
    is_first_study = forms.TypedChoiceField(
        choices=YES_NO_CHOICES,
        coerce=lambda x: x == 'True',  # Converts "True"/"False" strings from HTML to Python booleans
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial=True, # Default to Yes
        required=True,
        label="Is this your first and/or subsequent study?"
    )
    
    english_instruction = forms.TypedChoiceField(
        choices=YES_NO_CHOICES,
        coerce=lambda x: x == 'True',
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial=True, # Default to Yes
        required=True,
        label="Was English the language of instruction?"
    )
    
    class Meta:
        model = StudentApplication
        fields = '__all__'
        # Ensure only unique, non-system fields are excluded here
        exclude = ['submitted_at', 'status', 'applicant', 'official_comment'] 

        widgets = {
            # --- 1. PERSONAL DETAILS ---
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Surname and Given Names'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'marital_status': forms.Select(attrs={'class': 'form-select'}),
            'place_of_birth': forms.TextInput(attrs={'class': 'form-control'}),
            'tribe': forms.TextInput(attrs={'class': 'form-control'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+256...'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'permanent_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            
            # Add these to widgets
            'num_father': forms.NumberInput(attrs={'class': 'form-control small-box', 'min': 0}),
            'num_mother': forms.NumberInput(attrs={'class': 'form-control small-box', 'min': 0}),
            'num_brother': forms.NumberInput(attrs={'class': 'form-control small-box', 'min': 0}),
            'num_sister': forms.NumberInput(attrs={'class': 'form-control small-box', 'min': 0}),
            'num_wife': forms.NumberInput(attrs={'class': 'form-control small-box', 'min': 0}),
            'num_husband': forms.NumberInput(attrs={'class': 'form-control small-box', 'min': 0}),
            'num_son': forms.NumberInput(attrs={'class': 'form-control small-box', 'min': 0}),
            'num_daughter': forms.NumberInput(attrs={'class': 'form-control small-box', 'min': 0}),
            'num_others': forms.NumberInput(attrs={'class': 'form-control small-box', 'min': 0}),
            'family_contact_1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name and Phone'}),
            'family_contact_2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name and Phone'}),

            # --- 2. CHURCH & RELIGIOUS INFO ---
            'attending_church': forms.TextInput(attrs={'class': 'form-control'}),
            'location_of_church': forms.TextInput(attrs={'class': 'form-control'}),
            'church_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Pastor/Elder'}),
            'time_of_baptism': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Month/Year'}),
            'senior_pastor': forms.TextInput(attrs={'class': 'form-control'}),
            'pastor_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'denomination': forms.TextInput(attrs={'class': 'form-control'}),
            'person_known_to_ants': forms.TextInput(attrs={'class': 'form-control'}), # Corrected duplicate name
            
            # 'is_first_study' and 'english_instruction' are defined above, so removed from here

            # --- 3. ACADEMIC PRIZES ---
            'academic_prizes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'List any prizes or distinctions...'}),

            # --- 4. PROGRAM & FINANCE ---
            'program_choice': forms.Select(attrs={'class': 'form-select'}),
            'finance_method': forms.Select(attrs={'class': 'form-select'}),
            'sponsor_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'If applicable'}),

            # --- 5. SOURCE & GOALS ---
            'source_of_info': forms.RadioSelect(attrs={'class': 'form-check-input'}), # Corrected duplicate name
            'source_details': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Specify platform name, student name, or other details...'
            }),
            'purpose_of_study': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                'placeholder': 'e.g. I want to deepen my understanding of the Bible...'}),
            'future_plan': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                    'placeholder': 'e.g. To serve as a youth pastor in my home district...'}),

            # --- 6. ATTACHMENT CHECKLIST ---
            'has_certificates': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_transcripts': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_recommendation': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_testimony': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

            # --- 7. ACTUAL FILE UPLOADS ---
            'passport_photo': forms.FileInput(attrs={'class': 'form-control'}),
            'academic_docs_file': forms.FileInput(attrs={'class': 'form-control'}), # Corrected name
            'recommendation_letter': forms.FileInput(attrs={'class': 'form-control'}),
            'testimony_file': forms.FileInput(attrs={'class': 'form-control'}),
        }

# --- THE TABULAR FORMSETS (For Education and Employment) ---

EducationFormSet = inlineformset_factory(
    StudentApplication, 
    EducationEntry, 
    fields=('institute', 'period', 'award'), 
    extra=2, 
    can_delete=True,
    widgets={
        'institute': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'School Name'}),
        'period': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Year-Year'}),
        'award': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'UCE/Diploma/etc'}),
    }
)

EmploymentFormSet = inlineformset_factory(
    StudentApplication, 
    EmploymentEntry, 
    fields=('period', 'employer', 'post_held'), 
    extra=2,
    can_delete=True,
    widgets={
        'period': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Year-Year'}),
        'employer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company/Church'}),
        'post_held': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title'}),
    }
)

# --- USER SIGNUP FORM ---

class StudentSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True, help_text="Required for Login")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
    
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if StudentProfile.objects.filter(phone_number=phone).exists():
            raise forms.ValidationError("This phone number is already registered.")
        return phone