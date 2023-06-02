from django.contrib import admin

# Register your models here.
from .models import *
from googleSearchApp.models import *


class CountryAdmin(admin.ModelAdmin):
    list_display = ('country', 'state','place','zipcode',)

    search_fields = ('country',)
    list_filter = ('country',)
    list_per_page = 500

admin.site.register(Wallet)
admin.site.register(User_Query)
admin.site.register(Categories)
admin.site.register(Country,CountryAdmin)
admin.site.register(location_search_fields)