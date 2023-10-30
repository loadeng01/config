from django.urls import path
from .views import *
# from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogOutView.as_view())

]
