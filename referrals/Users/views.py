import random

from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string

from .forms import RegistrationForm, EditProfileForm
from .models import User


@login_required
def user_profile(request):
    return render(request, 'Users/profile.html')


def update_parent_points(points, user):
    User = get_user_model()
    if points == 0:
        return
    elif points == 1:
        user.points += 1
    else:
        if not user.parent_id:
            user.points += points
        else:
            parent_user = User.objects.get(id=user.parent_id)
            user.points += + 1
            points -= 1
            update_parent_points(points, parent_user)

    user.save()


def send_mail(request, user, form):
    current_site = get_current_site(request)
    mail_subject = 'Activate your account.'
    message = render_to_string('Users/active_email.html', {
        'user': user.username,
        'domain': current_site.domain,
        'confirmation_code': user.confirmation_code,
        'user_pk': user.pk,
    })
    to_email = form.cleaned_data.get('email')
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()


def user_register(request):
    User = get_user_model()
    form = RegistrationForm(request.POST or None, request.FILES or None)

    if request.method != 'POST' or not form.is_valid():
        return render(request, 'Users/register.html', {'form': form})

    without_code_count = User.objects.filter(without_invite_code=True).count()
    invite_code = form['invite_code'].value()

    if not invite_code and without_code_count >= 5:
        form.add_error('invite_code', error='You need to get invite code')
        return render(request, 'Users/register.html', {'form': form})

    if invite_code:
        invite_code = int(invite_code)
        try:
            parent_user = User.objects.get(invite_code=invite_code)

        except ObjectDoesNotExist:
            form.add_error('invite_code', error='Your code is wrong')
            return render(request, 'Users/register.html', {'form': form})

        else:
            children_count = User.objects.filter(parent_id=parent_user.id).count() + 1
            try:
                user = create_user(form, parent_id=parent_user.id)
            except IntegrityError:
                form.add_error('username', error='Username is used.')
                return render(request, 'Users/register.html', {'form': form})

            update_parent_points(
                children_count, parent_user)

            user.save()
            send_mail(request, user, form)

            return HttpResponse('Please confirm your email address to complete the registration')

    elif not invite_code and without_code_count < 5:
        try:
            user = create_user(form)
        except IntegrityError as e:
            form.add_error('username', error=e.message)
            return render(request, 'Users/register.html', {'form': form})

        user.without_invite_code = 1

        user.save()
        send_mail(request, user, form)

        return HttpResponse('Please confirm your email address to complete the registration')


def user_activate(request, confirmation_code, user_pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=user_pk)
    code = user.confirmation_code
    confirmation_code = int(confirmation_code)

    if user and confirmation_code == code:
        user.is_active = True
        user.email_verified = True
        user.confirmation_code = 0
        user.save()
        user = authenticate(user=user)
        if user.is_active:
            login(request, user)
            return redirect('user_profile')
    else:
        return HttpResponse('Activation link is invalid!')


@login_required
def edit_profile(request):
    user = request.user
    data = {'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'invite_code': user.invite_code,
            }
    form = EditProfileForm(request.user, request.POST or None, request.FILES or None, initial=data)
    if form.is_valid():
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = form.cleaned_data['email']
        user.avatar = form.cleaned_data['avatar']
        user.set_password(form.cleaned_data['password1'])
        user.save()
        user = authenticate(user=user)
        login(request, user)
        return redirect('user_profile')

    return render(request, "Users/edit_profile.html", {"form": form})


@login_required
def profile_view(request):
    User = get_user_model()
    user = User.objects.get(pk=request.user.id)

    return render(request, 'Users/profile.html', {"user": user})


@login_required
def generate_code(request):
    user = request.user
    user.invite_code = random.randint(100000000, 999999999)
    user.save()
    return redirect('edit_profile')


def create_user(form, parent_id=None):
    User = get_user_model()
    user = User.objects.create_user(
        username=form.cleaned_data['username'],
        email=form.cleaned_data['email'],
        avatar=form.cleaned_data['avatar'],
        confirmation_code=random.randint(100000000, 999999999),
        invite_code=random.randint(100000000, 999999999))
    user.is_active = False
    user.set_password(form.cleaned_data['password1'])

    if parent_id is not None:
        user.parent_id = parent_id

    return user


@login_required
def top_ten(request):
    top = User.objects.all().order_by('-points')
    top = filter(
        lambda x: x.points > 0, top[:10]
    )

    return render(request, 'Users/top_ten.html', {'top': top})
