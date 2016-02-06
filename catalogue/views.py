from datetime import datetime

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseForbidden
from django.template import RequestContext
from django.db.models import Count, Avg, Q
from django.contrib.sessions.models import Session
from django.middleware.csrf import get_token

from catalogue.models import *
from catalogue.forms import *


def home(request):
    top_search_queries = SearchQuery.objects.values('text').annotate(Count('text')).order_by('-text__count')[:5]
    most_posted_employers = MyUser.objects.annotate(Count('task_employer')).filter(task_employer__count__gt=0).order_by('-task_employer__count')[:5]
    employees = MyUser.objects.annotate(Count('task_employee')).filter(task_employee__count__gt=0)
    best_employees = employees.annotate(Avg('comment_employee__rate')).order_by('-comment_employee__rate__avg')[:5]
    context = {
        'top_search_queries': top_search_queries,
        'most_posted_employers': most_posted_employers,
        'best_employees': best_employees,
        'total_home_visits': Session.objects.count(),
    }
    return render_to_response("home.html", context, context_instance=RequestContext(request))


def browse(request, category='all'):
    if request.method == 'GET':
        if category == 'all':
            tasks = Task.objects.all()
        else:
            tasks = Task.objects.filter(category__slug=category)
        context = {
            'tasks': tasks.order_by('-upload_date'),
            'user': MyUser.objects.get(user=request.user) if isinstance(request.user, User) else None,
            'categories': Category.objects.all(),
            'selected_category': Category.objects.get(slug=category),
        }
        return render_to_response("browse.html", context, context_instance=RequestContext(request))
    else:
        return HttpResponseNotAllowed(['GET'])


def search(request):
    if request.method == 'GET':
        if 'query' in request.GET:
            query = request.GET['query']
            if query:  # avoid saving empty queries
                SearchQuery.objects.create(text=query)
            query_words = query.lower().split()
            tasks = Task.objects.all()
            for word in query_words:
                tasks = tasks.filter(Q(title__icontains=word) | Q(text__icontains=word) | Q(category__name__icontains=word) | Q(location__icontains=word))
            context = {
                'tasks': tasks.order_by('-upload_date'),
                'query': query,
                'user': MyUser.objects.get(user=request.user) if isinstance(request.user, User) else None,
            }
            return render_to_response("search_results.html", context, context_instance=RequestContext(request))
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseNotAllowed(['GET'])


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
    return render_to_response("profile.html", context, context_instance=RequestContext(request))


@login_required
def edit(request):
    user = MyUser.objects.get(user=request.user)
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/profile/')
    form = EditProfileForm(instance=user)
    context = {
        'user': user,
        'form': form,
        'error': '',
        'skills': Skill.objects.all(),
        'user_skills': user.skills.get_queryset(),
    }
    return render_to_response('edit_profile.html', context, context_instance=RequestContext(request))


def signup(request):
    if request.method == "POST":
        form = NewProfileForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user_if_any = MyUser.objects.filter(user__username=username)
            if len(user_if_any) > 0:
                return render_to_response('registration/signup.html', {'form': form, 'error':'User Already Exists'}, context_instance=RequestContext(request))

            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            display_name = form.cleaned_data['display_name']
            user = User.objects.create_user(username, email, password)
            user.save()
            myUser = MyUser.objects.create(user=user, display_name=display_name)
            myUser.save()
            return HttpResponseRedirect('/')

    form = NewProfileForm()
    return render_to_response('registration/signup.html', {'form': form, 'error':''}, context_instance=RequestContext(request))


@login_required
def history(request):
    user = MyUser.objects.get(user=request.user)
    tasks_as_employee = Task.objects.filter(employee__user=request.user)
    tasks_as_employer = Task.objects.filter(employer__user=request.user)
    requested_tasks = TaskRequest.objects.filter(employee__user=request.user)
    context = {
        'user': user,
        'tasks_as_employee': tasks_as_employee,
        'tasks_as_employer': tasks_as_employer,
        'requested_tasks': requested_tasks,
    }
    return render_to_response('history.html', context, context_instance=RequestContext(request))


