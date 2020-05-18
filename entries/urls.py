from django.conf.urls.static import static
from django.urls import path

from django.conf import settings
from .views import HomeView, EntryView, CreateEntryView, like_view

urlpatterns = [
    path('', HomeView.as_view(), name='home_blog'),
    path('likes/', like_view, name='blogLike'),
    path('entries/<int:pk>/', EntryView.as_view(), name='entry_details'),
    path('create_entry/', CreateEntryView.as_view(success_url="/"), name='create_entry'),
]
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
