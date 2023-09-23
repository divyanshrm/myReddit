from django.db import models
from django.conf import settings
import misaka
# Create your models here.
from django.urls import reverse

from groups.models import Group

from django.contrib.auth import get_user_model


User=get_user_model()

class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts')
    created_at=models.DateTimeField(auto_now=True)
    message=models.TextField(max_length=5000)
    message_html=models.TextField(editable=False)
    group=models.ForeignKey(Group,on_delete=models.CASCADE,related_name='posts',null=False,blank=False)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_posts', blank=True)

    @property
    def total_likes(self):
        return self.likes.count()

    @property
    def total_dislikes(self):
        return self.dislikes.count()

    def __str__(self):
        return self.message
    def save(self,*args, **kwargs):
        self.message_html=misaka.html(self.message)
        super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse("posts:single", kwargs={"username": self.user.username,"pk":self.pk})
    class Meta:
        ordering=['-created_at']
        unique_together=['user','message']

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.content

