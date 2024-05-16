from django.urls import path
from .views import GroupActionsView

GroupActionsView = GroupActionsView()

urlpatterns = [
    path('create_group/', GroupActionsView.create_group, name='create_group'),
    path('delete_group/', GroupActionsView.delete_group, name='delete_group'),
    path('assign_admin/', GroupActionsView.assign_admin, name='assign_admin'),
    path('delete_assign_admin/', GroupActionsView.delete_assign_admin, name='delete_assign_admin'),
    path('update_group/', GroupActionsView.update_group, name='update_group'),
    path('subscribe_to_group/', GroupActionsView.subscribe_to_group, name='subscribe_to_group'),
    path('unsubscribe_from_group/', GroupActionsView.unsubscribe_from_group, name='unsubscribe_from_group'),
    path('search_groups/', GroupActionsView.search_groups, name='search_groups'),
]