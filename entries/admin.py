from django.contrib import admin
from .models import Entries, Likes, PostImages


class PhotoInline(admin.StackedInline):
    model = PostImages
    extra = 1


class MultiImages(admin.ModelAdmin):
    inlines = [PhotoInline]

    def save_model(self, request, obj, form, change):
        obj.save()

        for afile in request.FILES.getlist('photos_multiple'):
            obj.photos.create(image=afile)


admin.site.register(Entries, MultiImages)
# admin.site.register(Likes)
#admin.site.register(PostImages)

# Register your models here.
