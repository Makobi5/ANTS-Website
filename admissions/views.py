from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ApplicationForm, StudentSignUpForm
from .models import StudentApplication
from .models import StudentApplication, StudentProfile # <--- Import Profile
from django.shortcuts import render, redirect, get_object_or_404 # <--- Add get_object_or_404

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

# 5. The Application Form (Now Protected)
@login_required(login_url='student_login')
def apply_now(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.applicant = request.user
            application.save()
            messages.success(request, "Application submitted successfully!")
            return redirect('student_dashboard')
    else:
        # Pre-fill data
        initial_data = {
            'full_name': f"{request.user.first_name} {request.user.last_name}",
            'email': request.user.email,
            
            # NEW: Check if the URL has a course_id (e.g. ?course_id=5)
            # If yes, select that program automatically!
            'program_choice': request.GET.get('course_id')
        }
        form = ApplicationForm(initial=initial_data)

    return render(request, 'admissions/apply.html', {'form': form})

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