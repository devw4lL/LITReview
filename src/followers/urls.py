from django.urls import path

from .views import GetCustomUser, FollowedFollowers, follow_user, unfollow_user

app_name = "followers"

urlpatterns = [
    path('search_users/', GetCustomUser.as_view(), name="get-users"),
    path('social/', FollowedFollowers.as_view(), name="social"),
    path('follow/<int:pk>/', follow_user, name="follow"),
    path('unfollow/<int:pk>', unfollow_user, name="unfollow"),
]