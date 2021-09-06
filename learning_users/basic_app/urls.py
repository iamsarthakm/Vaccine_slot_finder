from django.urls import path
from . import views

# SET THE NAMESPACE!
app_name = 'basic_app'

# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    path('register/',views.register,name='register'),
    path('user_login/',views.user_login,name='user_login'),
    path('slot_booking/',views.slot_booking,name='slot_booking'),
    path('add_beneficiary/',views.add_beneficiary,name='add_beneficiary'),
    # path('user_feedback/',views.user_feedback,name='user_feedback'),
]
