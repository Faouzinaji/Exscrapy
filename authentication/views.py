import random

from django.contrib import messages, auth
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import Landing, Price


class HomeView(View):
    template_name = 'landing.html'
    def get(self, request, *args, **kwargs):
        banner = Landing.objects.filter(section__code='bn').last()
        intro = Landing.objects.filter(section__code='int')
        pric = Landing.objects.filter(section__code='pric').last()
        last = Landing.objects.filter(section__code='last').last()
        all_price = Price.objects.all()
        context = {
            'banner': banner, 'intro': intro, 'pric': pric,
            'all_price': all_price, 'last': last
        }
        return render(request, self.template_name, context)


from .models import Profile
def send_email_otp(x,user_email,otp):


    subject = 'Verification Code'

    html_content = render_to_string('otp_email_template.html',
                                    {'first_name': x.owner.first_name, 'last_name': x.owner.last_name,'otp':otp
                                     })
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(subject, text_content, 'adnanrafique340@gmail.com', user_email)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return None

def Login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        if not email:
            messages.error(request, 'Email is required')
            return redirect('Login')
        if not password:
            messages.error(request, 'Password is required')
            return redirect('Login')
        user = auth.authenticate(username=email.split('@', 1)[0], password=password)
        if user is not None:

            login(request, user)
            return redirect('dashboard')

        else:
            messages.error(request,'Invalid ID or password')
            return redirect('Login')
    return render(request, 'Login.html')



def Logout(request):
    logout(request)
    messages.info(request,'You have been Logged Out')
    return redirect('Login')




def forget_password(request):
    if request.method == 'POST':
        Username = request.POST.get('un')
        if not Username:
            messages.error(request, 'Email is required')
            return redirect('forget_password')

        user=User.objects.filter(email=Username).first()
        print(user)

        x= Profile.objects.filter(owner=user).first()
        if user is None:
            messages.error(request,'User not found with this Email')
            return render(request, 'forget-password.html')

        otp = str(random.randint(1000, 9999))
        x.otp = otp
        x.save()
        mobile=x.phone
        print(otp)

        user_email = []
        user_email.append(user.email)
        send_email_otp(x, user_email, otp)

        request.session['mobile'] = mobile
        request.session['Username'] = user.email

        return redirect('reset_password')

    return render(request,'forget-password.html')


def reset_password(request):
    mobile = request.session['mobile']
    Username = request.session['Username']


    if request.method == 'POST':
        otp = request.POST.get('2facode')
        profile = Profile.objects.filter(owner__email=Username).first()



        if otp == profile.otp:


             request.session['Username'] = Username
             messages.success(request, 'Verification code match successfully')
             return redirect('update_password')

        else:
            messages.error(request,'Invalid OTP,please try again')
            return render(request, 'reset_password_otp.html')

    return render(request, 'reset_password_otp.html')


def update_password(request):
    Username = request.session['Username']


    if request.method == 'POST':
        users = User.objects.get(email=Username)
        user_profile = Profile.objects.get(owner=users)

        new_password = request.POST.get('new_password')



        if len(new_password)!=0:
            users.set_password(new_password)
            user_profile.changed_default_password = 'Yes'
            user_profile.save()
            users.save()

            messages.info(request, 'Password updated successfully,Please Login with New Set Password')
            return redirect('Login')

    else:

     return render(request,'update_password.html')



