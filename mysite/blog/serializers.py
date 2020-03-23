from rest_framework import serializers
from .models import *


# Create serializers here
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('__all__')


class PostCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "content", "category", "author")


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("image",)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('__all__')