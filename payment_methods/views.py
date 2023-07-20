from django.contrib import messages
from django.shortcuts import render, redirect

from authentication.models import Profile
from .models import *
import stripe
from googleSearchScraper import settings
from dateutil.relativedelta import relativedelta
from Home.models import Wallet
import datetime



def pricing(request):
    pricing = Price_plan.objects.all()
    users = Profile.objects.get(owner__email=request.user.email)
    user_wallet = Wallet.objects.get(user_id=users)
    sub_exist=''
    if not Subscriber.objects.filter(user=request.user, status='Active').exists():
        sub_exist='No'
        subscriber=None
    else:
        sub_exist='Yes'

        subscriber = Subscriber.objects.get(user=request.user, status='Active')
        stripe.api_key = settings.STRIPE_SECRET_KEY
        retrieve_sub = stripe.Subscription.retrieve(
            subscriber.stripeSubscriptionId
        )
        print('user accoutn status on stripe is:', retrieve_sub.status)
        if retrieve_sub.status == "active":
            subscriber.status = 'Active'
            subscriber.save()
        else:
            subscriber.status = 'Cancel'
            subscriber.save()

    return render(request, 'pricing_plan.html', {'plans': pricing,'user_wallet':user_wallet,'sub_exist':sub_exist,'current_active_plan':subscriber})


def checkout(request, plan_id):
    planDetail = Price_plan.objects.get(pk=plan_id)
    users = Profile.objects.get(owner__email=request.user.email)
    user_wallet = Wallet.objects.get(user_id=users)

    if not Subscriber.objects.filter(user=request.user, status='Active').exists():
        return render(request, 'checkout.html', {'plan': planDetail,'user_wallet':user_wallet})
    else:
        error_message_text='You already have subscription of this ' + planDetail.title + ' plan.'
        messages.error(request,error_message_text )

        return redirect('pricing')



def checkout_session(request, plan_id):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    plan = Price_plan.objects.get(pk=plan_id)
    dict = {
        'Basic Plan': settings.BASIC_PRICE_ID, 
        'Premium Plan': settings.PREMIUM_PRICE_ID,
        'Standard Plan': settings.ADVANCE_PRICE_ID
    }
    plan_price = dict[plan.title]

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            "price": plan_price,
            'quantity': 1,
        }],

        mode='subscription',
        success_url=f'{request.build_absolute_uri("/")}'+'plans/payment_success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=f'{request.build_absolute_uri("/")}'+'plans/payment_cancel',

        client_reference_id=plan_id

    )
    return redirect(session.url, code=303)


def stripe_payment_success(request):
    try:
        session_id = request.GET.get("session_id")
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)
        plan_id = session.client_reference_id
        stripe_subscription_id = session.subscription
        stripe_customer_id = session.customer
        plan = Price_plan.objects.get(pk=plan_id)
        user_profile = Profile.objects.get(owner=request.user)
        user_wallet = Wallet.objects.get(user_id=user_profile)
        user = request.user
        try:
            subsciber_details = Subscriber.objects.get(user=user, status='Active')
            subsciber_details.status = 'Expire'
            subsciber_details.save()
        except Exception as e:
            pass

        subsciption_from = datetime.date.today(),
        subsciption_to = datetime.date.today() + relativedelta(months=1)
        Subscriber.objects.create(
            plan=plan,
            user=user,
            price=plan.price,
            status='Active',
            payment_method='Stripe',
            subsciption_from=datetime.date.today(),
            stripeCustomerId=stripe_customer_id,
            stripeSubscriptionId=stripe_subscription_id,
            subsciption_to=datetime.date.today() + relativedelta(months=1)
        )
        #updating the user wallet of no of lines
        user_wallet.available_requests_balance+=plan.no_of_lines
        user_wallet.save()
        #creating a transaction
        transaction_history.objects.create(user_id=user,plan=plan).save()
        user_email = user.email
        plan_title = plan.title
        #send_payment_success_email(user_email, plan_title, subsciption_from, subsciption_to)

        return render(request, 'payment_success.html',{'subsciption_from':subsciption_from,'subsciption_to':subsciption_to,'plan_title':plan_title,'user_wallet':user_wallet})
    except Exception as e:
        print('exception at line 83 is:', e)
        users = Profile.objects.get(owner__email=request.user.email)
        user_wallet = Wallet.objects.get(user_id=users)
        return render(request, 'payment_cancel.html',{'user_wallet':user_wallet})


def payment_cancel(request):
    users = Profile.objects.get(owner__email=request.user.email)
    user_wallet = Wallet.objects.get(user_id=users)
    return render(request, 'payment_cancel.html',{'user_wallet':user_wallet})


def cancel_subscription(request):
    subscriber=Subscriber.objects.get(user=request.user,status='Active')
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe.Subscription.delete(
        subscriber.stripeSubscriptionId
    )
    subscriber.status='Cancel'
    subscriber.save()
    messages.error(request,'Active subscription cancelled successfully.')
    return redirect('pricing')