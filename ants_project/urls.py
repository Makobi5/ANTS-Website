from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
from academics import views
from staff.views import edit_profile
from news import views as news_views

urlpatterns =[
    path('admin/profile/', edit_profile, name='edit_profile'),
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('staff/', include('staff.urls')),
    path('programs/', include('academics.urls')),
    path('admissions/', include('admissions.urls')),
    path('news/', include('news.urls')),
    path('gallery/', news_views.gallery, name='gallery'),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    
    # THE BULLETPROOF IMAGE/CSS ROUTING FOR DIRECTADMIN
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

handler404 = 'core.views.error_404'
handler500 = 'core.views.error_500'