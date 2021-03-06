from django.conf.urls import include, url
from django.contrib import admin
from catalogue.views import home, take_task, new_task, profile, history, comments, edit, signup, search, browse, manage_task_requests, accept_request, done_task, comment_employee, payment, employee_profile, employee_comments, employee_history, manage_users, delete_user

urlpatterns = [
    url(r'^category/(?P<category>[A-Za-z0-9_\-]+)/$', browse, name='browse'),
    url(r'^$', home, name='default_home'),
    url(r'^take_task/(?P<task_id>[0-9]+)/$', take_task, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/password_reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    url(r'^accounts/password_reset_done/$', 'django.contrib.auth.views.password_reset', name='password_reset_done'),
    url(r'^new_task/$', new_task),
    url(r'^accept_request/(?P<task_request_id>[0-9]+)/$', accept_request),
    url(r'^done_task/(?P<task_id>[0-9]+)/$', done_task),
    url(r'^payment/(?P<task_request_id>[0-9]+)/$', payment),
    url(r'^comment_employee/(?P<employee_id>[0-9]+)/$', comment_employee),
    url(r'^accounts/profile/$', profile),
    url(r'^profile/(?P<employee_id>[0-9]+)/$', employee_profile),
    url(r'^comments/(?P<employee_id>[0-9]+)/$', employee_comments),
    url(r'^history/(?P<employee_id>[0-9]+)/$', employee_history),
    url(r'^accounts/history/$', history),
    url(r'^accounts/comments/$', comments),
    url(r'^accounts/manage_task_requests/$', manage_task_requests),
    url(r'^accounts/manage_users/$', manage_users),
    url(r'^accounts/edit/$', edit),
    url(r'^accounts/signup/$', signup),
    url(r'^search/$', search),
    url(r'^delete_user/$', delete_user),
]