@login_required
def comments(request):
    user = MyUser.objects.get(user=request.user)
    context = {
        'user': user,
        'your_comments': Comment.objects.filter(employer=user),
        'comments_about_you': Comment.objects.filter(employee=user),
    }
    return render_to_response('comments.html', context, context_instance=RequestContext(request))


@login_required
def delete_user(request):
    if request.method == 'POST':
        if 'user_id' in request.POST:
            admin_user = MyUser.objects.get(user=request.user)
            try:
                deleted_user = MyUser.objects.get(id=request.POST['user_id'])
                if admin_user.is_admin:
                    if not deleted_user.is_admin:
                        deleted_user.delete()
                        return HttpResponseRedirect('/accounts/manage_users/')
                    else:
                        return HttpResponseForbidden()
                else:
                    return HttpResponseForbidden()
            except ObjectDoesNotExist:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseNotAllowed(['POST'])


@login_required
def manage_users(request):
    user = MyUser.objects.get(user=request.user)
    if user.is_admin:
        context = {
            'user': user,
            'users': MyUser.objects.all(),
            'csrf_token': get_token(request),
        }
        return render_to_response('manage_users.html', context, context_instance=RequestContext(request))
    else:
        return HttpResponseForbidden()


@login_required
def manage_task_requests(request):
    user = MyUser.objects.get(user=request.user)
    tasks = Task.objects.filter(employer=user, status='N')
    task_requests = {}
    if tasks:
        for t in tasks:
            task_requests[t] = TaskRequest.objects.filter(task=t)
    context = {
        'user': user,
        'task_requests': task_requests,
    }
    return render_to_response('manage_task_requests.html', context, context_instance=RequestContext(request))


@login_required
def accept_request(request, task_request_id):
    user = MyUser.objects.get(user=request.user)
    task_request = TaskRequest.objects.get(id=task_request_id)
    task = task_request.task
    task.employee = task_request.employee
    task.status = 'A'
    task.save()
    return HttpResponseRedirect('/accounts/profile')


@login_required
def done_task(request, task_id):
    user = MyUser.objects.get(user=request.user)
    task = Task.objects.get(id=task_id)
    task.status = 'D'
    task.save()
    return HttpResponseRedirect('/comment_employee/%d' % task.employee.id)


@login_required
def comment_employee(request, employee_id):
    employer = MyUser.objects.get(user=request.user)
    employee = MyUser.objects.get(id=employee_id)
    tasks = Task.objects.filter(employer=employer, employee=employee, status='D')
    if not tasks:
        return HttpResponseNotAllowed()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.employer = employer
            comment.employee = employee
            comment.save()

        return HttpResponseRedirect('/accounts/profile')
    form = CommentForm()
    return render_to_response('comment_employee.html', {'form': form, 'employee':employee}, context_instance=RequestContext(request))


@login_required
def payment(request, task_request_id):
    employer = MyUser.objects.get(user=request.user)
    task_request = TaskRequest.objects.get(id=task_request_id)
    task = task_request.task
    return render_to_response('payment.html', {'employee': task_request.employee, 'price': task.price, 'task_request':task_request}, context_instance=RequestContext(request))


@login_required
def new_task(request):
    employer = MyUser.objects.get(user=request.user)
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            category = form.cleaned_data['category']
            price = form.cleaned_data['price']
            task = Task.objects.create(employer=employer, title=title, price=price, text=text, upload_date=datetime.now(), category=category, status='N')
            task.save()

        return HttpResponseRedirect('/')
    form = NewTaskForm()
    categories = Category.objects.all()
    return render_to_response('new_task.html', {'form': form, 'categories': categories}, context_instance=RequestContext(request))
