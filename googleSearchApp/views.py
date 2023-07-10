import json
import os
from django.core.mail import EmailMessage
from payment_methods.models import *
from googleSearchScraper import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
import pandas as pd 
from datetime import datetime
from serpapi import GoogleSearch
from django.core.files import File
from Home.models import Wallet
from authentication.models import Profile
from django.contrib import messages
from django.db import transaction
from email.mime.application import MIMEApplication
from Home.models import *
import stripe
from .models import *
from googleSearchScraper import settings


def send_mail(strValue, to_email):
    # Create a multipart message
    subject = 'Business Data'
    message = 'Requested Business Data'
    mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [to_email, 'rayhunboss27@gmail.com'])
    file_path = os.path.join(settings.BASE_DIR, strValue)
    with open(file_path,'rb') as file:
        mail.attach(MIMEApplication(file.read(), Name=strValue))
    mail.send()

    return None


@login_required
def index(request):
    users = Profile.objects.get(owner__email=request.user.email)
    user_wallet = Wallet.objects.get(user_id=users)
    categories=Categories.objects.all()

    countries = Country.objects.order_by('country').values('country').distinct()
    current_active_plan_price = 0.01
    if Subscriber.objects.filter(user=request.user, status='Active').exists():
        current_active_plan = Subscriber.objects.get(user=request.user, status='Active')
        current_active_plan_price = current_active_plan.plan.perline_price


    if request.method == 'POST':
            activity = request.POST.get('activity')
            query_reference = request.POST.get('query_reference')
            selected_country = request.POST.get('selected_country')
            selected_state = request.POST.get('selected_state')
            selected_places = request.POST.getlist('places')
            if activity == 'Select':
                messages.error(request, 'Select Business Category')
                return redirect('index')
            selected_items = 0
            search_keywords=[]
            if selected_places:
                for db_data in selected_places:
                    selected_items += 1
                    search_keywords.append(activity+ ' in '+ db_data+ ',' + selected_country)
            else:
                if not selected_state and selected_country:
                    place = Country.objects.filter(country=selected_country)
                    if place:
                        for db_data in place:
                            print(f"place====== {place}, db_data ========={db_data}")
                            selected_items += 1
                            search_keywords.append(activity + ' in ' + db_data.place + ',' + selected_country)
            sum_queries = selected_items * 15
            sum_rows = sum_queries * 20
            expected_price=sum_rows * current_active_plan_price
            expected_time_min=pd.to_timedelta(int(sum_queries), unit='m')
            expected_time_max=pd.to_timedelta(int(sum_queries*3), unit='m')

            request.session['search_keyword'] = search_keywords
            request.session['activity'] = activity
            request.session['query_reference'] = query_reference
            request.session['received_record'] = sum_queries
            request.session['expected_price'] = expected_price
            context = {'few_lines': search_keywords, "num": sum_rows,'selected_items':selected_items,'expected_price':expected_price,'sum_queries':sum_queries,'user_profile':users,'user_wallet':user_wallet,'expected_time_min':expected_time_min,'expected_time_max':expected_time_max}
            return render(request, 'checkdata.html', context)
            # return render(request, 'index.html', {'user_wallet':user_wallet,'countries':countries,'categories':categories,'user_profile':users})
    return render(request, 'index.html', {'user_wallet':user_wallet,'countries':countries,'categories':categories,'user_profile':users})


@login_required
def getdata(request):
    if request.method == 'POST':
        promocode_list = ["1212121" , "222222" ]
        promocode = request.session.get('promocode')
        if promocode in promocode_list:
            #if this excute so u will add discount in payment
            print("get discount")

        # add apyment checkout code here so that it will show in getdata template
        return render(request, 'getData.html')              
    return render(request, 'index.html')


@login_required
def get_data_option(request):
    users = Profile.objects.get(owner__email=request.user.email)
    user_wallet = Wallet.objects.get(user_id=users)
    return render(request,'get_data_option.html',{'user_wallet':user_wallet})


def signup_redirect(request):
    if request.user.is_authenticated:
        messages.error(request, "Something wrong here, it may be that you already have account!")
        return redirect("dashboard")
    else:
        return redirect("Login")


