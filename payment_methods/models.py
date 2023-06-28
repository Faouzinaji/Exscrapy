from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils.timezone import now


class Price_plan(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=1500,null=True,blank=True)
    price = models.IntegerField()
    perline_price = models.FloatField(null=True,blank=True)

    no_of_lines=models.IntegerField()
    plan_img = models.ImageField(upload_to='Plan Images', blank=True, verbose_name='Plan Images')



    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = 'Price Plans'


class Subscriber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    plan = models.ForeignKey(Price_plan, on_delete=models.CASCADE, null=True)
    price = models.CharField(max_length=50)
    payment_method = models.CharField(max_length=50,null=True,blank=True)
    subsciption_from = models.DateField(verbose_name='Subscription From')
    subsciption_to = models.DateField(verbose_name='Subscription To')
    stripeCustomerId = models.CharField(max_length=255, verbose_name='Stripe Customer Id',null=True,blank=True)
    stripeSubscriptionId = models.CharField(max_length=255, verbose_name='Stripe Subscription Id',null=True,blank=True)
    status = models.CharField(default='Expire',max_length=50,null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')





    class Meta:
        verbose_name_plural = 'Subscribers'



class transaction_history(models.Model):

    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    plan = models.ForeignKey(Price_plan, on_delete=models.CASCADE, null=True)



    inserted_on = models.DateField(default=now,null=True, blank=True)
    updated_on = models.DateField(default=now,null=True, blank=True)

    def __str__(self):
        return self.user_id