from django.urls import path
from .views import my_profile_view

urlpatterns = [
    path('<int:user_id>/', my_profile_view, name='my_profile'),
]