@login_required
def getdatabycsv(request):
    user_profile=Profile.objects.get(owner=request.user)
    user_wallet=Wallet.objects.get(user_id=user_profile)
    if request.method == 'GET' or request.method == 'POST':
        received_record = request.session.get('received_record')
        search_keyword = request.session.get('search_keyword')
        activity = request.session.get('activity')
        query_reference = request.session.get('query_reference')
        expected_price = request.session.get('expected_price')
        if received_record < user_wallet.available_requests_balance:
            data_dic=[]
            for item in search_keyword:
                params = {
                        "engine": "google_maps",
                        "q": item,
                        "type": "search",
                        "start": 0,
                        "ll": "@40.7455096,-74.0083012,14z",
                        "api_key":"589c12eaa768b8bfbf721ffb8961347436051c017b86335a7d6f0e1e498fb2e4"

                        }
                client = GoogleSearch(params)
                data = client.get_dict()
                try:
                    for result in data['local_results']:
                        try:
                            title = result['title']
                        except:
                            title = "Not Available"
                        try:
                            address = result['address']
                        except:
                            address = "Not Available"
                        try:
                            rating = result['rating']
                        except:
                            rating = "Not Available"
                        try:
                            reviews = result['reviews']
                        except:
                            reviews = "Not Available"
                        try:
                            type_search = result['type']
                        except:
                            type_search = "Not Available"
                        try:
                            open_state = result['open_state']
                        except:
                            open_state = "Not Available"
                        try:
                            phone = result['phone']
                        except:
                            phone = "Not Available"
                        try:
                            website = result['website']
                        except:
                            website = "Not Available"
                        try:
                            description = result['description']
                        except:
                            description = "Not Available"
                        dict = {
                            "Bussines Type": type_search,
                            "Bussines Name": title,
                            "Bussines Description": description,
                            "Bussines Address": address,
                            "Bussines Hours ": open_state,
                            "Bussines Phone ": phone,
                            "Bussines Website ": website,
                            "Bussines Rating": rating,
                            "Bussines Reviews": reviews,
                        }
                        data_dic.append(dict)

                except Exception as e:
                        print('Exception at line no 247 is', e)
                        pass

            df = pd.DataFrame(data_dic)
            now = datetime.now()
            current_time = now.strftime("%d_%m_%Y_%H_%M_%S")
            filename=str(current_time)+"_bussinesslist.csv"
            df.to_csv(filename, index=False)

            send_mail(filename, request.user.email)

            user_wallet.available_requests_balance-=received_record
            user_wallet.save()

            with open(filename, 'rb') as file:
                User_Query.objects.create(
                    user_id=request.user, category=activity, 
                    no_of_records_limit=received_record, query_type='Locations',
                    query_name=query_reference,
                    query_list=json.dumps(search_keyword), output_file=File(file)
                )
            messages.error(request, 'Your requested file is ready and you can download on dashboard.')
            return redirect('dashboard')
        else:
            return render(request,'pay_as_go.html',{'counter_pages':received_record, 'expected_price':int(expected_price),'user_wallet':user_wallet,'user_profile':user_profile})


@login_required
def pay_as_go(request, expected_price):
    stripe.api_key = settings.STRIPE_SECRET_KEY
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
        success_url=f'{request.build_absolute_uri("/")}'+'google_search/pay_as_go_success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=f'{request.build_absolute_uri("/")}'+'plans/payment_cancel',
        client_reference_id=expected_price

    )

    return redirect(session.url, code=303)


@login_required
def pay_as_go_success(request):
        try:
            session = stripe.checkout.Session.retrieve(request.GET['session_id'])
            received_record = request.session.get('received_record')
            activity = request.session.get('activity')
            query_reference = request.session.get('query_reference')
            search_keyword = request.session.get('search_keyword')
            data_dic = []
            for item in search_keyword:
                params = {
                    "engine": "google_maps",
                    "q": item,
                    "type": "search",
                    "start": 0,
                    "ll": "@40.7455096,-74.0083012,14z",
                    "api_key": "589c12eaa768b8bfbf721ffb8961347436051c017b86335a7d6f0e1e498fb2e4"
                }
                client = GoogleSearch(params)
                data = client.get_dict()
                try:
                    for result in data['local_results']:
                        try:
                            title = result['title']
                        except:
                            title = "Not Available"
                        try:
                            address = result['address']
                        except:
                            address = "Not Available"
                        try:
                            rating = result['rating']
                        except:
                            rating = "Not Available"
                        try:
                            reviews = result['reviews']
                        except:
                            reviews = "Not Available"
                        try:
                            type_search = result['type']
                        except:
                            type_search = "Not Available"
                        try:
                            open_state = result['open_state']
                        except:
                            open_state = "Not Available"
                        try:
                            phone = result['phone']
                        except:
                            phone = "Not Available"
                        try:
                            website = result['website']
                        except:
                            website = "Not Available"
                        try:
                            description = result['description']
                        except:
                            description = "Not Available"
                        dict = {
                            "Bussines Type": type_search,
                            "Bussines Name": title,
                            "Bussines Description": description,
                            "Bussines Address": address,
                            "Bussines Hours ": open_state,
                            "Bussines Phone ": phone,
                            "Bussines Website ": website,
                            "Bussines Rating": rating,
                            "Bussines Reviews": reviews,
                        }
                        data_dic.append(dict)
                except Exception as e:
                    print(e)

            df = pd.DataFrame(data_dic)
            now = datetime.now()
            current_time = now.strftime("%d_%m_%Y_%H_%M_%S")
            filename = str(current_time) + "_bussinesslist.csv"
            df.to_csv(filename, index=False)
            send_mail(filename, request.user.email)

            with open(filename, 'rb') as file:
                User_Query.objects.create(
                    user_id=request.user, category=activity,
                    no_of_records_limit=received_record,query_name=query_reference,
                    query_type='Locations',query_list=json.dumps(search_keyword),
                    output_file=File(file)
                )
            messages.error(request, 'Your requested file is ready and you can download on dashboard.')
            return redirect('dashboard')
        except Exception as e:
            messages.error(request, "Payment failed, please try again.")
            return redirect('dashboard')


