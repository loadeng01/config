from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('', views.PostViewSet)

urlpatterns = [
    # path('', PostListCreateView.as_view()),
    # path('<int:pk>/', PostDetailView.as_view())
    path('', include(router.urls))
]
