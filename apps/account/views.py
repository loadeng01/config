from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import RegistrationSerializer
from rest_framework.response import Response


class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Аккаунт успешно создан', status=201)






