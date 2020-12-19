from django.urls import path
from .views import CategoryPosts, ViewPost, BlogPosts

urlpatterns = [
    path('', BlogPosts.as_view(), name='blog'),
    path('category/<int:category_id>/', CategoryPosts.as_view(), name='category'),
    path('blog/<int:post_id>', ViewPost.as_view(), name='view_post'),
]