from django.contrib.auth.models import User
from django.db import models
from authentication.models import Profile
from django.utils.timezone import now

# Create your models here.
class Wallet(models.Model):

    user_id = models.ForeignKey(Profile,on_delete=models.CASCADE)

    available_requests_balance= models.IntegerField(null=True, blank=True)

    description = models.CharField(max_length=2000,null=True, blank=True)
    inserted_on = models.DateField(default=now,null=True, blank=True)
    updated_on = models.DateField(default=now,null=True, blank=True)



class User_Query(models.Model):

    user_id = models.ForeignKey(User,on_delete=models.CASCADE)



    category = models.CharField(max_length=2000,null=True, blank=True)
    query_type = models.CharField(max_length=2000,null=True, blank=True)
    country = models.CharField(max_length=2000,null=True, blank=True)
    no_of_records_limit = models.IntegerField(null=True, blank=True)

    locations = models.CharField(max_length=2000,null=True, blank=True)
    query_list = models.TextField(max_length=25000,null=True, blank=True)
    query_name = models.CharField(max_length=2000,null=True, blank=True)
    output_file = models.FileField(max_length=25000,upload_to='scrapped_files', blank=True,null=True, verbose_name='Scrapped Files')
    inserted_on = models.DateField(default=now,null=True, blank=True)
    updated_on = models.DateField(default=now,null=True, blank=True)



class Country(models.Model):
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100,blank=True,null=True)
    place = models.CharField(max_length=100,blank=True,null=True)
    zipcode = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.country



class Categories(models.Model):
    name = models.CharField(max_length=21000,blank=True,null=True)


    def __str__(self):
        return self.name