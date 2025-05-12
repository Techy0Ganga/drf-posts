from rest_framework import serializers
from .models import Post
from django.contrib.auth.models import User


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Post
        fields = ['title', 'img_url', 'content', 'likes', 'owner']

class UserSerializer(serializers.Serializer):

    posts = serializers.PrimaryKeyRelatedField(many=True, queryset=Post.objects.all())
    class Meta:
        model = User
        # fields = ['id', 'username', 'posts']
        fields = '__all__'