from django.db import models
#from django.contrib.auth.models import User
from account.models import Account


# Create your models here.
class Entries(models.Model):
    entry_title = models.CharField(max_length=50)
    entry_text = models.TextField()
    liked = models.ManyToManyField(Account, blank=True, default=None, related_name='liked')
    entry_date = models.DateTimeField(auto_now_add=True)
    entry_author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='entry_author')
    entry_images = models.ImageField(null=True, blank=True)
    entry_tag = models.CharField(max_length=50)


    class Meta:
        verbose_name_plural = 'Entry List'

    def __str__(self):
        return f'{self.entry_title}'

    @property
    def num_likes(self):
        return self.liked.all().count()


LIKE_CHOICES = {
    ('Likes', 'Like'),
    ('Unlike', 'Unlike')
}


class Likes(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    entries = models.ForeignKey(Entries, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=10)

    def __str__(self):
        return str(self.entries.entry_title)


class PostImages(models.Model):
    entries = models.ForeignKey(Entries, on_delete=models.CASCADE)
    images = models.ImageField()

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = 'Images'
