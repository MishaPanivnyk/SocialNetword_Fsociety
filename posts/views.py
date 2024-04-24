import cloudinary.uploader
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Post, Like, Comment
from .forms import PostForm
from django.contrib.auth import get_user_model
from account.models import CustomUser
from django.db.models import Q
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            author_identifier = request.POST.get('author', '')
            author = get_user_model().objects.get(Q(email=author_identifier) | Q(name=author_identifier))  
            
            post = form.save(commit=False)
            post.author = author 
            
            upload_result = cloudinary.uploader.upload(request.FILES['image'])
            post.image_url = upload_result['secure_url'] 
            
            author.post_count += 1
            author.save()

            post.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

def look_post_list_user(request, author_identifier):
    user = CustomUser.objects.get(Q(email=author_identifier) | Q(name=author_identifier))
    posts = Post.objects.filter(author=user)

    post_data = []
    for post in posts:
        comments = Comment.objects.filter(post=post)
        comments_list = []
        for comment in comments:
            comments_list.append({
                'text': comment.text,
                'created_at': comment.created_at,
                'user': {
                    'name': comment.user.name,
                    'email': comment.user.email,
                    'avatar': comment.user.avatar.url
                }
            })
        
        likes_count = Like.objects.filter(post=post).count()
        is_liked = Like.objects.filter(post=post, user=user).exists()  # Перевірка, чи вподобав поточний користувач цей пост
        post_data.append({
            'id': post.id,  
            'author': {
                'name': user.name,
                'email': user.email,
                'avatar': user.avatar.url
            },
            'post': {
                'image': post.image.url,
                'description': post.description,
                'likes': likes_count,
                'isLiked': is_liked,  
                'comments': comments_list
            }
        })
    
    return JsonResponse(post_data, safe=False)

def look_post_list_all(request, author_identifier):
    user = CustomUser.objects.get(Q(email=author_identifier) | Q(name=author_identifier))
    posts = Post.objects.annotate(likes_count=Count('like')).all()
    post_data = []
    for post in posts:
        comments_list = [comment.text for comment in post.comments.all()]  # Список коментарів для даного поста
        likes_count = post.likes_count
        is_liked = Like.objects.filter(post=post, user=user).exists()  # Перевірка, чи вподобав поточний користувач цей пост
        post_data.append({
            'id': post.id,
            'author': {
                'name': post.author.name,
                'email': post.author.email,
                'avatar': post.author.avatar.url
            },
            'post': {
                'image': post.image.url,
                'description': post.description,
                'likes': likes_count,
                'isLiked': is_liked,  
                'comments': comments_list
            }
        })
    return JsonResponse(post_data, safe=False)


def like_post(request):
    if request.method == 'POST':
        name = request.POST.get('name_user')  
        post_id = request.POST.get('post_id')  
        print(name,post_id)
        user = CustomUser.objects.get(name=name)  # Знаходимо користувача за ім'ям
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(user=user, post=post)
        if created:
            post.likes += 1
            post.save()
            like.isLike = True
            like.save()
            return JsonResponse({'message': 'Post liked successfully'})
        else:
            return JsonResponse({'message': 'You already liked this post'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

def comment_post(request):
    if request.method == 'POST':
        name = request.POST.get('name_user')
        post_id = request.POST.get('post_id')
        user = CustomUser.objects.get(name=name)  # shykaemo user за im`yam
        post = get_object_or_404(Post, id=post_id)
        comment_text = request.POST.get('comment', '')
        comment = Comment.objects.create(user=user, post=post, text=comment_text)
        comment.save()
        return JsonResponse({'message': 'Comment added successfully'})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

def delete_post(request):
    if request.method == 'POST':
        name = request.POST.get('name_user')  
        post_id = request.POST.get('post_id')  
        user = CustomUser.objects.get(name=name)  # shykaemo user за im`yam
        post = get_object_or_404(Post, id=post_id)

        user.post_count -= 1
        user.save()

        if user == post.author:
            post.delete()
            return JsonResponse({'message': 'Post deleted successfully'})
        else:
            return JsonResponse({'error': 'You are not authorized to delete this post'}, status=403)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

def unlike_post(request):
    if request.method == 'POST':
        name = request.POST.get('name_user')
        post_id = request.POST.get('post_id')
        user = CustomUser.objects.get(name=name)
        post = get_object_or_404(Post, id=post_id)
        try:
            like = Like.objects.get(user=user, post=post)
            like.delete()
            post.likes -= 1
            return JsonResponse({'message': 'Like removed successfully'})
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'You have not liked this post'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

#def delete_comment(request):
 #   if request.method == 'POST':
  #      username = request.POST.get('username')
   #     comment_id = request.POST.get('comment_id') 
    #    user = CustomUser.objects.get(username=username)
     #   try:
      #      comment = Comment.objects.get(id=comment_id)
       #     if user == comment.user:  
        #        comment.delete()
         #       return JsonResponse({'message': 'Comment deleted successfully'})
          #  else:
           #     return JsonResponse({'error': 'You are not authorized to delete this comment'}, status=403)
        #except ObjectDoesNotExist:
         #   return JsonResponse({'error': 'Comment not found'}, status=404)
    # else:
      #  return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
