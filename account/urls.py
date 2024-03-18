# urls.py
from django.urls import path
from .views import RegisterView, ObtainTokenView, LogoutView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('api/token/', ObtainTokenView.as_view(), name='token_obtain'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
]
