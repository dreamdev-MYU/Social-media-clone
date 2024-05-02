from django.urls import path
from .views import (RegisterApiView,LoginApiView,SendFollowRequestApiView, 
                    MyFollowRequestsApiView, AcceptFollowRequestApiView,DeleteFollowRequestApiView,
                    IgnoreFollowRequestApiView, MyAllFollowersListApiView)


urlpatterns = [
    path('register/', RegisterApiView.as_view()),
    path('login/', LoginApiView.as_view()),
    path('send-follow-requests/', SendFollowRequestApiView.as_view()),
    path('my-follow-requests/', MyFollowRequestsApiView.as_view() ),
    path('accept-request/', AcceptFollowRequestApiView.as_view() ),
    path('delete-follower/', DeleteFollowRequestApiView.as_view() ),
    path('ignore-request/', IgnoreFollowRequestApiView.as_view() ),
    path('my-all-followers/', MyAllFollowersListApiView.as_view() ),
]
