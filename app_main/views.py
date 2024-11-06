from django.shortcuts import redirect, render


def redirect_to_home(request):
    return redirect("account")


def teacher_groups(request):
    context = {
        'groups': True,
    }
    return render(request, 'app_main/teacher-groups.html', context)
