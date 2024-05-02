from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import ValidationError
from .models import FollowRequest, Follower


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required = True, write_only = True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email','password', 'confirm_password')

    def validate(self, validated_data):
        password = validated_data.get('password')
        confirm_password = validated_data.get('confirm_password')

        if confirm_password!=password:
            data={
                'status':False,
                'message':"Passwords don't match"
            }
            raise ValidationError(data)
        return validated_data
    
    def save(self):
        validated_data = self.validated_data
        username = validated_data['username']
        first_name = validated_data.get('first_name', '')
        last_name = validated_data.get('last_name', '')
        email = validated_data['email']
        password = validated_data['password']

        user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()

        return user
    

class FollowRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = FollowRequest
        fields = ['id', 'from_user', 'to_user', 'is_accepted']


class FollowerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follower
        fields = ['id', 'user', 'follower']