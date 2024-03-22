from django.urls import path
from .views import SignUpView, ObtainTokenView, LogoutView, SignInView, PasswordResetView, EmailVerificationView, my_profile_view, message_view, friend_view

urlpatterns = [
    path('register/', SignUpView.as_view(), name='register'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('login/', SignInView.as_view(), name='login'),
    path('api/token/', ObtainTokenView.as_view(), name='token_obtain'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify/<str:uidb64>/<str:token>/', EmailVerificationView.as_view(), name='verify_email'),
    path('mypage/<str:account_token>/', my_profile_view, name='mypage'),
    path('message/<str:account_token>/', message_view, name='message'),
    path('friend/<str:account_token>/', friend_view, name='friend'),
]