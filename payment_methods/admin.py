from django.contrib import admin
from .models import *



class Price_planAdmin(admin.ModelAdmin):

    list_display = ('id','title','price','no_of_lines','description')

admin.site.register(Price_plan,Price_planAdmin)






class SubscriberAdmin(admin.ModelAdmin):

    list_display = ('user','plan','price','subsciption_from','subsciption_to','status','payment_method','created_at')

admin.site.register(Subscriber,SubscriberAdmin)