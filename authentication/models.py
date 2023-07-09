from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models


GENDER = (
    (1, "Mail"),
    (2, "Femail"),
)


class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=25, blank=True, null=True, verbose_name='Phone No')
    picture = models.ImageField(upload_to='ProfileImages', blank=True, verbose_name='Photo')
    gender = models.CharField(
        choices=GENDER, max_length=25, blank=True, null=True,
        verbose_name='Gender'
    )
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


class CommonField(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)

    class Meta:
        abstract = True

class Section(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Landing(CommonField):
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)
    link = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.section.name


class Price(models.Model):
    models.ForeignKey(Landing, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=100)
    sub_title = models.CharField(max_length=100)
    price = models.FloatField(null=True, blank=True, default=0.00)

    def __str__(self):
        return self.title

class Features(models.Model):
    to = models.ForeignKey(Price, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
