import cloudinary.uploader
from django.conf import settings
from django.http import JsonResponse
from .models import Post
from .forms import PostForm
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            
            # Завантаження зображення на Cloudinary
            upload_result = cloudinary.uploader.upload(request.FILES['image'])
            post.image_url = upload_result['secure_url']  # Збереження URL зображення з Cloudinary
            
            post.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        return JsonResponse({'success': False, 'error': 'Only POST requests are allowed'}, status=405)

def api_post_list(request):
    posts = Post.objects.all()
    post_data = [{'author': post.author.name, 'image': post.image_url, 'description': post.description} for post in posts]
    return JsonResponse(post_data, safe=False)

def post_list(request):
    posts = Post.objects.all()
    post_data = [{'author': post.author.name, 'image': post.image_url, 'description': post.description} for post in posts]
    return JsonResponse(post_data, safe=False)
