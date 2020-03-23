from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from mysite.parsers import ImageParser
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
                         request_body=PostCreationSerializer)
    def post(self, request, format=None):
        serializer = PostCreationSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            data = serializer.data
            data["id"] = obj.id
            return Response(data, status=status.HTTP_201_CREATED)
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

        serializer = PostCreationSerializer(post, data=request.data, partial=True)
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


class PostImage(APIView):
    parser_classes = (MultiPartParser, ImageParser)

    @swagger_auto_schema(responses={201: "Resource Created",
                                    400: "Bad Request",
                                    404: "Post Not Found",
                                    415: "Unsupported Media Type",
                                    500: "Internal Server Error"},
                         operation_description="Set the image for a project.",
                         request_body=PostImageSerializer)
    def post(self, request, post_id, format=None):
        try:
            post = Post.objects.get(pk=post_id)
        except:
            return Response({"error": "Post Not Found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            serializer = PostImageSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response({"error": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "Unsupported Media Type"}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)


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
