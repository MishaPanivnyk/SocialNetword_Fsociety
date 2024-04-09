import cloudinary.uploader
from django.conf import settings
from django.http import JsonResponse
from .models import Post
from .forms import PostForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

@csrf_exempt
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            author_name = request.POST.get('author', '')
            author = get_user_model().objects.filter(name=author_name).first()
            
            if not author:
                return JsonResponse({'success': False, 'error': 'User not found'}, status=404)
            
            post = form.save(commit=False)
            post.author = author 
            
            upload_result = cloudinary.uploader.upload(request.FILES['image'])
            post.image_url = upload_result['secure_url'] 
            
            post.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        return JsonResponse({'success': False, 'error': 'Only POST requests are allowed'}, status=405)

def look_post_list_user(request, author_name):
    posts = Post.objects.filter(author__name=author_name)

    post_data = [{'author': post.author.name, 'image': post.image.url, 'description': post.description} for post in posts]
    
    return JsonResponse(post_data, safe=False)



def look_post_list_all(request):
    posts = Post.objects.all()
    post_data = [{'author': post.author.name, 'image': post.image.url, 'description': post.description} for post in posts]
    return JsonResponse(post_data, safe=False)