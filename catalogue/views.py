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
    context = {
        'user': MyUser.objects.get(user=request.user),
    }
    return render_to_response("profile.html", context)

@login_required
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=request.user.myuser)
    else:
        form = EditProfileForm(instance=request.user.myuser)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/accounts/profile/%d' % request.user.id)
    return render_to_response('edit_profile.html', {'request': request, 'form':form})

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
