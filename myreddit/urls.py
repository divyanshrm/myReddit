"""myreddit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import re_path
from accounts import views
from django.urls import include
from django.conf.urls.static import static


app_name='myreddit'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_page, name='home'),
    re_path('^accounts/',include('accounts.urls',namespace='accounts')),
    re_path('^accounts/',include('django.contrib.auth.urls')),
    re_path('^test/$',views.TestPage.as_view(),name='test'),
    re_path('^thanks/$',views.ThanksPage.as_view(),name='thanks'),
    re_path("^posts/", include("posts.urls", namespace="posts")),
    re_path("^groups/",include("groups.urls", namespace="groups"))
]
