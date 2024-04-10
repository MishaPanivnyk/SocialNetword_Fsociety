import cloudinary.uploader
from django.conf import settings
from django.http import JsonResponse
from .models import Post
from .forms import PostForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from account.models import CustomUser
from django.db.models import Q

@csrf_exempt
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
            
            post.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        return JsonResponse({'success': False, 'error': 'Only POST requests are allowed'}, status=405)

def look_post_list_user(request, author_identifier):
    posts = Post.objects.filter(author__email=author_identifier) | Post.objects.filter(author__name=author_identifier)
    user = get_user_model().objects.get(Q(email=author_identifier) | Q(name=author_identifier))

    post_data = [{
        'author': {
            'name': user.name,
            'email': user.email,
            'avatar': user.avatar.url
        },
        'posts': [{
            'image': post.image.url,
            'description': post.description
        } for post in posts]
    }]
    
    return JsonResponse(post_data, safe=False)



def look_post_list_all(request):
    posts = Post.objects.all()
    post_data = [{
        'author': {
            'name': post.author.name,
            'email': post.author.email,
            'avatar': post.author.avatar.url
        },
        'image': post.image.url,
        'description': post.description
    } for post in posts]
    return JsonResponse(post_data, safe=False)