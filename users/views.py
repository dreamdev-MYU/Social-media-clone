from .serializers import RegisterSerializer, FollowRequestSerializer, FollowerSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.generics import ListAPIView
from .models import FollowRequest, Follower
from django.contrib.auth.models import User


class RegisterApiView(APIView):

  def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': serializer.data,
                'refresh': str(refresh),
                'access':str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
class LoginApiView(APIView):
    def post(self, request, *args, **kwargs):

        username = request.data.get('username')
        password = request.data.get('password')

     
        user = authenticate(username=username, password=password)
        if user:
            
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': {'id': user.id, 'username': user.username},  
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
           
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class SendFollowRequestApiView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        to_user_id = request.data.get('to_user_id')
        if not to_user_id:
            return Response({'error': 'to_user_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        to_user = User.objects.filter(id=to_user_id).first()
        if not to_user:
            return Response({'error': 'Invalid to_user_id'}, status=status.HTTP_400_BAD_REQUEST)

        if FollowRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
            return Response({'error': 'You already sent a follow request to this user'}, status=status.HTTP_400_BAD_REQUEST)

        follow_request = FollowRequest(from_user=request.user, to_user=to_user)
        follow_request.save()
        return Response({'success': 'Follow request sent'}, status=status.HTTP_200_OK)


class MyFollowRequestsApiView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        follow_requests = FollowRequest.objects.filter(to_user=request.user)
        serializer = FollowRequestSerializer(follow_requests, many=True)
        return Response(serializer.data)
    

class AcceptFollowRequestApiView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def patch(self, request, *args, **kwargs):
        follow_request_id = request.data.get('follow_request_id')
        if not follow_request_id:
            return Response({'error': 'follow_request_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        follow_request = FollowRequest.objects.filter(id=follow_request_id).first()
        if not follow_request:
            return Response({'error': 'Invalid follow_request_id'}, status=status.HTTP_400_BAD_REQUEST)

        if follow_request.to_user != request.user:
            return Response({'error': 'You are not authorized to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)

        follow_request.accepted = True
        follow_request.save()
        Follower.objects.create(user=request.user, follower=follow_request.from_user)
        return Response({'success': 'Follow request accepted'}, status=status.HTTP_200_OK)
    
  
class DeleteFollowRequestApiView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        follow_request_id = request.data.get('follow_request_id')
        if not follow_request_id:
            return Response({'error': 'follow_request_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        follow_request = FollowRequest.objects.filter(id=follow_request_id).first()
        if not follow_request:
            return Response({'error': 'Invalid follow_request_id'}, status=status.HTTP_400_BAD_REQUEST)

        if follow_request.from_user != request.user:    
            return Response({'error': 'You are not authorized to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)

        follow_request.delete()
        return Response({'success': 'Follow request deleted'}, status=status.HTTP_200_OK)
    
class IgnoreFollowRequestApiView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def patch(self, request, *args, **kwargs):
        follow_request_id = request.data.get('follow_request_id')
        if not follow_request_id:
            return Response({'error': 'follow_request_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        follow_request = FollowRequest.objects.filter(id=follow_request_id).first()
        if not follow_request:
            return Response({'error': 'Invalid follow_request_id'}, status=status.HTTP_400_BAD_REQUEST)

        if follow_request.to_user != request.user:
            return Response({'error': 'You are not authorized to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)

        follow_request.delete()
        return Response({'success': 'Follow request ignored'}, status=status.HTTP_200_OK)



class MyAllFollowersListApiView(ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FollowerSerializer

    def get_queryset(self):
        return Follower.objects.filter(user=self.request.user)