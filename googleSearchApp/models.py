from django.contrib.auth.models import User
from django.db import models
from authentication.models import Profile


class location_search_fields(models.Model):

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    country = models.CharField(max_length=1500,null=True, blank=True)
    is_first_cycle = models.IntegerField(null=True, blank=True)
    starting_pointer = models.IntegerField(null=True, blank=True)
    ending_pointer = models.IntegerField(null=True, blank=True)