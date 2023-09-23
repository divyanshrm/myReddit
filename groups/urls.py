
from . import views
from django.urls import re_path,path
app_name='groups'

urlpatterns = [
    re_path(r'^$',views.ListGroups.as_view(),name='all'),
    re_path('^new/$',views.CreateGroup.as_view(),name='create'),
    re_path('^posts/in/(?P<slug>[-\w]+)/$',views.SingleGroup.as_view(),name='single'),
    re_path(r"join/(?P<slug>[-\w]+)/$",views.JoinGroup.as_view(),name="join"),
    re_path(r"leave/(?P<slug>[-\w]+)/$",views.LeaveGroup.as_view(),name="leave"),

]
