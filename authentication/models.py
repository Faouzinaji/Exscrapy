from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)

    phone = models.CharField(max_length=25, blank=True, null=True, verbose_name='Phone No')

    picture = models.ImageField(upload_to='ProfileImages', blank=True, verbose_name='Photo')



    gender = models.CharField(max_length=25, blank=True, null=True, verbose_name='Gender')
    profession = models.CharField(max_length=25, blank=True, null=True)
    otp = models.CharField(max_length=25, blank=True, null=True, verbose_name='OTP')


    changed_default_password = models.CharField(max_length=500, blank=True, default='No', null=True,verbose_name='Changed Default Password?')
    joined_via = models.CharField(max_length=2500, blank=True, null=True,verbose_name='How joined?')


    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='Updated At')


    class Meta:
        verbose_name = 'User Profile'

    def __str__(self):
        return self.owner.username