from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Reel, LikeReels, CommentReels
from .forms import ReelForm
from account.models import CustomUser
from django.contrib.auth import get_user_model
import cloudinary.uploader
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers.json import DjangoJSONEncoder

class ReelView:
    def create_reel(self, request):
        if request.method == 'POST':
            form = ReelForm(request.POST, request.FILES)
            if form.is_valid():
                author_identifier = request.POST.get('author', '')
                author = get_user_model().objects.get(Q(email=author_identifier) | Q(name=author_identifier))

                reel = form.save(commit=False)
                reel.author = author

                upload_result = cloudinary.uploader.upload(request.FILES['video'], resource_type="video",
                                                        format='mp4') 
                reel.video = upload_result['secure_url']

                author.reel_count += 1
                author.save()

                reel.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'errors': form.errors}, status=400)
        else:
            return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


    def like_reel(self, request):
            if request.method == 'POST':
                name = request.POST.get('name_user')
                reel_id = request.POST.get('reel_id')
                user = CustomUser.objects.get(name=name)
                reel = get_object_or_404(Reel, id=reel_id)
                like, created = LikeReels.objects.get_or_create(user=user, reel=reel)
                if created:
                    reel.likes += 1
                    reel.save()
                    like.is_like = True
                    like.save()
                    return JsonResponse({'message': 'Reel liked successfully'})
                else:
                    return JsonResponse({'message': 'You already liked this reel'}, status=400)
            else:
                return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
        
    def unlike_reel(self, request):
        if request.method == 'POST':
            name = request.POST.get('name_user')
            reel_id = request.POST.get('reel_id')
            user = CustomUser.objects.get(name=name)
            reel = get_object_or_404(Reel, id=reel_id)
            try:
                like = LikeReels.objects.get(user=user, reel=reel)
                reel.likes -= 1
                reel.save()
                like.delete()
                return JsonResponse({'message': 'Like removed successfully'})
            except LikeReels.DoesNotExist:
                return JsonResponse({'message': 'You have not liked this reel'}, status=400)
        else:
            return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

    def comment_reel(self, request):
        if request.method == 'POST':
            name = request.POST.get('name_user')
            reel_id = request.POST.get('reel_id')

            try:
                user = CustomUser.objects.get(name=name)
                reel = Reel.objects.get(id=reel_id)

                comment_text = request.POST.get('comment')
                if comment_text:
                    comment = CommentReels.objects.create(user=user, reel=reel, text=comment_text)
                    return JsonResponse({'message': 'Comment added successfully'})
                else:
                    return JsonResponse({'error': 'Comment text is empty'}, status=400)
            except (ObjectDoesNotExist, ValueError):
                return JsonResponse({'error': 'User or reel not found'}, status=404)
        else:
            return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
        
    def delete_comment(self, request):
        if request.method == 'POST':
            comment_id = request.POST.get('comment_id')
            try:
                comment = CommentReels.objects.get(id=comment_id)
                comment.delete()
                return JsonResponse({'message': 'Comment deleted successfully'})
            except CommentReels.DoesNotExist:
                return JsonResponse({'error': 'Comment not found'}, status=404)
        else:
            return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
        
    def look_reel_list_user(self, request, author_identifier):
        user = CustomUser.objects.get(Q(email=author_identifier) | Q(name=author_identifier))
        reels = Reel.objects.filter(author=user)
        reel_data = []
        for reel in reels:
            comments_list = [] 
            for comment in reel.comments.all():  
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
            likes_count = LikeReels.objects.filter(reel=reel).count()
            is_liked = LikeReels.objects.filter(reel=reel, user=user).exists()
            
            video_url = reel.video.url if isinstance(reel.video, cloudinary.models.CloudinaryResource) else reel.video
            
            reel_data.append({
                'id': reel.id,
                'author': {
                    'name': user.name,
                    'email': user.email,
                    'avatar': user.avatar.url
                },
                'reel': {
                    'video': video_url,
                    'description': reel.description,
                    'likes': likes_count,
                    'isLiked': is_liked,
                    'comments': comments_list  
                }
            })
        return JsonResponse(reel_data, encoder=DjangoJSONEncoder, safe=False)

    def look_reel_list_all(self, request):
        reels = Reel.objects.all()
        reel_data = []
        for reel in reels:
            comments_list = [] 
            for comment in reel.comments.all(): 
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
            likes_count = LikeReels.objects.filter(reel=reel).count()
            
            video_url = reel.video.url if isinstance(reel.video, cloudinary.models.CloudinaryResource) else reel.video

            reel_data.append({
                'id': reel.id,
                'author': {
                    'name': reel.author.name,
                    'email': reel.author.email,
                    'avatar': reel.author.avatar.url
                },
                'reel': {
                    'video': video_url,
                    'description': reel.description,
                    'likes': likes_count,
                    'comments': comments_list  
                }
            })
        return JsonResponse(reel_data, encoder=DjangoJSONEncoder, safe=False)