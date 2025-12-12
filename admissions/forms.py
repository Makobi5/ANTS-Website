from django import forms
from .models import StudentApplication
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import StudentApplication, StudentProfile

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = StudentApplication
        fields = '__all__'
        exclude = ['submitted_at', 'status']

        widgets = {
            # Personal
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Surname and Given Names'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'marital_status': forms.Select(attrs={'class': 'form-select'}),
            'place_of_birth': forms.TextInput(attrs={'class': 'form-control'}),
            'tribe': forms.TextInput(attrs={'class': 'form-control'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+256...'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'permanent_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            
            # Next of Kin
            'next_of_kin_name': forms.TextInput(attrs={'class': 'form-control'}),
            'next_of_kin_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'next_of_kin_relationship': forms.TextInput(attrs={'class': 'form-control'}),

            # Church
            'attending_church': forms.TextInput(attrs={'class': 'form-control'}),
            'church_location': forms.TextInput(attrs={'class': 'form-control'}),
            'church_title': forms.TextInput(attrs={'class': 'form-control'}),
            'baptism_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 1998'}),
            'senior_pastor': forms.TextInput(attrs={'class': 'form-control'}),
            'pastor_contact': forms.TextInput(attrs={'class': 'form-control'}),

            # Education
            'education_history': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Example:\n- Makerere College, 2018-2020, UACE\n- Mengo SS, 2014-2017, UCE'}),

            # Program
            'program_choice': forms.Select(attrs={'class': 'form-select'}),
            'finance_method': forms.Select(attrs={'class': 'form-select'}),
            'sponsor_name': forms.TextInput(attrs={'class': 'form-control'}),

            # Uploads
            'passport_photo': forms.FileInput(attrs={'class': 'form-control'}),
            'academic_documents': forms.FileInput(attrs={'class': 'form-control'}),
            'recommendation_letter': forms.FileInput(attrs={'class': 'form-control'}),
        }
        
class StudentSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    # Add Phone Number Field
    phone_number = forms.CharField(required=True, help_text="Required for Login")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
    
    # We will handle saving the phone number in the View   
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        
        # Check if this number already exists in the database
        if StudentProfile.objects.filter(phone_number=phone).exists():
            raise forms.ValidationError("This phone number is already registered. Please use a different one or login.")
        
        return phone    