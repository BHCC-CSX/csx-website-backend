from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import json
from django.db import transaction


# Create your views here.
class UserList(APIView):
    """
    API Endpoint to list users.
    METHODS: GET
    """
    permission_classes = [permissions.IsAuthenticated, ]

    @swagger_auto_schema(responses={200: UserSerializer(many=True), 500: "Internal Server Error"})
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRegister(APIView):
    """
    API Endpoint to register users.
    METHODS: POST
    """
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(responses={200: "Success", 500: "Internal Server Error",
                                    400: "Bad Request", 403: "Bad Request", 201: "Created"})
    def post(self, request, format=None):
        if request.auth is None:
            data = request.data
            data = data.dict()
            serializer = UserRegisterSerializer(data=data)
            if serializer.is_valid():
                try:
                    with transaction.atomic():
                        user = serializer.save()

                        url, headers, body, token_status = self.create_token_response(request)
                        if token_status != 200:
                            raise Exception(json.loads(body).get("error_description", ""))

                        return Response(json.loads(body), status=token_status)
                except Exception as e:
                    return Response(data={"error": e.message}, status=status.HTTP_400_BAD_REQUEST)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)


class UserDetail(APIView):
    """
    API Endpoint to get the details for a user.
    METHODS: GET
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    @swagger_auto_schema(responses={200: UserSerializer(), 404: "User Not Found", 400: "Bad Request",
                                    500: "Internal Server Error"})
    def get(self, request, user_id, format=None):
        try:
            user = User.objects.get(pk=user_id)
        except Exception as e:
            return Response({"error": "User Not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Groups(APIView):
    """
    API Endpoint to get groups.
    METHODS: GET
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]

    @swagger_auto_schema(responses={200: GroupSerializer(many=True), 500: "Internal Server Error",
                                    400: "Bad Request"})
    def get(self, request, format=None):
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

