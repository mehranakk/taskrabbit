from django.conf.urls import include, url
from django.contrib import admin
from catalogue.views import home, take_task, new_task, profile, history, comments, edit, signup, search

urlpatterns = [
    url(r'^category/(?P<category>[A-Za-z0-9_]+)/$', home, name='home'),
    url(r'^$', home, name='default_home'),
    url(r'^take_task/(?P<task_id>[0-9]+)/$', take_task, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/password_reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    url(r'^accounts/password_reset_done/$', 'django.contrib.auth.views.password_reset', name='password_reset_done'),
    url(r'^new_task/$', new_task),
    url(r'^accounts/profile/$', profile),
    url(r'^accounts/history/$', history),
    url(r'^accounts/comments/$', comments),
    url(r'^accounts/edit/$', edit),
    url(r'^accounts/signup/$', signup),
    url(r'^search/$', search),
]
