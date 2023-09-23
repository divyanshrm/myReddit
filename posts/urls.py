from django.urls import re_path
from . import views

app_name='posts'

urlpatterns = [
    re_path('^$',views.PostList.as_view(),name='all'),
    re_path('^new/(?P<slug>[-\w]+)/$',views.CreatePost.as_view(),name='create'),
    re_path('^by/(?P<username>[-\w]+)/$',views.UserPosts.as_view(),name='for_user'),
    re_path('^by/(?P<username>[-\w]+)/(?P<pk>\d+)/$',views.PostDetail.as_view(),name='single'),
    re_path('delete/(?P<pk>\d+)/$',views.DeletePost.as_view(),name='delete'),
    re_path('^by/(?P<username>[-\w]+)/(?P<pk>\d+)/add_comment/$', views.add_comment, name='add_comment'),
    re_path('^by/(?P<username>[-\w]+)/(?P<postpk>\d+)/delete_comment/(?P<pk>\d+)/$', views.delete_comment, name='comment_delete'),
    re_path('^by/(?P<username>[-\w]+)/(?P<pk>\d+)/like/$', views.like_post, name='like_post'),
    re_path('^by/(?P<username>[-\w]+)/(?P<pk>\d+)/dislike/$', views.dislike_post, name='dislike_post'),

    

]
