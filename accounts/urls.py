from django.urls import path
from .views import Forget_pass, signout, sign_up, sign_in,fail,verify,success

urlpatterns = [
    path('signin/', sign_in, name='signin'),
    path('signup/', sign_up, name='signup'),
    path('signout/', signout, name='signout'),
    path('fail/', fail, name='fail'),
    path('success/', success, name='success'),
    path('verify/<auth_token>/', verify, name='verify'),
    path('Forget_pass/', Forget_pass, name='forget_pass'),
]
