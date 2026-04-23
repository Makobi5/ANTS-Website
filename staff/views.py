from django.shortcuts import render, get_object_or_404
from .models import StaffMember
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def edit_profile(request):
    user = request.user
    profile = user.profile  # Assumes UserProfile model from previous step
    
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        profile.ui_theme = request.POST.get('ui_theme')
        
        user.save()
        profile.save()
        messages.success(request, "Success! Your profile and theme preferences have been updated.")
        return redirect('edit_profile')

    return render(request, 'admin/edit_profile.html', {'profile_user': user})

def staff_list(request):
    principal = StaffMember.objects.filter(category='PRINCIPAL').first()
    management = StaffMember.objects.filter(category='MANAGEMENT')
    office = StaffMember.objects.filter(category='OFFICE')
    academic = StaffMember.objects.filter(category='ACADEMIC')
    support = StaffMember.objects.filter(category='SUPPORT')

    context = {
        'page_title': 'Staff Directory',  # <--- ADD THIS LINE
        'principal': principal,
        'management': management,
        'office': office,
        'academic': academic,
        'support': support,
    }
    return render(request, 'staff/staff_list.html', context)

def staff_detail(request, slug):
    # Fetch the staff member by their unique URL slug
    staff = get_object_or_404(StaffMember, slug=slug)
    return render(request, 'staff/staff_detail.html', {'staff': staff})

# ... existing imports ...

# 1. View for "The Principal" Link
def principal_profile(request):
    # Find the person marked as PRINCIPAL
    # We use 'first()' just in case there are accidental duplicates, we pick one.
    principal = StaffMember.objects.filter(category='PRINCIPAL').first()
    
    # If no principal exists yet, handle gracefully (optional, but good practice)
    if not principal:
        return render(request, 'core/home.html') # Or a 404 page

    # Re-use the Detail template we made earlier
    return render(request, 'staff/staff_detail.html', {'staff': principal})

# 2. View for "Management" Link
def management_list(request):
    principal = StaffMember.objects.filter(category='PRINCIPAL').first()
    management = StaffMember.objects.filter(category='MANAGEMENT')
    
    context = {
        'page_title': 'ANTS Management',  # <--- ADD THIS LINE (Custom Title)
        'principal': principal,
        'management': management,
        'office': [],
        'academic': [],
        'support': [],
    }
    return render(request, 'staff/staff_list.html', context)