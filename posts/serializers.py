from rest_framework import serializers
from .models import Posts, Comments, Likes

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = [ 'user', 'content', 'created_at']
        


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['post', 'user', 'comment', 'created_at']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = '__all__'