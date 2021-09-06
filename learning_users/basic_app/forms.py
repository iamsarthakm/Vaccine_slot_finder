from django import forms
from django.contrib.auth.models import User
from django.db.models import fields
from .models import UserProfileInfo , BeneficiaryInfo
# class UserForm(forms.ModelForm):

#     class Meta():
#         model = User
#         fields = ('username','email','password')

#         widgets ={

#             'username':forms.TextInput(attrs={'class':'form-control'}),
#             'email':forms.EmailInput(attrs={'class':'form-control'}),
#             'password':forms.PasswordInput(attrs={'class':'form-control'})
#         }

class UserProfileInfoForm(forms.ModelForm):

    class Meta():

        model = UserProfileInfo
        fields = ('username','email','password','pincode','district','mail_slot_availability','age')


        widgets ={
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'password':forms.PasswordInput(attrs={'class':'form-control'}),
            'pincode':forms.NumberInput(attrs={'class':'form-control'}),
            'district':forms.TextInput(attrs={'class':'form-control'}),
            'mail_slot_availability':forms.CheckboxInput(attrs={'class':'form-control'}),
            'age':forms.NumberInput(attrs={'class':'form-control'}),
        }



class BeneficiaryInfoForm(forms.ModelForm):

    class Meta():

        model = BeneficiaryInfo
        fields = ('name',)

        widgets ={
            'name':forms.TextInput(attrs={'class':'form-control'})
        }