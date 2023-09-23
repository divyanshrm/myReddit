from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
# Create your views here.
from django.http import Http404
from django.views.generic import *
from django.contrib.auth import get_user_model
from braces.views import SelectRelatedMixin
from django.contrib import messages
from groups import models as ms
from . import models
from . import forms
from django.contrib.auth.decorators import login_required
User=get_user_model()
class PostList(SelectRelatedMixin,ListView):
    model=models.Post
    select_related=('user','group')
    template_name='posts/user/post_list.html'
    def get_queryset(self):
        if self.request.user.is_authenticated:
        # Get groups where the current user is a member
            user_groups = ms.Group.objects.filter(memberships__user=self.request.user)
        # Filter posts to only those from the groups user is part of
            return super().get_queryset().filter(group__in=user_groups)
        else:
            return self.model.objects.none()

class UserPosts(LoginRequiredMixin,ListView):
    login_url='accounts:login'
    model=models.Post
    template_name='posts/user_post_list.html'
    def get_queryset(self) -> QuerySet[Any]:
        try:
            self.post_user=User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context=super().get_context_data(**kwargs)
        context['post_user']=User.objects.get(username__iexact=(self.kwargs.get('username')))
        return context

class PostDetail(SelectRelatedMixin,DetailView):
    model=models.Post
    select_related=('user','group')
    template_name='posts/post_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['comment_form'] = forms.CommentForm()
        return context


class CreatePost(SelectRelatedMixin,LoginRequiredMixin,CreateView):
    fields = ('message', )
    model = models.Post

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        return form
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug'] = self.kwargs.get('slug')
        return context
    def form_valid(self, form):
        slug = self.kwargs.get('slug')
        group = models.Group.objects.get(slug=slug)
        post = form.save(commit=False)
        post.group = group
        post.user=self.request.user
        post.save()
        return super().form_valid(form)

class DeletePost(SelectRelatedMixin,LoginRequiredMixin,DeleteView):
    model=models.Post
    
    select_related=('user','group')
    def get_success_url(self):
        User = get_user_model()
        return reverse_lazy('posts:for_user', kwargs={'username': self.request.user.username})
    def get_queryset(self):
        q= super().get_queryset()
        return q.filter(user_id=self.request.user.id)
    def delete(self,*args, **kwargs):
        messages.success(self.request,'Post Deleted')
        return super().delete(*args, **kwargs)
from . import forms
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

@login_required
def add_comment(request, pk,*args, **kwargs):

    post = get_object_or_404(models.Post, pk=pk)
    
    if request.method == 'POST':
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('posts:single', username=post.user.username,pk=post.pk)
    
from django.http import HttpResponseRedirect
from django.urls import reverse
@login_required
def delete_comment(request, username,postpk,pk):
    comment = get_object_or_404(models.Comment, pk=pk)

    
    post = comment.post
    comment.delete()
    messages.success(request, 'Comment deleted successfully.')
    return redirect('posts:single', username=post.user.username, pk=post.pk)

@login_required
def like_post(request,username, pk):
    post = get_object_or_404(models.Post, pk=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        post.dislikes.remove(request.user)  # Ensure user doesn't dislike if they've liked
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def dislike_post(request,username, pk):
    post = get_object_or_404(models.Post, pk=pk)
    if post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.remove(request.user)
    else:
        post.dislikes.add(request.user)
        post.likes.remove(request.user)  # Ensure user doesn't like if they've disliked
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))