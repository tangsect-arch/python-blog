from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from .models import Entries, Likes, PostImages
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(LoginRequiredMixin, ListView):
    model = Entries
    template_name = 'entries/index.html'
    context_object_name = 'blog_entries'
    ordering = ['-entry_date']
    paginate_by = 3


class EntryView(LoginRequiredMixin, DetailView):
    model= Entries
    template_name = 'entries/entry_details.html'


class CreateEntryView(LoginRequiredMixin, CreateView):
    model = Entries
    template_name = 'entries/create_entry.html'
    fields = ['entry_title', 'entry_text', 'liked']

    def form_valid(self, form):
        form.instance.entry_author = self.request.user
        return super().form_valid(form)




def like_view(request):
    user = request.user
    postId = request.POST.get('postId')
    postObj = Entries.objects.get(id=postId)
    if user in postObj.liked.all():
        postObj.liked.remove(user)

    else:
        postObj.liked.add(user)

    like, created = Likes.objects.get_or_create(user=user, entries_id=postId)
    if not created:
        if like.value == 'Like':
            like.value = 'Unlike'
        else:
            like.value = 'Like'

    like.save()

    return redirect('home_blog')
