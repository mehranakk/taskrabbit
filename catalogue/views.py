from datetime import datetime

from django.http.response import HttpResponseNotFound, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseRedirect
from django.contrib.auth.models import User
from django.template import RequestContext, Context


from catalogue.models import *
from catalogue.forms import *


def home(request, category='all'):
    if category == 'all':
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(category__slug=category)
    context = {'request': request, 'tasks': tasks, 'categories':Category.objects.all(), 'selected_category':category}
    return render_to_response("tasks.html", context)


@login_required
def take_task(request, task_id):
    employee = MyUser.objects.get(user=request.user)
    tasks = TaskRequest.objects.filter(employee=employee, task=task_id)
    if tasks.count() != 0:
        return render_to_response('error.html', {'error': 'You have failed this city'})
    newTaskRequest = TaskRequest.objects.create(employee=employee, task=Task.objects.get(id=task_id))
    newTaskRequest.save()
    return HttpResponseRedirect('/')


@login_required
def profile(request):
    user = MyUser.objects.get(user=request.user)
    context = {
        'user': user,
        'skills': user.skills.all(),
    }
    return render_to_response("profile.html", context)

@login_required
def edit(request):
    user = MyUser.objects.get(user=request.user)
    context = {
        'user': user,
        'skills': user.skills.all(),
    }
    return render_to_response('edit.html', context)

@login_required
def signup(request):
    if request.method == "POST":
        form = NewProfileForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            display_name = form.cleaned_data['display_name']
            user = User.objects.create_user(username, email, password)
            user.save()
            myUser = MyUser.objects.create(user=user, display_name=display_name)
            myUser.save()
            return HttpResponseRedirect('/all/')

    form = NewProfileForm()
    return render_to_response('registration/signup.html', {'form': form}, context_instance=RequestContext(request))


@login_required
def history(request):
    tasks_as_employee = Task.objects.filter(employee__user=request.user)
    tasks_as_employer = Task.objects.filter(employer__user=request.user)
    requested_tasks = TaskRequest.objects.filter(employee__user=request.user)
    return render_to_response('history.html', {'tasks_as_employee': tasks_as_employee, 'tasks_as_employer':tasks_as_employer,
            'requested_tasks': requested_tasks})


@login_required
def comments(request):
    user = MyUser.objects.get(user=request.user)
    context = {
        'your_comments': Comment.objects.filter(employer=user),
        'comments_about_you': Comment.objects.filter(employee=user),
    }
    return render_to_response('comments.html', context)


@login_required
def new_task(request):
    employer = MyUser.objects.get(user=request.user)
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            category = form.cleaned_data['category']
            task = Task.objects.create(employer=employer, title=title, text=text, upload_date=datetime.now(),
                    category=category, status='N')
            task.save()

        return HttpResponseRedirect('/')
    form = NewTaskForm()
    return render_to_response('new_task.html', {'form': form}, context_instance=RequestContext(request))
