from django import forms
from .models import AlumniMember

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control py-3', 'placeholder': 'Your Full Name'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-3', 'placeholder': 'Your Email Address'
    }))
    subject = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'class': 'form-control py-3', 'placeholder': 'Subject'
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control', 'rows': 5, 'placeholder': 'How can we help you?'
    }))
    
class AlumniRegistrationForm(forms.ModelForm):
    class Meta:
        model = AlumniMember
        # We don't show 'is_approved' here, obviously!
        fields = ['full_name', 'email', 'phone', 'graduation_year', 'program', 'current_job', 'employer', 'photo', 'testimonial']
        
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'graduation_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2020'}),
            'program': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Program Studied'}),
            'current_job': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Current Role'}),
            'employer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Current Organization/Church'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'testimonial': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Share your experience at ANTS...'}),
        }    