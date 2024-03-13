from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPAirView, TokenRefreshView

from . import api

urlpatterns = [
    path('sipnup/',api.signup, name='signup'),
    path('login/', TokenObtainPAirView.as_view(), name='token_obtain'),
    path('login/', TokenRefreshView.as_view(), name='token_refresh')
]
