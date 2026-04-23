from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@staff_member_required
def edit_my_profile(request):
    user = request.user
    profile = user.profile
    
    if request.method == 'POST':
        # Logic to update first_name, last_name, and theme
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        profile.ui_theme = request.POST.get('ui_theme')
        
        user.save()
        profile.save()
        messages.success(request, "Your profile has been updated!")
        return redirect('admin:index')

    context = {
        'title': 'Edit My Profile',
        'user': user,
        'profile': profile,
    }
    return render(request, 'admin/edit_profile.html', context)