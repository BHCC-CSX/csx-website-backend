from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema


# Create your views here.
class PostList(APIView):
    """
    API Endpoint to List Posts
    METHODS: GET, POST
    """

    @swagger_auto_schema(responses={200: PostSerializer(many=True), 500: "Internal Server Error"})
    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(responses={201: "Post Created", 400: "Bad Request", 500: "Internal Server Error"},
                         operation_description="Creates Post",
                         request_body=PostSerializer)
    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
    """
    API Endpoint to get, edit, or delete a post.
    METHODS: GET, PATCH, DELETE
    """
    @staticmethod
    def __get_obj(obj_id):
        try:
            return Post.objects.get(pk=obj_id), None
        except:
            return None, {"error": "Post object not found."}

    @staticmethod
    def __check_category(cat_id):
        try:
            category = Category.objects.get(pk=cat_id)
            return True
        except:
            return False

    @swagger_auto_schema(responses={200: PostSerializer(many=False),
                                    404: "Post Not Found",
                                    500: "Internal Server Error"})
    def get(self, request, post_id, format=None):
        post, error = self.__get_obj(post_id)
        if post is None:
            return Response(data=error, status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: "Success",
                                    404: "Post Not Found",
                                    400: "Bad Request",
                                    500: "Internal Server Error"},
                         request_body=PostSerializer(partial=True))
    def patch(self, request, post_id, format=None):
        post, error = self.__get_obj(post_id)
        if post is None:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: "No Content",
                                    404: "Post Not Found",
                                    500: "Internal Server Error"})
    def delete(self, request, post_id, format=None):
        post, error = self.__get_obj(post_id)
        if post is None:
            return Response(data=error, status=status.HTTP_404_NOT_FOUND)

        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryList(APIView):
    """
    API Endpoint to get or create categories.
    METHODS: GET, POST
    """
    @swagger_auto_schema(responses={200: CategorySerializer(many=True), 500: "Internal Server Error"})
    def get(self, request, format=None):
        cats = Category.objects.all()
        serializer = CategorySerializer(cats, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(responses={201: "Post Created", 400: "Bad Request", 500: "Internal Server Error"},
                         request_body=CategorySerializer())
    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CategoryDetails(APIView):
    """
    API Endpoint to get or delete a category.
    METHODS: DELETE
    """
    @staticmethod
    def __get_obj(obj_id):
        try:
            return Category.objects.get(pk=obj_id), None
        except:
            return None, {'error': 'Category object not found.'}

    @swagger_auto_schema(responses={200: CategorySerializer(many=False),
                                    404: "Category Not Found",
                                    500: "Internal Server Error"})
    def get(self, request, cat_id, format=None):
        cat, error = self.__get_obj(cat_id)
        if cat is None:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(cat)
        return Response(serializer.data)

    @swagger_auto_schema(responses={204: "No Content", 404: "Category Not Found", 500: "Internal Server Error"})
    def delete(self, request, cat_id, format=None):
        cat, error = self.__get_obj(cat_id)
        if cat is None:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        cat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
