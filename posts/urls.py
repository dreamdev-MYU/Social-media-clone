from django.urls import path
from .views import (PostCreateApiView,GetAllPostsListApiView, 
                    MyAllPostsApiView,UpdateAPIView, PostDeleteApiView, AddCommentApiView,
                     GetAllPostComments, DestroyComment, AddLikeApiView, GetUsersWhoLiked, MyLikedPostsApiView, DestroyMyLikeApiView) 


urlpatterns = [
    path('create-post/', PostCreateApiView.as_view() ),
    path('all-posts/', GetAllPostsListApiView.as_view()),
    path('my-posts/', MyAllPostsApiView.as_view()),
    path('update-post/<int:pk>/', UpdateAPIView.as_view()),
    path('delete-post/<int:pk>/', PostDeleteApiView.as_view()), 

    path('leave-comment/', AddCommentApiView.as_view()),
    path('all-comments/<int:post_id>/', GetAllPostComments.as_view()),
    path('delete-comment/<int:pk>/', DestroyComment.as_view()),

    path('leave-like/', AddLikeApiView.as_view()),
    path('users-like/<int:post_id>/', GetUsersWhoLiked.as_view()),
    path('my-likes/', MyLikedPostsApiView.as_view()),
    path('delete-like/<int:pk>/', DestroyMyLikeApiView.as_view()),
]
