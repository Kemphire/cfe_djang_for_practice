from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def profile_view(request, *args, **kwargs):
    passed_username = kwargs.get("username", None)
    user = request.user
    print('user.has_perm("auth.add_user")', user.has_perm("auth.add_user"))
    profile_user_obj = get_object_or_404(User, username=passed_username)
    return HttpResponse("Hello {}".format(profile_user_obj.username))


@login_required
def profile_list_view(request):
    context = {
        "obj_list": User.objects.filter(is_active=True),
    }
    return render(request, "profiles/list.html", context)


@login_required
def profile_detail_view(request, username=None, *args, **kwargs):
    user = request.user
    print(
        user.username,
        user.has_perm("subscriptions.basic"),
        user.has_perm("subscriptions.pro"),
        user.has_perm("subscriptions.advanced"),
    )
    # user_groups = user.groups.all()
    # if user_groups.filter(name__icontains="basic").exists():
    #     return HttpResponse(
    #         f"Congrats you are from {user_groups.filter(name__icontains='basic').first().name}"
    #     )
    profile_user_obj = get_object_or_404(User, username=username)
    is_me = user == profile_user_obj
    context = {
        "object": profile_user_obj,
        "instance": profile_user_obj,
        "owner": is_me,
    }
    return render(request, "profiles/detail.html", context)
