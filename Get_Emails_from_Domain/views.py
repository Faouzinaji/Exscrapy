from datetime import datetime
import pandas as pd
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.files import File
# Create your views here.
import re
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import time
import stripe
from django.conf import settings
from Home.models import Wallet, User_Query
from authentication.models import Profile
from googleSearchApp.views import send_mail


#from here get email from domain code starts
url = "https://www.grokosto.com/"
EMAILS_REGEX = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
EMAIL_REGEX = r"""([^']*[A-Za-z]@[A-Za-z].[A-Za-z]+[^']+)"""


def get_emails_domain(url):
    emails_list = []

    headers = Headers(os="win", headers=True).generate()
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    for re_match in re.finditer(EMAILS_REGEX, str(soup)):
        emails_list_page = re_match.group()
        emails_list.append(emails_list_page)
    return emails_list


def get_clean_emails_domain(url):
    emails_data_domain = []
    emails_list = get_emails_domain(url)
    for re_match_clean in re.finditer(EMAIL_REGEX, str(emails_list)):
        emails_list_clean = re_match_clean.group()
        emails_data_domain.append(emails_list_clean)
        emails_data_domain = list(set(emails_data_domain))

    return emails_data_domain[0]


def get_page(url):
    headers = Headers(os="win", headers=True).generate()
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def get_links(url):
    soup = get_page(url)

    urls = soup.find_all('a')
    return urls
    # for link in soup.find_all('a'):
    #    print(link.get('href'))


def get_emails(url):
    emails_list = []
    emails_data = []
    urls = get_links(url)
    for link in urls:

        try:

            page = get_page(link.get('href'))
            time.sleep(1)

            for re_match in re.finditer(EMAILS_REGEX, str(page)):
                emails_list_page = re_match.group()
                emails_list.append(emails_list_page)
        except:
            pass

    for re_match in re.finditer(EMAIL_REGEX, str(emails_list)):
        emails_list_clean = re_match.group()
        emails_data.append(emails_list_clean)
        emails_data = list(set(emails_data))
        if emails_data:
            break
    return emails_data


def get_with_hybrid(url):
    try:
        emails = get_clean_emails_domain(url)
        print(emails)

        if emails:
            print(emails)

    except:
        emails_data = get_emails(url)
        print(emails_data)


def get_email_from_domain(request):
    user_profile = Profile.objects.get(owner=request.user)
    user_wallet = Wallet.objects.get(user_id=user_profile)




    #max_height = request.session['max_height']

    #list_page_to_extract = list_pagination(int(max_height) + 20)

    Dataset = []
    Dataset = pd.DataFrame(Dataset)

    if request.method == 'POST':
        # email = request.session.get('email')
        # search_keyword = request.session.get('search_keyword')
        # area = request.session.get('area')
        to_email = request.POST.get('email')
        user_entered_domains = request.POST.get('user_entered_domains')

        try:
            for loop in list_page_to_extract:
                try:
                    df_sample = get_data(search_keyword, area, loop)

                    try:
                        df_sample['email'] = get_with_hybrid(df_sample['links.website'])
                    except:
                        pass

                    dataset_frames = [Dataset, df_sample]
                    Dataset = pd.concat(dataset_frames, ignore_index=True, sort=False)


                except:
                    pass
        except:

            pass
        # now = datetime.now()
        # current_time = now.strftime("%d_%m_%Y_%H_%M_%S")
        # filename = str(current_time) + "_bussinesslist.csv"
        # column_names = ['title', 'place_id', 'lsig', 'place_id_search', 'rating',
        #                 'reviews', 'type', 'years_in_business', 'address', 'phone', 'hours',
        #                 'gps_coordinates.latitude', 'gps_coordinates.longitude',
        #                 'service_options.onsite_services', 'service_options.online_estimates',
        #                 'links.website']
        # Dataset.to_csv(filename, sep=',', encoding='utf-8', index=False, columns=column_names)
        received_record = 2
        #with open(filename, 'rb') as file:
            # x=User_Query.objects.create(user_id=request.user,
            #                           no_of_records_limit=received_record, query_type='Emails',
            #                           output_file=File(file)).save()

        x = User_Query.objects.create(user_id=request.user,no_of_records_limit=received_record, query_type='Emails')
        x_id=x.id
        x.save()
        #here will change the no of received_records


        list_of_domains=[]
        list_of_domains.append(user_entered_domains)

        return render(request,'check_get_email_from_domain_data.html',{'counter_pages':received_record, 'expected_price':3,'user_wallet':user_wallet,'list_of_domains':list_of_domains,'x':x_id})


    return render(request,'get_emails_from_domain_index.html')


def get_data_email_from_domain(request):
    user_profile = Profile.objects.get(owner=request.user)
    user_wallet = Wallet.objects.get(user_id=user_profile)

    if request.method == 'POST':
        x_id= request.POST.get('xid')
        no_of_record= request.POST.get('no_of_record')
        expected_price= request.POST.get('expected_price')

        if user_wallet.available_requests_balance>=int(no_of_record):
            user_query_record=User_Query.objects.get(pk=x_id)
            #here we will change the display option to yes and will redirect user to dashboard

        else:
            request.session['generated_record_email'] = x_id
            return redirect(pay_as_go_get_email_from_domain, expected_price)




def pay_as_go_get_email_from_domain(request,expected_price):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    generated_record_email = request.session.get('generated_record_email')

    session = stripe.checkout.Session.create(

        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Pay as Go',
                },
                'unit_amount': expected_price * 100,
            },
            'quantity': 1,
        }],
        mode='payment',

        success_url=f'{request.build_absolute_uri("/")}'+'get_emails/pay_as_go_get_email_from_domain_success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=f'{request.build_absolute_uri("/")}'+'plans/payment_cancel',

        client_reference_id=generated_record_email

    )

    return redirect(session.url, code=303)

def pay_as_go_get_email_from_domain_success(request):

        print('Line no 217 done')
        session = stripe.checkout.Session.retrieve(request.GET['session_id'])
        x_id = session.client_reference_id

        user_profile = Profile.objects.get(owner=request.user)
        user_wallet = Wallet.objects.get(user_id=user_profile)




        y=User_Query.objects.get(pk=x_id)
        #update display to true here
        messages.error(request, 'Your requested file is ready and you can download on dashboard.')

        return redirect('dashboard')




