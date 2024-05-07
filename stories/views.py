from datetime import timezone
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Story, LikeStory, CommentStory
from account.models import CustomUser
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
import cloudinary.uploader
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Story, LikeStory, CommentStory
from account.models import CustomUser
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

class StoryView:
    def create_story(self, request):
        if request.method == 'POST':
            author_identifier = request.POST.get('author', '')
            author = get_user_model().objects.get(Q(email=author_identifier) | Q(name=author_identifier))
            
            # Отримати дані про сторіс з запиту
            description = request.POST.get('description', '')
            
            # Перевірка, чи є в запиті відео чи зображення
            if 'video' in request.FILES:
                # Завантажити відео в Cloudinary
                upload_result = cloudinary.uploader.upload(request.FILES['video'], resource_type="video", format='mp4')
                media_url = upload_result['secure_url']
            elif 'image' in request.FILES:
                # Завантажити зображення в Cloudinary
                upload_result = cloudinary.uploader.upload(request.FILES['image'], resource_type="image")
                media_url = upload_result['secure_url']
            else:
                return JsonResponse({'error': 'No video or image provided'}, status=400)
            
            # Створити новий об'єкт сторісу і зберегти його в базі даних
            story = Story.objects.create(author=author, media=media_url, description=description)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
        
    def like_story(self, request):
        if request.method == 'POST':
            user_name = request.POST.get('user_name', '')
            story_id = request.POST.get('story_id', '')
            user = CustomUser.objects.get(name=user_name)
            story = get_object_or_404(Story, id=story_id)
            like, created = LikeStory.objects.get_or_create(user=user, story=story)
            if created:
                story.like += 1  
                story.save() 
                like.is_like = True
                like.save()
                return JsonResponse({'message': 'Story liked successfully'})
            else:
                return JsonResponse({'message': 'You already liked this story'}, status=400)
        else:
            return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

    def unlike_story(self, request):
        if request.method == 'POST':
            user_name = request.POST.get('user_name', '')
            story_id = request.POST.get('story_id', '')
            user = CustomUser.objects.get(name=user_name)
            story = get_object_or_404(Story, id=story_id)
            try:
                like = LikeStory.objects.get(user=user, story=story)
                story.like -= 1  
                story.save() 
                like.delete()
                return JsonResponse({'message': 'Like removed successfully'})
            except LikeStory.DoesNotExist:
                return JsonResponse({'message': 'You have not liked this story'}, status=400)
        else:
            return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

    def comment_story(self, request):
        if request.method == 'POST':
            user_name = request.POST.get('user_name', '')
            story_id = request.POST.get('story_id', '')
            comment_text = request.POST.get('comment_text', '')
            user = CustomUser.objects.get(name=user_name)
            story = get_object_or_404(Story, id=story_id)
            if comment_text:
                comment = CommentStory.objects.create(user=user, story=story, text=comment_text)
                return JsonResponse({'message': 'Comment added successfully'})
            else:
                return JsonResponse({'error': 'Comment text is empty'}, status=400)
        else:
            return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

    def delete_comment(self, request):
        if request.method == 'POST':
            comment_id = request.POST.get('comment_id', '')
            try:
                comment = CommentStory.objects.get(id=comment_id)
                comment.delete()
                return JsonResponse({'message': 'Comment deleted successfully'})
            except CommentStory.DoesNotExist:
                return JsonResponse({'error': 'Comment not found'}, status=404)
        else:
            return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

    def look_story_list_user(self, request, author_identifier):
        if request.method == 'GET':
            user_name = CustomUser.objects.get(Q(email=author_identifier) | Q(name=author_identifier))
            stories = Story.objects.filter(author=user_name)

            story_data = []
            for story in stories:
                comments_list = []
                for comment in story.comments.all():
                    comment_author = {
                        'name': comment.user_name.name,
                        'email': comment.user_name.email,
                        'avatar': comment.user_name.avatar.url
                    }
                    comments_list.append({
                        'id': comment.id,
                        'author': comment_author,
                        'text': comment.text
                    })
                story_data.append({
                    'id': story.id,
                    'author': {
                        'name': user_name.name,
                        'email': user_name.email,
                        'avatar': user_name.avatar.url
                    },
                    'story': {
                        'media': story.media.url,
                        'description': story.description,
                        'comments': comments_list,
                        'like': story.like,
                    }
                })
            return JsonResponse(story_data, safe=False)
        else:
            return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)

    def look_story_list_all(self, request):
        if request.method == 'GET':
            stories = Story.objects.all()
            story_data = []
            for story in stories:
                comments_list = []
                for comment in story.comments.all():
                    comment_author = {
                        'name': comment.user.name,
                        'email': comment.user.email,
                        'avatar': comment.user.avatar.url
                    }
                    comments_list.append({
                        'id': comment.id,
                        'author': comment_author,
                        'text': comment.text
                    })
                story_data.append({
                    'id': story.id,
                    'author': {
                        'name': story.author.name,
                        'email': story.author.email,
                        'avatar': story.author.avatar.url
                    },
                    'story': {
                        'media': story.media.url,
                        'description': story.description,
                        'comments': comments_list,
                        'like': story.like
                    }
                })
            return JsonResponse(story_data, safe=False)
        else:
            return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)
        
    def delete_old_stories(self, request):
        if request.method == 'POST':
            current_time = timezone.now()
            time_threshold = current_time - timedelta(hours=1)
            old_stories = Story.objects.filter(created_at__lt=time_threshold)
            old_stories.delete()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
        
    def delete_own_story(self, request):
        if request.method == 'POST':
            story_id = request.POST.get('story_id')
            if story_id is None:
                return JsonResponse({'error': 'Story ID is required in the request'}, status=400)
            story = get_object_or_404(Story, id=story_id)
            story.delete()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
