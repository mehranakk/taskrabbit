from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required


# Create your tests here.

def kasesher(request):
    return render_to_response('base.html', context={})

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
