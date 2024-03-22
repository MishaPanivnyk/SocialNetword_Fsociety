from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import my_profile  # імпортуємо модель профілю користувача

@login_required
def my_profile_view(request, user_id):
    user_profile = get_object_or_404(my_profile, pk=user_id)  # Отримуємо профіль користувача за його ідентифікатором
    profile_data = {
        'email': user_profile.user.email,  # Отримуємо email користувача через зв'язок з профілем
        'username': user_profile.user.username,
        'avatar': user_profile.user.avatar.url if user_profile.user.avatar else None,
        'bio': user_profile.user.bio,
        'birth_date': user_profile.user.birth_date,
        'located': user_profile.user.located,
        'is_email_verified': user_profile.user.is_email_verified,
        # Додайте інші дані з профілю користувача за необхідністю
    }
    return JsonResponse(profile_data)
