"""taskrabbit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin, auth
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', 'catalogue.views.kasesher', name='kaseshare'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/profile/(?P<user_id>[0-9]+)$', 'catalogue.views.profile'),
    url(r'^accounts/edit/$', 'catalogue.views.edit_profile'),
    url(r'^accounts/signup/$', 'catalogue.views.signup'),

]
