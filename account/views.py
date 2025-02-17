# views.py

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, logout , login
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
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from rest_framework.generics import UpdateAPIView
import cloudinary

class EmailVerificationView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_bytes(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(CustomUser, pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            # Якщо не вдається знайти користувача, перенаправте на сторінку з невдалим підтвердженням
            return HttpResponseRedirect('https://fsociety-new.netlify.app/#/confirm-request-not-found')

        if default_token_generator.check_token(user, token):
            user.is_email_verified = True
            user.is_active = True
            user.save()
            # Якщо підтвердження пройшло успішно, перенаправте на сторінку з успішним підтвердженням
            return HttpResponseRedirect('https://fsociety-new.netlify.app/#/successfully-confirmed-email')
        else:
            # Якщо токен недійсний, перенаправте на сторінку з невдалим підтвердженням
            return HttpResponseRedirect('https://fsociety-new.netlify.app/#/confirm-request-not-found')

class SignUpView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            if not user.avatar:
                upload_result = cloudinary.uploader.upload(os.path.join(settings.BASE_DIR, 'default_avatar.jpg'))
                user.avatar = upload_result['secure_url']
                user.save()

            subject = 'Підтвердження електронної адреси'
            message = f"""
                Congratulations, {user.email}!\n\n
                Thank you for registering.Please follow the link below to verify your account\n\n
                Confirmation link:: {user.get_email_verification_url(request)}\n\n
                If you have not registered on our site, simply ignore this email\n\n
                Best regards,
                Fsociety,\n

            """
            send_mail(subject, message, EMAIL_HOST_USER, [user.email],)

            user.account_token = str(default_token_generator.make_token(user))
            user.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(APIView):
    def post(self, request):
        email = request.data.get('email')
        user = get_object_or_404(CustomUser, email=email)
        return Response({'message': 'Лист для скидання пароля надіслано на вашу електронну адресу.'}, status=status.HTTP_200_OK)
    

class SignInView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            user.account_token = str(default_token_generator.make_token(user))
            user.save()
            return Response({'message': 'Успішний вхід', 'accessToken': user.account_token}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Incorrect email or password'}, status=status.HTTP_401_UNAUTHORIZED)


def my_profile_view(request, accessToken):

    if accessToken:
        try:
            user = CustomUser.objects.get(account_token=accessToken)
            serializer = CustomUserSerializer(user)
            return JsonResponse(serializer.data, safe=False)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'No user found with this token'}, status=404)
    else:
        return JsonResponse({'error': 'The user is not authorized'}, status=401)

class UpdateMyProfileView(APIView):
    def patch(self, request, accessToken):
        user = get_object_or_404(CustomUser, account_token=accessToken)
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            new_name = serializer.validated_data.get('name', None)
            if new_name and CustomUser.objects.filter(name=new_name).exclude(id=user.id).exists():
                return Response({'error': 'A user with that name already exists'}, status=status.HTTP_400_BAD_REQUEST)

            avatar_image = request.FILES.get('avatar', None)
            if avatar_image:
                upload_result = cloudinary.uploader.upload(avatar_image)
                serializer.validated_data['avatar'] = upload_result['secure_url']

            #user.save()
            # Оновлення об'єкта користувача з новими даними перед збереженням
            serializer.save()
            
            # Повернення оновлених даних
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LogoutView(APIView):
    def post(self, request):
        account_token = request.data.get('account_token')
        if account_token:
            try:
                user = CustomUser.objects.get(account_token=account_token)
                user.account_token = None
                user.save(update_fields=['account_token'])

                response = Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
                response.delete_cookie('accessToken')
                return response
            except CustomUser.DoesNotExist:
                return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Missing account_token.'}, status=status.HTTP_400_BAD_REQUEST)