@login_required
def run_again_query(request, id):
    user_profile = Profile.objects.get(owner=request.user)
    user_wallet = Wallet.objects.get(user_id=user_profile)
    query_obj=User_Query.objects.get(pk=id)
    if query_obj.no_of_records_limit < user_wallet.available_requests_balance:
        jsonDec = json.decoder.JSONDecoder()
        myPythonList = jsonDec.decode(query_obj.query_list)
        data_dic = []
        for item in myPythonList:
            params = {
                "engine": "google_maps",
                "q": item,
                "type": "search",
                "start": 0,
                "ll": "@40.7455096,-74.0083012,14z",
                "api_key": "589c12eaa768b8bfbf721ffb8961347436051c017b86335a7d6f0e1e498fb2e4"
            }
            client = GoogleSearch(params)
            data = client.get_dict()
            try:
                while ('next' in data['serpapi_pagination']):
                    client.params_dict["start"] += len(data['local_results'])
                    data = client.get_dict()
                    try:
                        for result in data['local_results']:
                            try:
                                print('Line no 604', result['title'])
                                title = result['title']
                            except:
                                title = "Not Available"
                            try:
                                address = result['address']
                            except:
                                address = "Not Available"
                            try:
                                rating = result['rating']
                            except:
                                rating = "Not Available"
                            try:
                                reviews = result['reviews']
                            except:
                                reviews = "Not Available"
                            try:
                                type_search = result['type']
                            except:
                                type_search = "Not Available"
                            try:
                                open_state = result['open_state']
                            except:
                                open_state = "Not Available"
                            try:
                                phone = result['phone']
                            except:
                                phone = "Not Available"
                            try:
                                website = result['website']
                            except:
                                website = "Not Available"
                            try:
                                description = result['description']
                            except:
                                description = "Not Available"
                            dict = {
                                "Bussines Type": type_search,
                                "Bussines Name": title,
                                "Bussines Description": description,
                                "Bussines Address": address,
                                "Bussines Hours ": open_state,
                                "Bussines Phone ": phone,
                                "Bussines Website ": website,
                                "Bussines Rating": rating,
                                "Bussines Reviews": reviews,
                            }
                            data_dic.append(dict)
                    except Exception as e:
                        pass
            except Exception as e:
                pass
        df = pd.DataFrame(data_dic)
        now = datetime.now()
        current_time = now.strftime("%d_%m_%Y_%H_%M_%S")
        filename = str(current_time) + "_bussinesslist.csv"
        df.to_csv(filename, index=False)

        send_mail(filename, request.user.email)
        user_wallet.available_requests_balance -= int(query_obj.no_of_records_limit)
        user_wallet.save()

        with open(filename, 'rb') as file:

            User_Query.objects.create(
                user_id=request.user, category=query_obj.category,
                no_of_records_limit=query_obj.no_of_records_limit, 
                query_name=query_obj.query_name, query_type='Locations',
                query_list=json.dumps(myPythonList), output_file=File(file)
            )
        messages.success(request, 'Your requested file is ready and you can download on dashboard.')
        return redirect('dashboard')
    else:
        msg_text=f'You must have {query_obj.no_of_records_limit} credit lines in your account to rerun this query. Please Buy plan'
        messages.error(request, msg_text)
        return redirect('dashboard')


@transaction.atomic
def bulk_record_creator(db_lst):
    # Loop over each store and invoke save() on each entry
    for data in db_lst:
        # save() method called on each member to create record
        data.save()

def import_data1(request):

    db_lst=[]
    df = pd.read_csv('static/datafiles/locations.csv')
    print(df)

    for index, row in df.iterrows():
        if row['country'] and row['state'] and row['place']:
            if row['zipcode']:
                db_lst.append(Country(country=row['country'],state=row['state'],place=row['place'],zipcode=row['zipcode']))
            else:
                db_lst.append(Country(country=row['country'],state=row['state'],place=row['place']))
    print(len(db_lst))
    bulk_record_creator(db_lst)


    return HttpResponse('Record added')


def import_data2(request):


    df = pd.read_excel('static/datafiles/categories(2).xlsx')

    dbframe = df
    for dbframe in dbframe.itertuples():
        obj=Categories.objects.create(name=dbframe.Categories)
        obj.save()

    return HttpResponse('Record added')


@csrf_exempt
def dropdown_get_country(request):
    if request.method == "POST":
        country = request.POST['country']
        print(country)
        data=[]
        states = Country.objects.filter(country=country).values('state').distinct()
        for state in states:
            if state['state']!='nan':
                data.append(state['state'])
        print(data)

        return JsonResponse( {'data':data}, safe=False)

@csrf_exempt
def dropdown_get_state(request):
    if request.method == "POST":
        state = request.POST['state']
        country = request.POST['country']
        print(country,state)

        data=[]
        places = Country.objects.filter(country=country,state=state).values('place').distinct()
        for place in places:
            if place['place']!='nan':
                data.append(place['place'])
        print(len(data))

        return JsonResponse( {'data':data}, safe=False)

