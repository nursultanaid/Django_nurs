from django.core.mail import send_mail
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.views import APIView
from users.serializers import UserCreateSerializer, UserLoginSerializer, CodeSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import random
from users.models import Code

class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
            email=serializer.validated_data['email'],
            is_active=False
        )
        code = ''.join([str(random.randint(0, 9)) for i in range(6)])
        Code.objects.create(code=code, user=user)
        send_mail(
            'Your code',
            message=code,
            from_email='<EMAIL>',
            recipient_list=[user.email]
        )
        return Response(data={'user_id': user.id}, status=status.HTTP_201_CREATED)

# class RegistrationAPIView(APIView):
#     def post(self, request):
#         serializer = UserCreateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = User.objects.create_user(
#             username=serializer.validated_data['username'],
#             password=serializer.validated_data['password'],
#             email=serializer.validated_data['email'],
#             is_active=False
#         )
#         code = ''.join([str(random.randint(0, 9)) for i in range(6)])
#         SmsCode.objects.create(code=code, user=user)
#         send_mail(
#             'Your code',
#             message=code,
#             from_email='<EMAIL>',
#             recipient_list=[user.email]
#         )
#         # Step 3: Return Response
#         return Response(data={'user_id': user.id}, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key})
        return Response(status=status.HTTP_401_UNAUTHORIZED, data={'error': 'Invalid user or password'})


class ConfirmAPIView(APIView):
    def post(self, request):
        serializer = CodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']
        try:
            sms = Code.objects.get(code=code)
        except Code.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Code is invalid'})
        sms.user.is_active = True
        sms.user.save()
        sms.delete()
        return Response(data={'active': True}, status=status.HTTP_200_OK)