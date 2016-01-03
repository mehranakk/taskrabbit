from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from catalogue.models import MyUser
from django.http import HttpRequest, HttpResponseRedirect



def kasesher(request):
    is_logged_in = False
    if request.user.is_authenticated():
        is_logged_in = True
    return render_to_response('base.html', context={'is_logged_in': is_logged_in})

@login_required
def profile(request, user_id):
    u = get_object_or_404(MyUser, pk=user_id)
    is_profile_owner = False
    is_following = False
    if u.id == request.user.id:
        is_profile_owner = True
    else:
        if request.user.myuser.following.filter(id=u.id).count():
            is_following = True
    return render_to_response("profile.html", {'request': request, 'user': u, 'is_profile_owner': is_profile_owner,
                                               'is_following': is_following, })

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
    #Not Supported yet
    return HttpResponseRedirect('/accounts/login/$')
