from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Posts, Comments, Likes
from rest_framework import status
from .serializers import PostSerializer, CommentSerializer, LikeSerializer

class PostCreateApiView(APIView):
    
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class GetAllPostsListApiView(ListAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer


class MyAllPostsApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        posts = Posts.objects.filter(user=request.user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class PostUpdateApiView(UpdateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class PostDeleteApiView(DestroyAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response({'success': True, 'message': 'Post deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    

class AddCommentApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetAllPostComments(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comments.objects.filter(post_id=post_id)
    
class DestroyComment(DestroyAPIView):
    queryset = Comments.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'success': True, 
                         'message': 'Comment deleted successfully'
                         }, 
                         status=status.HTTP_204_NO_CONTENT)

    
class AddLikeApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = LikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetUsersWhoLiked(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LikeSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Likes.objects.filter(post_id=post_id)
    

class MyLikedPostsApiView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LikeSerializer

    def get_queryset(self):
        return Likes.objects.filter(user=self.request.user)
    
class DestroyMyLikeApiView(DestroyAPIView):
    queryset = Likes.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk' 

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"success": True, "message": "Like deleted successfully"}, status=status.HTTP_204_NO_CONTENT)