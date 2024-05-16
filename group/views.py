from django.http import JsonResponse
from posts.models import Group, GroupMembership
from account.models import CustomUser
import cloudinary.uploader
from .serializers import GroupSerializer,GroupMembershipSerializer

class GroupActionsView:
    def create_group(self, request):
        if request.method == 'POST':
            name_user = request.POST.get('name_user')  
            name = request.POST.get('name')
            type = request.POST.get('type')
            description = request.POST.get('description')
            location = request.POST.get('location')

            user = CustomUser.objects.get(name=name_user)
            upload_result_img = cloudinary.uploader.upload(request.FILES['image'])
            image_url = upload_result_img['secure_url']
        
            upload_result_header = cloudinary.uploader.upload(request.FILES['header_image'])
            header_image_url = upload_result_header['secure_url']

            if Group.objects.filter(name=name).exists():
                return JsonResponse({'error': 'Group with this name already exists.'}, status=400)

            group = Group.objects.create(name=name, description=description, type=type, image=image_url, header_image=header_image_url,created_by=user, location=location)

            return JsonResponse({'message': 'Group created successfully.'})
        else:
            return JsonResponse({'error': 'Method not allowed.'}, status=405)

    def delete_group(self,request):
        group_id = request.POST.get('group_id')
        name_user = request.POST.get('name_user')

        user = CustomUser.objects.get(name=name_user)
        group = Group.objects.get(id=group_id)

        if user == group.created_by:  
            group.delete()

            return JsonResponse({'message': 'Group deleted successfully.'})
        else:
            return JsonResponse({'message': 'You are not authorized to delete this group.'}, status=403)

    def assign_admin(self,request):
        if request.method == 'POST':
            group_id = request.POST.get('group_id')
            name_user = request.POST.get('name_user')
            
            group = Group.objects.get(id=group_id)
            user = CustomUser.objects.get(name=name_user)
            group_membership = GroupMembership.objects.filter(group=group, user=user)

            for membership in group_membership:
                membership.is_admin = True
                membership.save()

            return JsonResponse({'message': 'User assigned as admin successfully.'})
        else:
            return JsonResponse({'error': 'Method not allowed.'}, status=405)
        
    def delete_assign_admin(self,request):
        if request.method == 'POST':
            group_id = request.POST.get('group_id')
            name_user = request.POST.get('name_user')
            
            group = Group.objects.get(id=group_id)
            user = CustomUser.objects.get(name=name_user)
            
            group_membership = GroupMembership.objects.get(group=group, user=user)
            
            if group_membership.is_admin:
                group_membership.is_admin = False
                group_membership.save()

                return JsonResponse({'message': 'Admin removed successfully.'})
            else:
                return JsonResponse({'message': 'User is not an admin of this group.'}, status=400)
        else:
            return JsonResponse({'error': 'Method not allowed.'}, status=405)

    def subscribe_to_group(self, request):
        if request.method == 'POST':
            group_id = request.POST.get('group_id')
            user_name = request.POST.get('user_name')

            group = Group.objects.get(id=group_id)
            user = CustomUser.objects.get(name=user_name)

            if group.members.filter(name=user).exists():
                return JsonResponse({'message': 'User is already subscribed to this group.'}, status=400)

            membership = GroupMembership.objects.filter(group=group, user=user).exists()

            if not membership:
                group_membership = GroupMembership.objects.create(group=group, user=user)
                group_membership.save()
                group.members.add(user)

                return JsonResponse({'message': 'Subscribed to group successfully.'})
            else:
                return JsonResponse({'message': 'User is already subscribed to this group.'}, status=400)
        else:
            return JsonResponse({'error': 'Method not allowed.'}, status=405)


    def unsubscribe_from_group(self, request):
        if request.method == 'POST':
            group_id = request.POST.get('group_id')
            user_name = request.POST.get('user_name')

            group = Group.objects.get(id=group_id)
            user = CustomUser.objects.get(name=user_name)

            group.members.remove(user)

            membership = GroupMembership.objects.filter(group=group, user=user).first()

            if membership:
                membership.delete()
                return JsonResponse({'message': 'Unsubscribed from group successfully.'})
            else:
                return JsonResponse({'message': 'User is not subscribed to this group.'}, status=400)
        else:
            return JsonResponse({'error': 'Method not allowed.'}, status=405)

    def search_groups(self,request):
        if request.method == 'GET':
            name_query = request.GET.get('name') 
            type_query = request.GET.get('type')

            if name_query:
                groups = Group.objects.filter(name__icontains=name_query)
            elif type_query:
                groups = Group.objects.filter(type__icontains=type_query)
            else:
                groups = Group.objects.all()

            group_data = []
            for group in groups:
                group_serializer = GroupSerializer(group)
                membership_serializer = GroupMembershipSerializer(group.groupmembership_set.all(), many=True)

                group_data.append({
                    'group': group_serializer.data,
                    'membership': membership_serializer.data
                })

            return JsonResponse(group_data, safe=False)
        else:
            return JsonResponse({'error': 'Method not allowed.'}, status=405)
        
    def update_group(self,request):
        if request.method == 'POST':
            group_id = request.POST.get('group_id')
            update_type = request.POST.get('update_type')

            group = Group.objects.get(id=group_id)

            if update_type == 'location':
                location = request.POST.get('location')
                group.location = location

            elif update_type == 'description':
                description = request.POST.get('description')
                group.description = description

            elif update_type == 'type':
                type = request.POST.get('type')
                group.type = type

            elif update_type == 'name':
                new_name = request.POST.get('name')

                if Group.objects.filter(name=new_name).exclude(id=group_id).exists():
                    return JsonResponse({'error': 'Group with this name already exists.'}, status=400)

                group.name = new_name

            elif update_type == 'image':
                upload_result = cloudinary.uploader.upload(request.FILES['image'])
                group.image_url = upload_result['secure_url']

            elif update_type == 'header_image':
                upload_result = cloudinary.uploader.upload(request.FILES['image'])
                group.header_image_url = upload_result['secure_url']

            else:
                return JsonResponse({'error': 'Invalid update type.'}, status=400)

            group.save()

            return JsonResponse({'message': f'{update_type.capitalize()} updated successfully.'})
        else:
            return JsonResponse({'error': 'Method not allowed.'}, status=405)