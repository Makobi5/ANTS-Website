from django.shortcuts import render, get_object_or_404
from .models import StaffMember

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