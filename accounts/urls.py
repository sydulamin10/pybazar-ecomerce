from django.urls import path
from .views import Forget_pass,sign_up,sign_in


urlpatterns = [
    path('signin/', sign_in, name='signin'),
    path('signup/', sign_up, name='signup'),
    path('Forget_pass/', Forget_pass, name='forget_pass'),
]