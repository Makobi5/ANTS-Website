from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

urlpatterns =[
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('staff/', include('staff.urls')),
    path('programs/', include('academics.urls')),
    path('admissions/', include('admissions.urls')),
    path('news/', include('news.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    
    # THE BULLETPROOF IMAGE/CSS ROUTING FOR DIRECTADMIN
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

handler404 = 'core.views.error_404'
handler500 = 'core.views.error_500'