from .models import PopupBanner


def user_theme(request):
    if request.user.is_authenticated:
        try:
            return {'current_theme': request.user.profile.ui_theme}
        except:
            return {'current_theme': 'default'}
    return {'current_theme': 'default'}


def popup_banner(request):
    """Makes the active PopupBanner available on every page via {{ popup_banner }}"""
    popup = PopupBanner.objects.filter(is_active=True).first()
    return {'popup_banner': popup}