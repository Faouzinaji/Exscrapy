import os
from typing import Any
from django.conf import settings
from django.db.models import Sum
from django.views.generic import DetailView, UpdateView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from authentication.models import Profile
from django.contrib import auth, messages
from django.urls import reverse_lazy
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from payment_methods.models import Subscriber
from .models import *


def dashboard(request):
    # print('line no 15', request.user.password,request.user.first_name,request.user.last_name,request.user.email,request.user.username)
    try:
        users = Profile.objects.get(owner__email=request.user.email)
        user_wallet=Wallet.objects.get(user_id=users)
        user_quries=User_Query.objects.filter(user_id=request.user).order_by('-id')


        if users.changed_default_password == 'No':
            return redirect('setting_security')


        context = {'user_profile': users,'user_wallet':user_wallet,'user_quries':user_quries}


        return render(request, 'dashboard.html', context)
    except Exception as e:
        print('line no 33 exception is',e)

        y = Profile.objects.create(owner=request.user, changed_default_password='No',
                                   joined_via='Google Authentication')

        if not Wallet.objects.filter(user_id=y).exists():
            purse = Wallet.objects.create(

                user_id=y,
                available_requests_balance=0,

                description='Wallet created on Sign Up'

            )
            purse.save()



        else:
            pass

        y.save()

        # user_email = []
        # user_email.append(request.user.email)
        #
        # subject = 'Thank you for account creation with us.'
        #
        # html_content = render_to_string('email_template.html',
        #                                 {'first_name': request.user.first_name, 'last_name': request.user.last_name,
        #                                  })
        # text_content = strip_tags(html_content)
        #
        # msg = EmailMultiAlternatives(subject, text_content, 'adnanrafique340@gmail.com', user_email)
        # msg.attach_alternative(html_content, "text/html")
        # msg.send()

        return redirect('dashboard')


class UpdateProfileView(UpdateView):
    template_name = 'update.html'
    model = Profile
    fields = ['phone', 'picture', 'gender', 'profession']
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        messages.success(self.request, "The profile was updated successfully.")
        return super(UpdateProfileView,self).form_valid(form)


class UserProfileView(DetailView):
    template_name = 'profile.html'
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.model.objects.get(pk=self.kwargs["pk"])
        subscriber = user.subscriber_set.all()
        available = user.profile.wallet_set.all().last().available_requests_balance
        no_of_lines = subscriber.aggregate(Sum('plan__no_of_lines'))['plan__no_of_lines__sum']
        spent = int(no_of_lines) - int(available)
        context['user'] = user
        context['spent'] = spent
        context['no_of_lines'] = no_of_lines
        context['subscriber'] = subscriber.last()
        context['all_subscriber'] = subscriber.order_by('status')
        return context


@login_required(login_url='Login')
def Setting(request):
    users = User.objects.get(username=request.user)

    user_profile = Profile.objects.get(owner=users)
    user_wallet = Wallet.objects.get(user_id=user_profile)

    if user_profile.changed_default_password == 'No':
        return redirect('setting_security')




    context = {'user_profile': user_profile, 'users': users,'user_wallet':user_wallet}
    if request.method == 'POST':
        fname = request.POST.get('firstname')
        lname = request.POST.get('lastname')
        email = request.POST.get('Email')
        phone = request.POST.get('phone')


        if len(fname) != 0:
            users.first_name = fname
        if len(lname) != 0:
            users.last_name = lname
        if len(email) != 0:
            users.email = email



        if len(request.FILES) != 0:
            my_file = request.FILES['upload']

            if my_file.content_type == 'image/jpg' or my_file.content_type == 'image/jpeg' or my_file.content_type == 'image/png':
                user_profile.picture = request.FILES['upload']

                users.save()
                user_profile.save()

                messages.success(request, 'Data updated successfully')
                return redirect('Settings')

            messages.success(request, 'Only JPG, PNG & JPEG image type is allowed')
            return redirect('Settings')
        users.save()
        messages.success(request, 'Data updated successfully')
        return redirect('Settings')

    return render(request, 'settings.html', context)


@login_required(login_url='Login')
def setting_security(request):
    user_profile = Profile.objects.get(owner=request.user)



    context = {'user_profile': user_profile}
    if request.method == 'POST':
        users = User.objects.get(email=request.user.email)
        current_password = request.POST.get('current_password')
        phone = request.POST.get('phone')

        new_password = request.POST.get('new_password')

        if len(new_password) != 0:
            users.set_password(new_password)
            users.save()
            # if len(phone) != 0:
            user_profile.changed_default_password = 'Yes'
            user_profile.save()
            user = auth.authenticate(username=request.user.username, password=new_password)
            if user is not None:
                login(request, user)
                messages.info(request, 'Password updated successfully.')
                return redirect('pricing')
    else:

        return render(request, 'settings-security.html', context)


def contact_us(request):
    users = Profile.objects.get(owner=request.user)
    user_wallet = Wallet.objects.get(user_id=users)
    if users.changed_default_password == 'No':
        return redirect('setting_security')

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')

        subject = request.POST.get('subject')
        message = request.POST.get('message')
        user_email = []
        user_email.append(request.user.email)

        html_content = render_to_string(
            'email_template_contact_us.html',
            {'name': name, 'email': email, 'subject': subject, 'message': message}
        )
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, user_email)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        messages.info(request, 'Email sent Successfully. Admin will contact you soon.')
        return redirect('contact_us')

    context = {'user_profile': users,'user_wallet':user_wallet}

    return render(request, 'contact_us.html', context)
