from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from .forms import ChatUserCreationForm, ChatUserAuthenticationForm
from .models import ChatUser


INCORRECT_PASSWORD = 'Wrong password. Try again'
PASSWORDS_DONT_MATCH = 'Passwords don\'t match. Try again'
UNKNOWN_ERROR = 'Weak password. Try again'


def USER_DOES_NOT_EXIST(id):
    return f'User with name {id} does not exist'


def USER_ALREADY_EXISTS(id):
    return f'User with name {id} already exists'


def auth(request):
    if request.user.is_authenticated:
        return JsonResponse({
            'redirect_url': request.build_absolute_uri('/chat'),
        }, status=200)
    if request.method == 'POST' and request.is_ajax():
        if request.POST.get('submit') == 'signup':
            form = ChatUserCreationForm(data=request.POST)
            if form.is_valid():
                form.save()
                id = form.cleaned_data.get('id')
                password = form.cleaned_data.get('password1')
                user = authenticate(id=id, password=password)
                login(request, user)
                try:
                    user = ChatUser.objects.get(id=request.user.id)
                    user.status = 1
                    user.save()
                except ChatUser.DoesNotExist:
                    return JsonResponse({
                        'error_message': UNKNOWN_ERROR,
                        'type': 'id',
                    }, status=404)
                except IntegrityError:
                    return JsonResponse({
                        'error_message': UNKNOWN_ERROR,
                        'type': 'id',
                    }, status=404)
                except Exception:
                    return JsonResponse({
                        'error_message': UNKNOWN_ERROR,
                        'type': 'id',
                    }, status=404)

                return JsonResponse({
                    'redirect_url': request.build_absolute_uri('/chat'),
                }, status=201)

            id = request.POST.get('id')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            if ChatUser.objects.filter(id=id).exists():
                return JsonResponse({
                    'error_message': USER_ALREADY_EXISTS(id),
                    'type': 'id',
                }, status=400)
            if password1 != password2:
                return JsonResponse({
                    'error_message': PASSWORDS_DONT_MATCH,
                    'type': 'password',
                }, status=400)

            return JsonResponse({
                'error_message': UNKNOWN_ERROR,
            }, status=404)

        elif request.POST.get('submit') == 'signin':
            form = ChatUserAuthenticationForm(data=request.POST)
            if form.is_valid():
                id = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(id=id, password=password)
                if user:
                    login(request, user)
                    try:
                        user = ChatUser.objects.get(id=request.user.id)
                        user.status = 1
                        user.save()
                    except ChatUser.DoesNotExist:
                        return JsonResponse({
                            'error_message': USER_DOES_NOT_EXIST(id),
                            'type': 'id',
                        }, status=404)
                    except IntegrityError:
                        return JsonResponse({
                            'error_message': UNKNOWN_ERROR,
                            'type': 'id',
                        }, status=404)
                    except Exception:
                        return JsonResponse({
                            'error_message': UNKNOWN_ERROR,
                            'type': 'id',
                        }, status=404)

                    return JsonResponse({
                        'redirect_url': request.build_absolute_uri('/chat'),
                    }, status=200)
                else:
                    return JsonResponse({
                        'error_message': UNKNOWN_ERROR,
                        'type': 'id',
                    }, status=404)

            id = request.POST.get('username')
            password = request.POST.get('password')
            try:
                user = ChatUser.objects.get(id=id)
                if user.password != password:
                    return JsonResponse({
                        'error_message': INCORRECT_PASSWORD,
                        'type': 'password',
                    }, status=400)

                return JsonResponse({
                    'error_message': UNKNOWN_ERROR,
                    'type': 'id',
                }, status=404)
            except ChatUser.DoesNotExist:
                return JsonResponse({
                    'error_message': USER_DOES_NOT_EXIST(id),
                    'type': 'id',
                }, status=400)
        else:
            request.session['auth_type'] = request.POST.get('auth_type')
            if request.session.get('auth_type') == 'signup':
                form = ChatUserCreationForm()
                return render(request, 'accounts/signup.html', {'form': form})
            elif request.session.get('auth_type') == 'signin':
                form = ChatUserAuthenticationForm()
                return render(request, 'accounts/signin.html', {'form': form})

    # request.GET
    else:
        if request.GET.get('auth_type') is not None:
            request.session['auth_type'] = request.GET.get('auth_type')

        if request.session.get('auth_type') == 'signup':
            form = ChatUserCreationForm()
        else:
            form = ChatUserAuthenticationForm()

    return render(request, 'accounts/_base.html', {'form': form})


@login_required
def logout(request):
    try:
        user = ChatUser.objects.get(id=request.user.id)
        user.status = 0
        user.last_online = timezone.now()
        user.save()
    except ChatUser.DoesNotExist:
        redirect('auth')
    except IntegrityError:
        redirect('auth')
    except Exception:
        redirect('auth')

    django_logout(request)
    return redirect('home')
