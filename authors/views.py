from django.shortcuts import render
from .forms import RegisterForm


def register(request):
    if request.POST:
        form = RegisterForm(request.POST)
    else:
        form = RegisterForm()
    return render(request, 'authors/pages/register.html', {
        'form': form,
    })
