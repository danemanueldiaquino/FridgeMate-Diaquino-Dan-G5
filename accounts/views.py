from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .decorators import role_required
from .forms import FridgeItemForm, ProfileForm, RegistrationForm
from .models import FridgeItem

User = get_user_model()


def custom_404(request, exception):
    return render(request, '404.html', status=404)


def custom_500(request):
    return render(request, '500.html', status=500)


def _can_manage_all(user):
    return getattr(user, 'role', '') == 'manager' or user.is_superuser


def _scoped_items_queryset(user):
    if _can_manage_all(user):
        return FridgeItem.objects.select_related('owner')
    return FridgeItem.objects.filter(owner=user)


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


@login_required
def dashboard(request):

    if request.user.role == 'manager':
        return redirect('manager_dashboard')

    return redirect('member_dashboard')


@role_required('manager')
def manager_dashboard(request):
    items = FridgeItem.objects.select_related('owner')[:10]
    total_items = FridgeItem.objects.count()
    return render(
        request,
        'accounts/manager_dashboard.html',
        {
            'recent_items': items,
            'total_items': total_items,
        }
    )


@role_required('member')
def member_dashboard(request):
    items = FridgeItem.objects.filter(owner=request.user)[:10]
    total_items = FridgeItem.objects.filter(owner=request.user).count()
    return render(
        request,
        'accounts/member_dashboard.html',
        {
            'recent_items': items,
            'total_items': total_items,
        }
    )


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


@login_required
def fridge_item_list(request):
    items = _scoped_items_queryset(request.user).select_related('owner')
    zone_filter = request.GET.get('zone', '').strip()

    if zone_filter in dict(FridgeItem.StorageZone.choices):
        items = items.filter(zone=zone_filter)

    return render(
        request,
        'accounts/fridge_item_list.html',
        {
            'items': items,
            'selected_zone': zone_filter,
            'zones': FridgeItem.StorageZone.choices,
            'can_manage_all': _can_manage_all(request.user),
        }
    )


@login_required
def fridge_item_create(request):
    if request.method == 'POST':
        form = FridgeItemForm(request.POST, owner=request.user)
        if form.is_valid():
            with transaction.atomic():
                item = form.save(commit=False)
                item.owner = request.user
                item.save()
            messages.success(request, f'Added "{item.name}" to fridge tracking.')
            return redirect('fridge_item_list')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = FridgeItemForm()

    return render(
        request,
        'accounts/fridge_item_form.html',
        {
            'form': form,
            'page_title': 'Add Fridge Item',
            'submit_label': 'Save Item',
        }
    )


@login_required
def fridge_item_update(request, pk):
    item = get_object_or_404(_scoped_items_queryset(request.user), pk=pk)

    if request.method == 'POST':
        form = FridgeItemForm(request.POST, instance=item, owner=item.owner)
        if form.is_valid():
            with transaction.atomic():
                form.save()
            messages.success(request, f'Updated "{item.name}".')
            return redirect('fridge_item_list')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = FridgeItemForm(instance=item)

    return render(
        request,
        'accounts/fridge_item_form.html',
        {
            'form': form,
            'page_title': 'Edit Fridge Item',
            'submit_label': 'Update Item',
        }
    )


@login_required
def fridge_item_delete(request, pk):
    item = get_object_or_404(_scoped_items_queryset(request.user), pk=pk)

    if request.method == 'POST':
        item_name = item.name
        with transaction.atomic():
            item.delete()
        messages.success(request, f'Removed "{item_name}" from fridge tracking.')
        return redirect('fridge_item_list')

    return render(
        request,
        'accounts/fridge_item_confirm_delete.html',
        {'item': item}
    )