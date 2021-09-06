from django.contrib import admin
from .models import UserProfileInfo, BeneficiaryInfo , SlotBookedInfo

# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(BeneficiaryInfo)
admin.site.register(SlotBookedInfo)
