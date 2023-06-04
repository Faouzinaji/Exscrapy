import json
import os
from payment_methods.models import *
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import random
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from selenium import webdriver
import pandas as pd 
from datetime import datetime
from serpapi import GoogleSearch
from django.core.files import File
from Home.models import Wallet
from authentication.models import Profile
from .forms import MyForm
from django.contrib import messages
from django.db import transaction
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import smtplib
from Home.models import *
import stripe
from django.conf import settings
from django.core.paginator import Paginator
from .models import *


def send_mail(strValue,to_email):
    # Create a multipart message
    msg = MIMEMultipart()
    body_part = MIMEText('Requested Business Data', 'plain')
    msg['Subject'] = 'Business Data'
    msg['From'] = 'adnanrafique340@gmail.com'
    msg['To'] = to_email
    # Add body to email
    msg.attach(body_part)






    file_path = os.path.join(settings.BASE_DIR, strValue)
    print('line no 34 done')
    with open(file_path,'rb') as file:
    # Attach the file with filename to the email
        msg.attach(MIMEApplication(file.read(), Name=strValue))

    # Create SMTP object

    smtp_obj = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_obj.starttls()
    # Login to the server
    smtp_obj.login('adnanrafique340@gmail.com', 'gqivvfogakumclyd')



    smtp_obj.sendmail(msg['From'], msg['To'], msg.as_string())
    smtp_obj.quit()
    return None
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

            print('Line no 88 selected address are:',selected_country, selected_state,selected_places)



            if activity == 'Select':
                messages.error(request, 'Select Business Category')
                return redirect('index')




            selected_items = 0
            search_keywords=[]
            if selected_places:


                for data in selected_places:

                        place = Country.objects.filter(country=selected_country, place=data)
                        print('line no 109', place)
                        if place:

                            for db_data in place:
                                print('Line no 110', db_data.place, db_data.zipcode)
                                selected_items += 1
                                dict={}

                                if db_data.zipcode != 'nan':
                                    print('Search Keyword is:', db_data.zipcode.partition('.')[0] + ','+db_data.place+ ',' + selected_country)


                                    search_keywords.append(activity+ ' in '+ db_data.place+ ',' + selected_country)

                                else:

                                    search_keywords.append(activity+ ' in '+ db_data.place+ ',' + selected_country)
                print('search keyword list is:',search_keywords)
            else:
                if not selected_state:
                    place = Country.objects.filter(country=selected_country)
                    print('line no 128', place)
                    if place:

                        for db_data in place:
                            print('Line no 132', db_data.place, db_data.zipcode)
                            selected_items += 1
                            dict = {}

                            if db_data.zipcode != 'nan':
                                print('Search Keyword is:',
                                      db_data.zipcode.partition('.')[0] + ',' + db_data.place + ',' + selected_country)

                                search_keywords.append(activity + ' in ' + db_data.place + ',' + selected_country)

                            else:

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

        




    return render(request, 'index.html',{'user_wallet':user_wallet,'countries':countries,'categories':categories,'user_profile':users})


# add payment code here
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

def get_data_option(request):
    users = Profile.objects.get(owner__email=request.user.email)
    user_wallet = Wallet.objects.get(user_id=users)
    return render(request,'get_data_option.html',{'user_wallet':user_wallet})



def  getdatabycsv(request):
    user_profile=Profile.objects.get(owner=request.user)
    user_wallet=Wallet.objects.get(user_id=user_profile)
    if request.method == 'POST':
        received_record = request.session.get('received_record')
        search_keyword = request.session.get('search_keyword')
        activity = request.session.get('activity')
        query_reference = request.session.get('query_reference')
        expected_price = request.session.get('expected_price')
        if received_record < user_wallet.available_requests_balance:
            data_dic=[]
            for item in search_keyword:
                print('Line no 173 ====================================',item)
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




                try:
                    while ('next' in data['serpapi_pagination']):
                        client.params_dict["start"] += len(data['local_results'])
                        data = client.get_dict()
                        print('Line no 201 fetched record is:', data['local_results'])
                        print('Line no 202 done.')
                        try:
                            for result in data['local_results']:
                                try:
                                    print('Line no 205',result['title'])
                                    title=result['title']
                                except:
                                    title="Not Available"
                                try:
                                    address=result['address']
                                except:
                                    address="Not Available"
                                try:
                                    rating=result['rating']
                                except:
                                    rating="Not Available"
                                try:
                                    reviews=result['reviews']
                                except:
                                    reviews="Not Available"
                                try:
                                    type_search=result['type']
                                except:
                                    type_search="Not Available"
                                try:
                                    open_state=result['open_state']
                                except:
                                    open_state="Not Available"
                                try:
                                    phone=result['phone']
                                except:
                                    phone="Not Available"
                                try:
                                    website=result['website']
                                except:
                                    website="Not Available"
                                try:
                                    description=result['description']
                                except:
                                    description="Not Available"
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
                            print('Exception at line no 243 is',e)
                            pass
                except Exception as e:
                        print('Exception at line no 247 is', e)

                        pass

            print('Line no 250 Received Records:',data_dic)

            df = pd.DataFrame(data_dic)
            now = datetime.now()
            current_time = now.strftime("%d_%m_%Y_%H_%M_%S")
            filename=str(current_time)+"_bussinesslist.csv"
            df.to_csv(filename,index=False)


            send_mail(filename, request.user.email)



            user_wallet.available_requests_balance-=received_record
            user_wallet.save()

            with open(filename, 'rb') as file:

                User_Query.objects.create(user_id=request.user, category=activity,no_of_records_limit=received_record,query_type='Locations',query_name=query_reference,
                                          query_list=json.dumps(search_keyword), output_file=File(file)).save()




            messages.error(request, 'Your requested file is ready and you can download on dashboard.')

            return redirect('dashboard')
        else:

            return render(request,'pay_as_go.html',{'counter_pages':received_record, 'expected_price':int(expected_price),'user_wallet':user_wallet,'user_profile':user_profile})



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



        success_url='http://localhost:8000/google_search/pay_as_go_success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url='https://exscrapy.herokuapp.com/plans/payment_cancel',
        #cancel_url='http://127.0.0.1:8000/plans/payment_cancel',

        client_reference_id=expected_price

    )

    return redirect(session.url, code=303)




