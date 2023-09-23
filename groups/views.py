from typing import Any
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
# Create your views here.
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views import generic
from . models import Group,GroupMember
from django.contrib import messages
from django.db.models import Q

class CreateGroup(LoginRequiredMixin,generic.CreateView):
    fields=('name','description')
    model=Group

class SingleGroup(generic.DetailView):
    model=Group
    template_name='groups/group_detail.html'
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # Add the member count to the context
        context['group_member_count'] = self.object.members.count()

        return context

class ListGroups(generic.ListView):
    model=Group
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Get the 'q' parameter from the URL (e.g., /your-url/?q=search_term)
        query = self.request.GET.get('q')
        
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query)  # Assuming you're searching by 'name', modify the field as needed
            )
        return queryset

class JoinGroup(LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self, *args: Any, **kwargs: Any):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})
    def get(self,request,*args, **kwargs):
        group=get_object_or_404(Group,slug=self.kwargs.get('slug'))
        try:
            GroupMember.objects.create(user=self.request.user,group=group)
        except:
            messages.warning(self.request,'Warning Already a Member')
        else:
            messages.success(self.request,'You are Now a Member')
        return super().get(request,*args, **kwargs)

class LeaveGroup(LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self, *args: Any, **kwargs: Any):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})
    def get(self,request,*args, **kwargs):
        try:
            membership=GroupMember.objects.filter(user=self.request.user,group__slug=self.kwargs.get('slug'))
        except GroupMember.DoesNotExist:
            messages.warning(self.request,'Sorry you are not in this group!')
        else:
            membership.delete()
            messages.success(self.request,'You have left the Group')
        return super().get(request, *args, **kwargs)

