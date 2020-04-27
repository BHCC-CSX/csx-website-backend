from .serializers import *
from django.db.models import Case, When
from rest_framework.views import APIView
from mysite.views import CustomAPIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import permission_classes
from mysite.parsers import ImageParser
from rest_framework import status, permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Create your views here.
class PostList(CustomAPIView):
    """
    API Endpoint to List Posts
    METHODS: GET, POST
    """
    permission_classes = {"get": [permissions.AllowAny],
                          "post": [permissions.IsAuthenticated]}

    @swagger_auto_schema(responses={200: PostSerializer(many=True), 500: "Internal Server Error"})
    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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


class PostDetail(CustomAPIView):
    """
    API Endpoint to get, edit, or delete a post.
    METHODS: GET, PATCH, DELETE
    """
    permission_classes = {"get": [permissions.AllowAny],
                          "patch": [permissions.IsAuthenticated],
                          "delete": [permissions.IsAdminUser]}
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


class PostImage(CustomAPIView):
    parser_classes = (MultiPartParser, ImageParser)

    permission_classes = [permissions.IsAuthenticated]

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


class CategoryList(CustomAPIView):
    """
    API Endpoint to get or create categories.
    METHODS: GET, POST
    """
    permission_classes = {"get": [permissions.AllowAny],
                          "post": [permissions.IsAdminUser]}

    @swagger_auto_schema(responses={200: CategorySerializer(many=True), 500: "Internal Server Error"})
    def get(self, request, format=None):
        cats = Category.objects.all()
        serializer = CategorySerializer(cats, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(responses={201: "Post Created", 400: "Bad Request", 500: "Internal Server Error"},
                         request_body=CategorySerializer())
    def post(self, request, format=None):
        cat = Category.objects.filter(name=request.data['name'])

        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            data = serializer.data
            data['id'] = obj.id
            return Response(data, status=status.HTTP_201_CREATED)
        if len(cat) > 0:
            msg = {"error": "Category already exists"}
        else:
            msg = {"error": "Bad Request"}
        return Response(msg, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetails(CustomAPIView):
    """
    API Endpoint to get or delete a category.
    METHODS: DELETE
    """
    permission_classes = {"get": [permissions.AllowAny],
                          "delete": [permissions.IsAdminUser]}

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


class CategoryPosts(CustomAPIView):
    """
    Endpoint for getting the posts of a category.
    METHODS: GET
    """
    permission_classes = {"get": [permissions.AllowAny]}

    @swagger_auto_schema(responses={200: PostSerializer(many=True), 204: "No Content",
                                    404: "Category Not Found", 500: "Internal Server Error"})
    def get(self, request, cat_id, format=None):
        try:
            cat = Category.objects.get(pk=cat_id)
        except:
            return Response({"error": "Category could not be found!"}, status=status.HTTP_404_NOT_FOUND)
        posts = Post.objects.filter(category=cat)
        if len(posts) is 0:
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ResolveCategoryID(APIView):
    """
    Endpoint to get IDs for given category names.
    METHODS: POST
    """
    permission_classes = [permissions.AllowAny]
    name_schema = openapi.Schema(type="string")
    request_schema = openapi.Schema(type="array", items=name_schema)

    @swagger_auto_schema(responses={200: openapi.Response("Success",
                                                          schema=CategoryIDSerializer,
                                                          examples={"application/json": [1, 2]}),
                                    404: "Category Not Found", 500: "Internal Server Error",
                                    400: "Bad Request"},
                         operation_id="blog_categories_names_to_ids", request_body=request_schema)
    def post(self, request, format=None):
        names = set(request.data)  # Remove duplicates
        objs = Category.objects.filter(name__in=names)
        data = {obj.name: obj.id for obj in objs}
        if len(names) == len(objs):
            return Response(data, status=status.HTTP_200_OK)

        return Response({"error": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)


class ResolveCategoryName(APIView):
    """
    Endpoint to get names for given category IDs.
    METHODS: POST
    """
    permission_classes = [permissions.AllowAny]
    name_schema = openapi.Schema(type="integer")
    request_schema = openapi.Schema(type="array", items=name_schema)

    @swagger_auto_schema(responses={200: openapi.Response("Success",
                                                          schema=CategoryIDSerializer,
                                                          examples={"application/json": [1, 2]}),
                                    404: "Category Not Found", 500: "Internal Server Error",
                                    400: "Bad Request"},
                         operation_id="blog_categories_ids_to_names", request_body=request_schema)
    def post(self, request, format=None):
        ids = set(request.data)  # Remove duplicates
        names = Category.objects.filter(pk__in=ids)
        data = {name.id: name.name for name in names}
        if len(names) == len(ids):
            return Response(data, status=status.HTTP_200_OK)

        return Response({"error": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)
