from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .forms import RegistrationForm

User = get_user_model()


def register(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()

            messages.success(
                request,
                'Your account has been created successfully!'
            )

            login(request, user)

            return redirect('dashboard')

    else:
        form = RegistrationForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )

from .decorators import role_required


@login_required
def dashboard(request):

    if request.user.role == 'manager':
        return redirect('manager_dashboard')

    return redirect('member_dashboard')


@role_required('manager')
def manager_dashboard(request):

    return render(
        request,
        'accounts/manager_dashboard.html'
    )


@role_required('member')
def member_dashboard(request):

    return render(
        request,
        'accounts/member_dashboard.html'
    )
from .forms import ProfileForm


@login_required
def profile(request):

    return render(
        request,
        'accounts/profile.html',
        {'user_profile': request.user}
    )


@login_required
def edit_profile(request):

    if request.method == 'POST':

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=request.user
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Your profile has been updated!'
            )

            return redirect('profile')

    else:

        form = ProfileForm(instance=request.user)

    return render(
        request,
        'accounts/edit_profile.html',
        {'form': form}
    )