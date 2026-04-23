def user_theme(request):
    if request.user.is_authenticated:
        try:
            return {'current_theme': request.user.profile.ui_theme}
        except:
            return {'current_theme': 'default'}
    return {'current_theme': 'default'}