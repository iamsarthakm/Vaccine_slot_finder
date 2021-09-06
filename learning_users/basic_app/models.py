from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.db.models.fields import AutoField
from django.db.models.fields.related import ForeignKey
from django.db.models import IntegerField, Model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _
# SuperUserInformation
# User: Jose
# Email: training@pieriandata.com
# Password: testpassword

# Create your models here.


class UserProfileInfo(models.Model):

    # Create relationship (don't inherit from User!)
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=264)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=264, null=False)
    uid = models.AutoField(primary_key=True)
    age = models.IntegerField(null=True)
    pincode = models.IntegerField(null=True,  validators=[MaxValueValidator(
        999999), MinValueValidator(100000, _('Please enter Valid Pincode'))])
    district = models.CharField(max_length=264, null=True)
    mail_slot_availability = models.BooleanField(null=True)
    slot_booked = models.BooleanField(null=True)
    is_authenticated = models.BooleanField(default=False)
    #slot_id = models.OneToOneField('SlotBookedInfo',on_delete=DO_NOTHING,null=True)

    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.username

class BeneficiaryInfo(models.Model):

    name = models.CharField(max_length=264)
    beneficiary_id = models.AutoField(primary_key=True)
    slot_booked = models.BooleanField(default=False)
    user_profile = models.ForeignKey(UserProfileInfo , on_delete=CASCADE)

    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.name



class SlotBookedInfo(models.Model):

    date = models.CharField(max_length=264)
    slot_id = models.AutoField(primary_key=True, null=False)
    beneficiary_id = models.OneToOneField(BeneficiaryInfo, on_delete=CASCADE, null=True)
    slot_timings = models.CharField(max_length=264)
    center = models.CharField(max_length=264)
    vaccine_type = models.CharField(max_length=264)
    block_name = models.CharField(max_length=264)

    def __str__(self):
        return self.center
