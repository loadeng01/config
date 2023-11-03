from django.urls import path
from .views import *

urlpatterns = {
    path('', CommentCreateView.as_view()),
    path('<int:pk>/', CommentDetailView.as_view()),
}
