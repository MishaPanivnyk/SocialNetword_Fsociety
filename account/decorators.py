from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework import status

def login_required(view_func):
    def wrapper(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': 'Необхідно авторизуватися для доступу до цього ресурсу.'}, status=status.HTTP_401_UNAUTHORIZED)
        return view_func(self, request, *args, **kwargs)
    return wrapper


def anonymous_required(view_func):
    def wrapper(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            raise PermissionDenied('Для доступу до цього ресурсу потрібно бути анонімним користувачем.')
        return view_func(self, request, *args, **kwargs)
    return wrapper