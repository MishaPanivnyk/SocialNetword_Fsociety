from django.http import JsonResponse
from .models import Message
from django.contrib.auth.models import User

from django.http import JsonResponse
from .models import Message
from account.models import CustomUser
from django.db.models import Q  # Додалимо імпорт для Q-об'єктів

def create_chat(request):
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver_id')  # Зміна на receiver_id
        content = request.POST.get('content')
        
        try:
            receiver = CustomUser.objects.get(id=receiver_id)  # Зміна на отримання користувача за ідентифікатором
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'Receiver not found'}, status=400)
        
        message = Message.objects.create(sender=request.user, receiver=receiver, content=content)
        return JsonResponse({'status': 'Chat created successfully'}, status=201)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
def get_chat_history(request, receiver_id):  # Оновлено сигнатуру функції
    if request.method == 'GET':
        try:
            receiver = CustomUser.objects.get(id=receiver_id)  # Зміна на отримання користувача за ідентифікатором
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'Receiver not found'}, status=400)
        
        messages = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=request.user))
        ).order_by('timestamp')

        history = [{
            'sender': msg.sender.id,
            'receiver': msg.receiver.id,
            'content': msg.content,
            'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        } for msg in messages]

        return JsonResponse({'history': history})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
def get_chat_messages(request, receiver_id):  # Оновлено сигнатуру функції
    if request.method == 'GET':
        try:
            receiver = CustomUser.objects.get(id=receiver_id)  # Зміна на отримання користувача за ідентифікатором
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'Receiver not found'}, status=400)
        
        messages = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=request.user))
        ).order_by('timestamp')

        history = [{
            'sender': msg.sender.id,
            'receiver': msg.receiver.id,
            'content': msg.content,
            'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        } for msg in messages]

        return JsonResponse({'messages': history})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
