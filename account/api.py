from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import CustomUserSerializer
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class SignUpView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            # Відправлення листа для верифікації облікового запису
            subject = 'Підтвердження облікового запису'
            message = render_to_string('verification_email.html', {
                'user': user,
                'domain': request.build_absolute_uri('/')[:-1],  # Отримання домену
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),  # Кодування ідентифікатора користувача
                'token': default_token_generator.make_token(user),  # Створення токена
            })
            send_mail(subject, message, None, [user.email])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(APIView):
    def post(self, request):
        email = request.data.get('email')
        user = get_object_or_404(CustomUser, email=email)

        # Відправлення листа для скидання пароля
        subject = 'Скидання пароля'
        message = render_to_string('password_reset_email.html', {
            'user': user,
            'domain': request.build_absolute_uri('/')[:-1],  # Отримання домену
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),  # Кодування ідентифікатора користувача
            'token': default_token_generator.make_token(user),  # Створення токена
        })
        send_mail(subject, message, None, [user.email])

        return Response({'message': 'Лист для скидання пароля надіслано на вашу електронну адресу.'}, status=status.HTTP_200_OK)

class SocialLogoutView(APIView):
    def post(self, request):
        # Додайте вашу логіку виходу з соціальної мережі тут
        return Response({'message': 'Ви вийшли зі свого облікового запису у соціальній мережі.'}, status=status.HTTP_200_OK)

class SignInView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        try:
            user = CustomUser.objects.get(email=email)
            if user.check_password(password):
                # Ви можете додати тут будь-яку логіку для успішного входу
                return Response({'message': 'Успішний вхід'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Неправильний пароль'}, status=status.HTTP_401_UNAUTHORIZED)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Користувача з таким email не існує'}, status=status.HTTP_404_NOT_FOUND)
