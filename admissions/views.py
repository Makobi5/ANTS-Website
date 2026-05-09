from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ApplicationForm, StudentSignUpForm
from .models import StudentApplication
from .forms import ApplicationForm, EmploymentFormSet, EducationFormSet
from .models import StudentApplication, StudentProfile # <--- Import Profile
from django.shortcuts import render, redirect, get_object_or_404 # <--- Add get_object_or_404
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
import os
from django.conf import settings
# This helper function finds the absolute path for images
def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access
    those resources on the local disk.
    """
    static_url = settings.STATIC_URL      # e.g. /static/
    static_root = settings.STATIC_ROOT    # folder on disk
    media_url = settings.MEDIA_URL        # e.g. /media/
    media_root = settings.MEDIA_ROOT      # folder on disk

    # 1. Handle Media Files (Passport Photos, etc.)
    if uri.startswith(media_url):
        path = os.path.join(media_root, uri.replace(media_url, ""))
        
    # 2. Handle Static Files (Logo, Header, Footer)
    elif uri.startswith(static_url):
        # We try to find the file in static folders
        from django.contrib.staticfiles import finders
        path = finders.find(uri.replace(static_url, ""))
        if not path:
            # Fallback for production
            path = os.path.join(static_root, uri.replace(static_url, ""))
            
    else:
        # If it's already an absolute path or external URL, return as is
        return uri

    # Make sure the file exists
    if not os.path.isfile(path):
        # We return uri as fallback instead of crashing
        return uri
        
    return path

def download_application_pdf(request, application_id):
    application = get_object_or_404(StudentApplication, id=application_id)
    template_path = 'admissions/application_pdf.html'
    context = {
        'application': application,
        }
    
    response = HttpResponse(content_type='application/pdf')
    filename = f"Application_{application.full_name.replace(' ', '_')}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    template = get_template(template_path)
    html = template.render(context)

    # ADD THE link_callback HERE
    pisa_status = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback
    )
    
    if pisa_status.err:
       return HttpResponse('Error generating PDF')
    return response

# 1. Sign Up View (Updated to save Phone)
def student_signup(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            # Save the User
            user = form.save()
            
            # Save the Phone Number to the Profile
            phone = form.cleaned_data.get('phone_number')
            StudentProfile.objects.create(user=user, phone_number=phone)
            
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('student_dashboard')
    else:
        form = StudentSignUpForm()
    return render(request, 'admissions/signup.html', {'form': form})

# 2. Login View (Updated to check Phone OR Username)
def student_login(request):
    if request.method == 'POST':
        # Get what the user typed
        username_or_phone = request.POST.get('username')
        password = request.POST.get('password')
        
        user = None
        
        # A. Try to find user by Phone Number first
        try:
            profile = StudentProfile.objects.get(phone_number=username_or_phone)
            user = authenticate(request, username=profile.user.username, password=password)
        except StudentProfile.DoesNotExist:
            # B. If not a phone number, try standard Username/Email login
            user = authenticate(request, username=username_or_phone, password=password)

        if user is not None:
            login(request, user)
            return redirect('student_dashboard')
        else:
            messages.error(request, "Invalid credentials. Please check your Phone/Username and Password.")
            form = AuthenticationForm() # Return empty form
    else:
        form = AuthenticationForm()
        
    return render(request, 'admissions/login.html', {'form': form})

# 3. Logout View
def student_logout(request):
    logout(request)
    return redirect('student_login')

# 4. Student Dashboard (The "Portal" Home)
@login_required(login_url='student_login')
def student_dashboard(request):
    # Get any applications this student has already made
    my_apps = StudentApplication.objects.filter(applicant=request.user)
    return render(request, 'admissions/dashboard.html', {'my_apps': my_apps})

# Update only the apply_now function in admissions/views.py

@login_required(login_url='student_login')
def apply_now(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        education_formset = EducationFormSet(request.POST)
        employment_formset = EmploymentFormSet(request.POST)

        if form.is_valid() and education_formset.is_valid() and employment_formset.is_valid():
            application = form.save(commit=False)
            application.applicant = request.user
            application.save()
            
            # Connect and save the tables
            education_formset.instance = application
            education_formset.save()
            
            employment_formset.instance = application
            employment_formset.save()
            
            messages.success(request, "Application submitted successfully!")
            return redirect('student_dashboard')
    else:
        form = ApplicationForm()
        education_formset = EducationFormSet()
        employment_formset = EmploymentFormSet()

    return render(request, 'admissions/apply.html', {
        'form': form,
        'education_formset': education_formset,
        'employment_formset': employment_formset
    })

@login_required(login_url='student_login')
def view_application(request, pk):
    # Fetch the application by Primary Key (ID), ensuring it belongs to the current user
    application = get_object_or_404(StudentApplication, pk=pk, applicant=request.user)
    
    return render(request, 'admissions/view_application.html', {'app': application})


def admission_requirements(request):
    return render(request, 'admissions/info_requirements.html')

def admission_procedure(request):
    return render(request, 'admissions/info_procedure.html')

def graduation_requirements(request):
    return render(request, 'admissions/info_graduation.html')

def admission_lists(request):
    # This can be a placeholder for now
    return render(request, 'admissions/info_lists.html')

def why_study(request):
    return render(request, 'admissions/why_study.html')