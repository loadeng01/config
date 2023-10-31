from django.urls import path
from .views import *

urlpatterns = [
    path('', CategoryCreateListView.as_view()),
]
