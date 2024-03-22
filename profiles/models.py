from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def my_profile(request):
    user = request.user
    profile_data = {
        'email': user.email,
        'username': user.username,
        'avatar': user.avatar.url if user.avatar else None,
        'bio': user.bio,
        'birth_date': user.birth_date,
        'located': user.located,
        'is_email_verified': user.is_email_verified,
        'friends': list(user.friends.values_list('friend__name', flat=True)),
        'sent_messages': list(user.sent_messages.values_list('content', flat=True)),
        'received_messages': list(user.received_messages.values_list('content', flat=True)),
    }
    return JsonResponse(profile_data)
