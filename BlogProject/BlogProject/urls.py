"""BlogProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from BlogApp import views
from django.contrib.auth import views as auth_views
from BlogApp.forms import LoginForm
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index_view),
    url(r'^home/', views.post_list_view),
    url(r'^politics/', views.post_list_view),
    url(r'^films/', views.post_list_view),
    url(r'^technology/', views.post_list_view),
    url(r'^business/', views.post_list_view),
    url(r'^sports/', views.post_list_view),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.post_list_view,name='post_list_by_tag_slug'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post>[-\w]+)/$',
     views.post_detail_view,name='post_detail'),
    url(r'^(?P<id>\d+)/share/$',views.sent_email_form_view),
    url(r'^indexsignup/', views.index_view),
    url(r'^signup/', views.signup_view),
    url(r'^login/$', views.login_view,name='login'),
    url(r'^accounts/',include('django.contrib.auth.urls')),
    url(r'^logout/', views.logout_view),
    url(r'^post/', views.post_view),
    url(r'^userposts/$', views.post_list_view,name='userposts'),
    url(r'^(?P<id>\d+)/removepost/$', views.post_object_view),
    url(r'^(?P<id>\d+)/updatepost/$', views.post_view),
    url(r'^(?P<id>\d+)/remove/$', views.post_delete_view),

]
