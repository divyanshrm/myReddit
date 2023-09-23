from django.db import models
from django.utils.text import slugify
from django.urls import reverse
# Create your models here.
import misaka
from django.contrib.auth import get_user_model
User=get_user_model()

from django import template

register=template.Library()

class Group(models.Model):
    name=models.CharField(max_length=512,unique=True)
    slug=models.SlugField(allow_unicode=True,unique=True)
    description=models.TextField(max_length=5000,blank=True,default='')
    description_html=models.TextField(max_length=5000,editable=False,default='',blank=True)
    members=models.ManyToManyField(User,through='GroupMember')

    def __str__(self):
        return self.name or ""
    
    def save(self,*args, **kwargs):
        self.slug=slugify(self.name)
        self.description_html=misaka.html(self.description)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("groups:single", kwargs={"slug": self.slug})
    
    class Meta:
        ordering=['name']
    
    pass

class GroupMember(models.Model):
    group=models.ForeignKey(Group,on_delete=models.CASCADE,related_name='memberships')
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_groups')
    def __str__(self):
        return self.user.username or ""

    class Meta:
        unique_together=('group','user')

    pass