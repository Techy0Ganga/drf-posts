from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('posts/', views.DetailPost.as_view(), name='post-list-create'),
    path('posts/<int:pk>', views.SinglePost.as_view(), name='pk-based'),
    # path('users/', views.ListUsers.as_view(), name='list-of-users'),
    # path('users/<int:pk>', views.RetriveUserDetails.as_view(), name='user-details')
]

urlpatterns = format_suffix_patterns(urlpatterns)