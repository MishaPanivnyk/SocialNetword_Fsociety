from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, logout
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from .models import CustomUser
from .serializers import CustomUserSerializer
from F_backend.settings import EMAIL_HOST_USER
import os
from django.conf import settings
from rest_framework.authentication import SessionAuthentication 
from django.http import JsonResponse

class EmailVerificationView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_bytes(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(CustomUser, pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            return Response({'error': 'Invalid verification link'}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            user.is_email_verified = True
            user.is_active = True
            user.save()
            return Response({'message': 'Email successfully verified'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid verification link'}, status=status.HTTP_400_BAD_REQUEST)

class SignUpView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            default_avatar_path = os.path.join(settings.BASE_DIR, 'account/avatar.jpg')
            user.avatar.save('avatar.jpg', open(default_avatar_path, 'rb'), save=True)

            subject = 'Підтвердження електронної адреси'
            message = f"""
                Вітаємо, {user.email}!\n\n
                Дякуємо за реєстрацію. Будь ласка, перейдіть за посиланням нижче, щоб підтвердити свій обліковий запис:\n\n
               Посилання для підтвердження: {user.get_email_verification_url(request)}\n\n
                Якщо ви не реєструвалися на нашому сайті, просто проігноруйте цей лист.\n\n
                З повагою,\n
                Ваша команда
            """
            send_mail(subject, message, EMAIL_HOST_USER, [user.email],)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(APIView):
    def post(self, request):
        email = request.data.get('email')
        user = get_object_or_404(CustomUser, email=email)
        # Sending password reset email logic
        return Response({'message': 'Лист для скидання пароля надіслано на вашу електронну адресу.'}, status=status.HTTP_200_OK)

class SignInView(APIView):
    authentication_classes = [SessionAuthentication] 

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # Генеруємо і зберігаємо токен для користувача
            user.account_token = str(default_token_generator.make_token(user))
            print(user.account_token )
            user.save()
            return Response({'message': 'Успішний вхід', 'account_token': user.account_token}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Неправильний email або пароль'}, status=status.HTTP_401_UNAUTHORIZED)

class ObtainTokenView(APIView):
    authentication_classes = [SessionAuthentication]  

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Неправильні облікові дані'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    authentication_classes = [SessionAuthentication]  
    def post(self, request):
        logout(request)
        return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)

def my_profile_view(request, account_token):
    user = CustomUser.objects.filter(account_token=account_token).first()
    if user:
        serializer = CustomUserSerializer(user)
        return JsonResponse(serializer.data)
    else:
        return JsonResponse({'error': 'Invalid token'}, status=404)
