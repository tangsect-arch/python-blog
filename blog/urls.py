from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns
from userapi import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('entries.urls')),
    path('users/', include('users.urls')),
    path('userapi/', views.entryList.as_view()),
    path('images/', views.photoList.as_view()),
    path('userapiList/', include('userapi.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)
