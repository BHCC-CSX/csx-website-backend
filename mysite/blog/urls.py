from django.urls import path, include
from rest_framework import routers
from . import views

# Create your URLs here
router = routers.DefaultRouter()

urlpatterns = [
    path('', views.PostList.as_view()),
    path('posts/', views.PostList.as_view()),
    path('posts/<int:post_id>/', views.PostDetail.as_view()),
    path('posts/<int:post_id>/image/', views.PostImage.as_view()),
    path('categories/', views.CategoryList.as_view(), name="category-list"),
    path('categories/<int:cat_id>/', views.CategoryDetails.as_view()),
]