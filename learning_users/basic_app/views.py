from basic_app.models import BeneficiaryInfo, UserProfileInfo, SlotBookedInfo
from django.shortcuts import redirect, render
from .forms import UserProfileInfoForm, BeneficiaryInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import requests
from datetime import datetime, timedelta
from django.utils import timezone
from datetime import datetime
from django.views import View
import json
from types import SimpleNamespace
from django.contrib import messages
from django.utils.translation import get_language
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.csrf import (csrf_exempt, ensure_csrf_cookie,)

def getUser(email):
    user_email = email
    user = UserProfileInfo.objects.get(email=user_email)
    return user


def getBeneficiaries(user):

    beneficiaries = BeneficiaryInfo.objects.filter(user_profile=user.uid)
    return beneficiaries


def checkUserSession(request):

    if request.session.get('key'):
        return True
    return False


def getSlotInfo(beneficiaries):
    slot_info = []
    for beneficiary in beneficiaries:
        if beneficiary.slot_booked == True:
            slot_info.append( SlotBookedInfo.objects.get(beneficiary_id = beneficiary.beneficiary_id) )

    return slot_info


def index(request):

    if checkUserSession(request):

        user = getUser(request.session.get('user_email'))
        pin = user.pincode
        date = timezone.now().today().strftime("%d-%m-%Y")
        centers = requests.get(
            f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pin}&date={date}').json()
         
        beneficiaries = getBeneficiaries(user)
        slot_info =getSlotInfo(beneficiaries)
        # print(slot_info)
        # print(beneficiaries)
        context = {'user': user, 'centers': centers , 'beneficiaries':beneficiaries}

        return render(request,'basic_app/index1.html',{'user': user, 'centers': centers , 'beneficiaries':beneficiaries , 'slot_info':slot_info})

    else:

        return render(request,'basic_app/index1.html')

def user_logout(request):

    if checkUserSession(request):

        user = getUser(request.session.get('user_email'))
        user.is_authenticated = False
        user.save()

    request.session.flush()
    return render(request, 'basic_app/index.html')


def add_beneficiary(request):

    user = getUser(request.session.get('user_email'))
    if request.method == 'POST':

        beneficiary_form = BeneficiaryInfoForm(data=request.POST)

        if beneficiary_form.is_valid():

            user = getUser(request.session.get('user_email'))
    
            beneficiary = beneficiary_form.save(commit=False)
            beneficiary.user_profile = UserProfileInfo.objects.get(uid = user.uid)
            beneficiary.save()

            return HttpResponseRedirect(reverse('index'))

        else:
            print(beneficiary_form.errors)

    else:

        beneficiary_form = BeneficiaryInfoForm()

    return render(request, 'basic_app/beneficiary.html',{'beneficiary_form':beneficiary_form , 'user':user})


def register(request):

    if checkUserSession(request):

        return HttpResponseRedirect(reverse('index'))

    registered = False

    if request.method == 'POST':

        profile_form = UserProfileInfoForm(data=request.POST)

        if profile_form.is_valid():

            profile = profile_form.save(commit=False)

            profile.save()

            registered = True

            pin = profile.pincode
            date = timezone.now().today().strftime("%d-%m-%Y")
            centers = requests.get(
                f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pin}&date={date}').json()

            if len(centers['centers']) > 0:
                message = "There are slots available in your area. Please visit our website to book it."
            else:
                message = "There are no slots available in your area. Please visit our website to check for slots for other pincode."

            try:
                if profile.mail_slot_availability:
                    send_mail(
                        'Regarding Slot Availability',
                        message,
                        'yourmail@domain.com',
                        [profile.email],
                        fail_silently=False,
                    )
            finally:
                return render(request, 'basic_app/login.html')

        else:

            print(profile_form.errors)

    else:

        profile_form = UserProfileInfoForm()

    context = {'profile_form': profile_form, 'registered': registered}

    return render(request, 'basic_app/registration.html', context)


def user_login(request):

    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_email = UserProfileInfo.objects.get(email=email).email
            user_pass = UserProfileInfo.objects.get(email=email).password
        except:

            return render(request, 'basic_app/invalid.html')

        user = getUser(email)

        if user_email == email and user_pass == password:

            user.is_authenticated = True
            auth = True
            user.save()
            request.session['user_email'] = user.email
            request.session['key'] = True
            pin = user.pincode
            date = timezone.now().today().strftime("%d-%m-%Y")
            centers = requests.get(
                f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pin}&date={date}').json()

            # if user.slot_booked == True:
            #     slot_info = SlotBookedInfo.objects.get(uid=user.uid)
            #     context = {'centers': centers,
            #                'user': user, 'slot_info': slot_info}
            #     return render(request, 'basic_app/index.html', context)
            # else:
            #     context = {'centers': centers, 'user': user}
            #     return render(request, 'basic_app/index.html', context)
            return HttpResponseRedirect(reverse('index'))

        else:

            return render(request, 'basic_app/invalid.html')

    if checkUserSession(request):

        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'basic_app/login.html', {})


# @csrf_exempt

class ByPincodeView(View):

    def get(self, request, *args, **kwargs):
        pin = request.GET['pin']

        if checkUserSession(request):

            user = getUser(request.session.get('user_email'))

            date = timezone.now().today().strftime("%d-%m-%Y")
            centers = requests.get(
                f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pin}&date={date}').json()

            # print(user)
            beneficiaries = getBeneficiaries(user)
            showSlot = True
            context = {'centers': centers, 'user': user , 'beneficiaries':beneficiaries , 'showSlot':showSlot} 
            return render(request, 'basic_app/index1.html', context)
@csrf_exempt
def slot_booking(request):

    if request.method == 'POST':
        slot_info = SlotBookedInfo()

        if checkUserSession(request):
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            user = getUser(request.session.get('user_email'))
            user_email = user.email
            # print(body_data['beneficiary'])
            beneficiary = BeneficiaryInfo.objects.get(beneficiary_id=body_data['beneficiary'])
            # print(beneficiary)
            if not beneficiary.slot_booked == True:
                beneficiary.slot_booked = True
                beneficiary.save()
            else:

                return HttpResponseRedirect(reverse('index'))
        slot_info.date = body_data['date']
        beneficiary = BeneficiaryInfo.objects.get(beneficiary_id=body_data['beneficiary'])
        slot_info.beneficiary_id = BeneficiaryInfo.objects.get(beneficiary_id=beneficiary.beneficiary_id)
        slot_info.slot_timings = body_data['slot_timings']
        slot_info.center = body_data['center']
        # print(slot_info.center)
        slot_info.vaccine_type = body_data['vaccine']
        slot_info.block_name = body_data['block']
        slot_info.save()
        return HttpResponseRedirect(reverse('index'))
