from django.contrib import admin
from .models import Group, GroupMembership

class GroupAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'description', 'type', 'created_by')
    list_filter = ('type', 'created_by')
    search_fields = ('name', 'description', 'created_by__username')
    readonly_fields = ('created_at',)
    filter_horizontal = ('members',)

admin.site.register(Group, GroupAdmin)

class GroupMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'is_admin')
    list_filter = ('group', 'is_admin')
    search_fields = ('user__username', 'group__name')
    readonly_fields = ('user', 'group')

admin.site.register(GroupMembership, GroupMembershipAdmin)