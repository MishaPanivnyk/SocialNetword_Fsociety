# Generated by Django 5.0.3 on 2024-03-21 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_customuser_avatar'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='friendship',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='friendship',
            name='from_user',
        ),
        migrations.RemoveField(
            model_name='friendship',
            name='to_user',
        ),
        migrations.RemoveField(
            model_name='group',
            name='members',
        ),
        migrations.RemoveField(
            model_name='grouppost',
            name='group',
        ),
        migrations.RemoveField(
            model_name='grouppost',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='grouppost',
            name='user',
        ),
        migrations.RemoveField(
            model_name='grouppostcomment',
            name='group_post',
        ),
        migrations.RemoveField(
            model_name='grouppostlike',
            name='group_post',
        ),
        migrations.RemoveField(
            model_name='grouppostcomment',
            name='user',
        ),
        migrations.RemoveField(
            model_name='grouppostlike',
            name='user',
        ),
        migrations.RemoveField(
            model_name='like',
            name='post',
        ),
        migrations.RemoveField(
            model_name='like',
            name='user',
        ),
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='message',
            name='recipient',
        ),
        migrations.RemoveField(
            model_name='message',
            name='sender',
        ),
        migrations.RemoveField(
            model_name='post',
            name='user',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Friendship',
        ),
        migrations.DeleteModel(
            name='Group',
        ),
        migrations.DeleteModel(
            name='GroupPost',
        ),
        migrations.DeleteModel(
            name='GroupPostComment',
        ),
        migrations.DeleteModel(
            name='GroupPostLike',
        ),
        migrations.DeleteModel(
            name='Like',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]