def pay_as_go_success(request):

        session = stripe.checkout.Session.retrieve(request.GET['session_id'])

        plan_id = session.client_reference_id
        user_profile = Profile.objects.get(owner=request.user)

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
                # "api_key": "32acf64a76bfa3ba6e97b9981c565c731b558096aab97aa3a4a41ba445f98b52"
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


            try:
                while ('next' in data['serpapi_pagination']):


                    client.params_dict["start"] += len(data['local_results'])
                    print('Line no 370 done')

                    data = client.get_dict()


                    print('Line no 355 fetched record is:',data['local_results'])
                    try:
                        for result in data['local_results']:

                            try:
                                print('Line no 359 is:',result['title'])
                                title=result['title']
                            except:
                                title="Not Available"
                            try:
                                address=result['address']

                            except:
                                address="Not Available"
                            try:
                                rating=result['rating']
                            except:
                                rating="Not Available"
                            try:
                                reviews=result['reviews']
                            except:
                                reviews="Not Available"
                            try:
                                type_search=result['type']
                            except:
                                type_search="Not Available"
                            try:
                                open_state=result['open_state']
                            except:
                                open_state="Not Available"
                            try:
                                phone=result['phone']
                            except:
                                phone="Not Available"
                            try:
                                website=result['website']
                            except:
                                website="Not Available"
                            try:
                                description=result['description']
                            except:
                                description="Not Available"
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
                            print('Line no 425 done')
                    except Exception as e:
                        print('Line no 427 exception is',e)
                        pass
            except Exception as e:
                print('Line no 430 exception is', e)
                pass

        print('Line no 409 Received Records:', data_dic)

        df = pd.DataFrame(data_dic)
        now = datetime.now()
        current_time = now.strftime("%d_%m_%Y_%H_%M_%S")
        filename = str(current_time) + "_bussinesslist.csv"
        df.to_csv(filename, index=False)

        # send_mail(filename, request.user.email)



        with open(filename, 'rb') as file:

            User_Query.objects.create(user_id=request.user, category=activity,
                                      no_of_records_limit=received_record,query_name=query_reference, query_type='Locations',query_list=json.dumps(search_keyword),
                                      output_file=File(file)).save()

        messages.error(request, 'Your requested file is ready and you can download on dashboard.')

        return redirect('dashboard')


def run_again_query(request,id):
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
            for result in data['local_results']:

                try:
                    print('Line no 596', result['title'])
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


            try:
                while ('next' in data['serpapi_pagination']):
                    client.params_dict["start"] += len(data['local_results'])
                    data = client.get_dict()
                    print('Line no 599 fetched record is:', data['local_results'])
                    print('Line no 600 done.')
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
                        print('Exception at line no 654 is', e)
                        pass
            except Exception as e:
                print('Exception at line no 708 is', e)

                pass

        print('Line no 712 Received Records:', data_dic)

        df = pd.DataFrame(data_dic)
        now = datetime.now()
        current_time = now.strftime("%d_%m_%Y_%H_%M_%S")
        filename = str(current_time) + "_bussinesslist.csv"
        df.to_csv(filename, index=False)

        # send_mail(filename, request.user.email)
        user_wallet.available_requests_balance -= int(query_obj.no_of_records_limit)
        user_wallet.save()

        with open(filename, 'rb') as file:

            User_Query.objects.create(user_id=request.user, category=query_obj.category,
                                      no_of_records_limit=query_obj.no_of_records_limit, query_name=query_obj.query_name,
                                      query_type='Locations', query_list=json.dumps(myPythonList),
                                      output_file=File(file)).save()

        messages.error(request, 'Your requested file is ready and you can download on dashboard.')

        return redirect('dashboard')
    else:
        msg_text='You must have ' + query_obj.no_of_records_limit + ' credit lines in your account to rerun this query. Please Buy plan'
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




